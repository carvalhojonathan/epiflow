import unicodedata
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Equipamento
from .formulario import EquipamentoForm


def cadastrar_equipamento(request):
    """
    Cadastra um novo equipamento/EPI.
    Após salvar com sucesso, exibe feedback e permanece na tela de cadastro com formulário limpo.
    """
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento cadastrado com sucesso!')
            return redirect('epis:cadastrar')
        else:
            messages.error(request, 'Equipamento não foi cadastrado! Verifique os campos.')
    else:
        form = EquipamentoForm()

    return render(request, 'epis/cadastrar.html', {
        'form': form,
        'titulo': 'Cadastrar Equipamento',
        'botao_texto': 'SALVAR',
    })


def remover_acentos(texto):
    """
    Remove acentos e converte para minúsculas para busca e ordenação insensíveis a acentuação.
    Ex: 'Óculos de Proteção' -> 'oculos de protecao'
    """
    if not texto:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    ).lower()


def aplicar_ordenacao_equipamentos(equipamentos, campo, direcao):
    """
    Ordena a lista de equipamentos com base no campo e direção ('asc' ou 'desc').
    Campos suportados: nome, ca_numero, validade_ca, saldo_estoque, estoque_minimo, status.
    """
    reverse = (direcao == 'desc')

    if campo == 'nome':
        return sorted(equipamentos, key=lambda x: remover_acentos(x.nome), reverse=reverse)
    elif campo == 'ca_numero':
        # Se for dígito, ordena numericamente; senão, alfabeticamente
        return sorted(
            equipamentos,
            key=lambda x: (
                int(x.ca_numero) if (x.ca_numero and x.ca_numero.isdigit()) else 0,
                x.ca_numero or ''
            ),
            reverse=reverse
        )
    elif campo == 'validade_ca':
        if reverse:
            return sorted(
                equipamentos,
                key=lambda x: (x.validade_ca is not None, x.validade_ca),
                reverse=True
            )
        else:
            return sorted(
                equipamentos,
                key=lambda x: (x.validade_ca is None, x.validade_ca)
            )
    elif campo == 'saldo_estoque':
        return sorted(equipamentos, key=lambda x: x.saldo_estoque or 0, reverse=reverse)
    elif campo == 'estoque_minimo':
        return sorted(equipamentos, key=lambda x: x.estoque_minimo or 0, reverse=reverse)
    elif campo == 'status':
        # Ordenação alfabética: 'Ativo' vem antes de 'Inativo'
        return sorted(equipamentos, key=lambda x: 'Ativo' if x.ativo else 'Inativo', reverse=reverse)
    else:
        # Padrão: Nome em ordem alfabética crescente
        return sorted(equipamentos, key=lambda x: remover_acentos(x.nome), reverse=False)


def listar_equipamentos(request):
    """
    Lista todos os equipamentos com suporte a busca insensível a acentos por nome ou número do CA
    e ordenação dinâmica por colunas (asc/desc).
    """
    termo_busca = request.GET.get('busca', '').strip()
    campo_ordenacao = request.GET.get('campo', 'nome')
    direcao_ordenacao = request.GET.get('direcao', 'asc')

    todos = list(Equipamento.objects.all())

    if termo_busca:
        termo_normalizado = remover_acentos(termo_busca)
        equipamentos = [
            e for e in todos
            if termo_normalizado in remover_acentos(e.nome)
            or termo_normalizado in remover_acentos(e.ca_numero)
        ]
    else:
        equipamentos = todos

    # Aplica ordenação dinâmica
    equipamentos = aplicar_ordenacao_equipamentos(equipamentos, campo_ordenacao, direcao_ordenacao)

    return render(request, 'epis/listar.html', {
        'equipamentos': equipamentos,
        'termo_busca': termo_busca,
        'campo_ordenacao': campo_ordenacao,
        'direcao_ordenacao': direcao_ordenacao,
    })


def editar_equipamento(request, id):
    """
    Edita um equipamento existente, pré-carregando seus dados no formulário.
    """
    equipamento = get_object_or_404(Equipamento, id=id)

    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipamento atualizado com sucesso!')
            return redirect('epis:listar')
        else:
            messages.error(request, 'Erro ao atualizar equipamento! Verifique os dados.')
    else:
        form = EquipamentoForm(instance=equipamento)

    return render(request, 'epis/cadastrar.html', {
        'form': form,
        'equipamento': equipamento,
        'titulo': 'Editar Equipamento',
        'botao_texto': 'Atualizar',
        'editando': True,
    })


def excluir_equipamento(request, id):
    """
    Exclui o equipamento após confirmação no modal.
    """
    equipamento = get_object_or_404(Equipamento, id=id)

    if request.method == 'POST':
        nome = equipamento.nome
        equipamento.delete()
        messages.success(request, f'Equipamento "{nome}" removido com sucesso!')
        return redirect('epis:listar')

    return redirect('epis:listar')


def alternar_status_equipamento(request, id):
    """
    Ativa ou inativa o equipamento rapidamente.
    """
    equipamento = get_object_or_404(Equipamento, id=id)
    equipamento.ativo = not equipamento.ativo
    equipamento.save()
    status_txt = "ativado" if equipamento.ativo else "inativado"
    messages.success(request, f'Equipamento "{equipamento.nome}" foi {status_txt} com sucesso!')
    return redirect('epis:listar')
