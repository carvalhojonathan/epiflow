import os
import base64
import unicodedata
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Emprestimo
from .formulario import EmprestimoForm, EmprestimoEdicaoForm
from apps.colaboradores.models import Colaborador
from apps.epis.models import Equipamento


def remover_acentos(texto):
    """Remove acentos e converte para minúsculas para busca insensível a acentuação."""
    if not texto:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    ).lower()


def aplicar_ordenacao(emprestimos, campo, direcao):
    """
    Ordena a lista de empréstimos com base no campo e direção ('asc' ou 'desc').
    Campos suportados: colaborador, equipamento, data_emprestimo, devolucao_prevista, devolucao_real, status.
    """
    reverse = (direcao == 'desc')

    if campo == 'colaborador':
        return sorted(emprestimos, key=lambda x: remover_acentos(x.colaborador.nome), reverse=reverse)
    elif campo == 'equipamento':
        return sorted(emprestimos, key=lambda x: remover_acentos(x.equipamento.nome), reverse=reverse)
    elif campo == 'data_emprestimo':
        return sorted(emprestimos, key=lambda x: (x.data_emprestimo, x.id), reverse=reverse)
    elif campo == 'devolucao_prevista':
        if reverse:
            return sorted(
                emprestimos,
                key=lambda x: (x.data_devolucao_prevista is not None, x.data_devolucao_prevista),
                reverse=True
            )
        else:
            return sorted(
                emprestimos,
                key=lambda x: (x.data_devolucao_prevista is None, x.data_devolucao_prevista)
            )
    elif campo == 'devolucao_real':
        if reverse:
            return sorted(
                emprestimos,
                key=lambda x: (x.data_devolucao_real is not None, x.data_devolucao_real),
                reverse=True
            )
        else:
            return sorted(
                emprestimos,
                key=lambda x: (x.data_devolucao_real is None, x.data_devolucao_real)
            )
    elif campo == 'status':
        return sorted(emprestimos, key=lambda x: remover_acentos(x.status), reverse=reverse)
    else:
        # Padrão: mais recentes primeiro
        return sorted(emprestimos, key=lambda x: (x.data_emprestimo, x.id), reverse=True)


def cadastrar_emprestimo(request):
    """
    Cadastra um novo empréstimo ou fornecimento de EPI.
    - Se for válido, subtrai 1 unidade do saldo de estoque do equipamento.
    - Permanece na tela de cadastro limpa após salvar com sucesso.
    """
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            equipamento = emprestimo.equipamento

            # Decrementa 1 unidade do estoque
            equipamento.saldo_estoque = max(0, equipamento.saldo_estoque - 1)
            equipamento.save(update_fields=['saldo_estoque'])

            emprestimo.save()
            messages.success(
                request,
                f'Empréstimo registrado com sucesso! Saldo restante de "{equipamento.nome}": {equipamento.saldo_estoque} un.'
            )
            return redirect('emprestimos:cadastrar')
        else:
            primeiro_campo = list(form.errors.keys())[0] if form.errors else ''
            msg_erro = form.errors[primeiro_campo][0] if primeiro_campo in form.errors else 'Verifique os dados preenchidos.'
            messages.error(request, f'Erro ao registrar empréstimo! {msg_erro}')
    else:
        form = EmprestimoForm()

    return render(request, 'emprestimos/cadastrar.html', {
        'form': form,
        'titulo': 'Controle de EPI',
        'botao_texto': 'SALVAR',
    })


def listar_emprestimos(request):
    """
    Lista todos os empréstimos com suporte a busca e ordenação por colunas (asc/desc).
    """
    termo_busca = request.GET.get('busca', '').strip()
    campo_ordenacao = request.GET.get('campo', 'data_emprestimo')
    direcao_ordenacao = request.GET.get('direcao', 'desc')

    todos = Emprestimo.objects.select_related('colaborador', 'equipamento').all()

    if termo_busca:
        termo_normalizado = remover_acentos(termo_busca)
        emprestimos = [
            e for e in todos
            if termo_normalizado in remover_acentos(e.colaborador.nome)
            or termo_normalizado in remover_acentos(e.colaborador.matricula)
            or termo_normalizado in remover_acentos(e.equipamento.nome)
            or termo_normalizado in remover_acentos(e.equipamento.ca_numero)
            or termo_normalizado in remover_acentos(e.status)
        ]
    else:
        emprestimos = list(todos)

    # Aplica ordenação dinâmica
    emprestimos = aplicar_ordenacao(emprestimos, campo_ordenacao, direcao_ordenacao)

    return render(request, 'emprestimos/listar.html', {
        'emprestimos': emprestimos,
        'termo_busca': termo_busca,
        'campo_ordenacao': campo_ordenacao,
        'direcao_ordenacao': direcao_ordenacao,
    })


def editar_emprestimo(request, id):
    """
    Edita um empréstimo existente / dá baixa na devolução.
    - Se o status mudar para 'Devolvido', o equipamento retorna ao estoque (+1).
    - Se o status era 'Devolvido' e for revertido para outro status, sai do estoque (-1).
    """
    emprestimo = get_object_or_404(Emprestimo, id=id)
    status_anterior = emprestimo.status

    if request.method == 'POST':
        form = EmprestimoEdicaoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            novo_status = form.cleaned_data['status']
            equipamento = emprestimo.equipamento

            # Atualização inteligente do saldo de estoque conforme a transição de status
            # 1. Item devolvido ao estoque
            if novo_status == 'Devolvido' and status_anterior != 'Devolvido':
                equipamento.saldo_estoque += 1
                equipamento.save(update_fields=['saldo_estoque'])
            # 2. Reversão (estava como Devolvido e voltou para Emprestado, Danificado, Perdido ou Fornecido)
            elif status_anterior == 'Devolvido' and novo_status != 'Devolvido':
                equipamento.saldo_estoque = max(0, equipamento.saldo_estoque - 1)
                equipamento.save(update_fields=['saldo_estoque'])

            form.save()
            messages.success(request, 'Empréstimo atualizado com sucesso!')
            return redirect('emprestimos:listar')
        else:
            primeiro_campo = list(form.errors.keys())[0] if form.errors else ''
            msg_erro = form.errors[primeiro_campo][0] if primeiro_campo in form.errors else 'Verifique os dados preenchidos.'
            messages.error(request, f'Erro ao atualizar empréstimo! {msg_erro}')
    else:
        form = EmprestimoEdicaoForm(instance=emprestimo)

    return render(request, 'emprestimos/editar.html', {
        'form': form,
        'emprestimo': emprestimo,
        'titulo': 'Editar Empréstimo de EPI',
        'botao_texto': 'ATUALIZAR',
    })


def excluir_emprestimo(request, id):
    """
    Exclui um registro de empréstimo após confirmação.
    Se o registro estava em aberto (Emprestado ou Fornecido), estorna a unidade de volta ao estoque.
    """
    emprestimo = get_object_or_404(Emprestimo, id=id)
    if request.method == 'POST':
        descricao = f"{emprestimo.equipamento.nome} para {emprestimo.colaborador.nome}"
        equipamento = emprestimo.equipamento

        # Se o item estava em posse do colaborador (fora do estoque), devolve ao estoque ao excluir
        if emprestimo.status in ['Emprestado', 'Fornecido']:
            equipamento.saldo_estoque += 1
            equipamento.save(update_fields=['saldo_estoque'])
            msg_estoque = f" (1 unidade de '{equipamento.nome}' retornou ao estoque)"
        else:
            msg_estoque = ""

        emprestimo.delete()
        messages.success(request, f'Registro de "{descricao}" removido com sucesso!{msg_estoque}')
        return redirect('emprestimos:listar')

    return redirect('emprestimos:listar')


def relatorio_emprestimos(request):
    """
    Tela de Relatórios de Controle de EPI com filtros cumulativos do tipo AND:
    - Colaborador (select com busca inteligente ou texto)
    - Equipamento (select com busca inteligente ou texto)
    - Status (Emprestado, Fornecido, Devolvido, Danificado, Perdido)
    - Ordenação dinâmica em todas as colunas (asc/desc)
    """
    colaborador_busca = request.GET.get('colaborador', '').strip()
    equipamento_busca = request.GET.get('equipamento', '').strip()
    status_busca = request.GET.get('status', '').strip()
    campo_ordenacao = request.GET.get('campo', 'data_emprestimo')
    direcao_ordenacao = request.GET.get('direcao', 'desc')

    # Compatibilidade com parâmetro antigo ?ordem=recentes/antigos
    ordem_antiga = request.GET.get('ordem')
    if ordem_antiga == 'antigos':
        campo_ordenacao = 'data_emprestimo'
        direcao_ordenacao = 'asc'
    elif ordem_antiga == 'recentes':
        campo_ordenacao = 'data_emprestimo'
        direcao_ordenacao = 'desc'

    emprestimos = Emprestimo.objects.select_related('colaborador', 'equipamento').all()
    colaboradores = Colaborador.objects.filter(ativo=True).order_by('nome')
    equipamentos = Equipamento.objects.filter(ativo=True).order_by('nome')

    # Filtro AND 1: Colaborador (por ID do select ou por digitação de nome/matrícula)
    colaborador_selecionado = None
    if colaborador_busca:
        if colaborador_busca.isdigit():
            colaborador_selecionado = Colaborador.objects.filter(id=colaborador_busca).first()
            if colaborador_selecionado:
                emprestimos = [e for e in emprestimos if e.colaborador_id == colaborador_selecionado.id]
        else:
            termo = remover_acentos(colaborador_busca)
            emprestimos = [
                e for e in emprestimos
                if termo in remover_acentos(e.colaborador.nome)
                or termo in remover_acentos(e.colaborador.matricula)
            ]

    # Filtro AND 2: Equipamento (por ID do select ou por digitação de nome/CA)
    equipamento_selecionado = None
    if equipamento_busca:
        if equipamento_busca.isdigit():
            equipamento_selecionado = Equipamento.objects.filter(id=equipamento_busca).first()
            if equipamento_selecionado:
                emprestimos = [e for e in emprestimos if e.equipamento_id == equipamento_selecionado.id]
        else:
            termo = remover_acentos(equipamento_busca)
            emprestimos = [
                e for e in emprestimos
                if termo in remover_acentos(e.equipamento.nome)
                or termo in remover_acentos(e.equipamento.ca_numero)
            ]

    # Filtro AND 3: Status
    if status_busca:
        emprestimos = [e for e in emprestimos if e.status == status_busca]

    # Aplica ordenação dinâmica
    emprestimos = aplicar_ordenacao(emprestimos, campo_ordenacao, direcao_ordenacao)

    # Carrega a logo em base64 para evitar bloqueios de CORS no html2pdf/html2canvas
    logo_base64 = ''
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo-icone.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as img_f:
            logo_base64 = f"data:image/png;base64,{base64.b64encode(img_f.read()).decode('utf-8')}"

    return render(request, 'emprestimos/relatorios.html', {
        'emprestimos': emprestimos,
        'total_registros': len(emprestimos),
        'colaboradores': colaboradores,
        'equipamentos': equipamentos,
        'colaborador_busca': colaborador_busca,
        'equipamento_busca': equipamento_busca,
        'colaborador_selecionado': colaborador_selecionado,
        'equipamento_selecionado': equipamento_selecionado,
        'status_busca': status_busca,
        'status_choices': Emprestimo.STATUS_CHOICES,
        'status_opcoes': Emprestimo.STATUS_CHOICES,
        'filtros_ativos': bool(colaborador_busca or equipamento_busca or status_busca),
        'campo_ordenacao': campo_ordenacao,
        'direcao_ordenacao': direcao_ordenacao,
        'logo_base64': logo_base64,
    })
