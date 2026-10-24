import unicodedata
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Colaborador
from .formulario import ColaboradorForm


def remover_acentos(texto):
    """
    Remove acentos e converte para minúsculas para ordenação insensível a acentuação.
    """
    if not texto:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    ).lower()


def aplicar_ordenacao_colaboradores(colaboradores, campo, direcao):
    """
    Ordena a lista de colaboradores com base no campo e direção ('asc' ou 'desc').
    Campos suportados: nome, matricula, cpf, funcao, telefone, status.
    """
    reverse = (direcao == 'desc')

    if campo == 'nome':
        return sorted(colaboradores, key=lambda x: remover_acentos(x.nome), reverse=reverse)
    elif campo == 'matricula':
        return sorted(colaboradores, key=lambda x: (x.matricula or '').lower(), reverse=reverse)
    elif campo == 'cpf':
        return sorted(colaboradores, key=lambda x: (x.cpf or ''), reverse=reverse)
    elif campo == 'funcao':
        return sorted(colaboradores, key=lambda x: remover_acentos(x.funcao or ''), reverse=reverse)
    elif campo == 'telefone':
        return sorted(colaboradores, key=lambda x: (x.telefone or ''), reverse=reverse)
    elif campo == 'status':
        # Ordenação alfabética: 'Ativo' vem antes de 'Inativo'
        return sorted(colaboradores, key=lambda x: 'Ativo' if x.ativo else 'Inativo', reverse=reverse)
    else:
        # Padrão: Nome em ordem alfabética crescente
        return sorted(colaboradores, key=lambda x: remover_acentos(x.nome), reverse=False)


def cadastrar_colaborador(request):
    """
    Cadastra um novo colaborador.
    Após salvar, exibe mensagem de feedback e permanece na tela de cadastro.
    """
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('colaboradores:cadastrar')
        else:
            primeiro_campo = list(form.errors.keys())[0] if form.errors else ''
            msg_erro = form.errors[primeiro_campo][0] if primeiro_campo in form.errors else 'Verifique os campos preenchidos.'
            messages.error(request, f'Usuário não foi cadastrado! {msg_erro}')
    else:
        form = ColaboradorForm()

    return render(request, 'colaboradores/cadastrar.html', {
        'form': form,
        'titulo': 'Cadastrar Colaborador',
        'botao_texto': 'SALVAR',
    })


def listar_colaboradores(request):
    """
    Lista colaboradores com suporte a pesquisa inteligente por nome, CPF ou matrícula
    e ordenação dinâmica pelas colunas (asc/desc).
    """
    termo_busca = request.GET.get('busca', '').strip()
    campo_ordenacao = request.GET.get('campo', 'nome')
    direcao_ordenacao = request.GET.get('direcao', 'asc')

    if termo_busca:
        termo_upper = termo_busca.upper()

        # 1. Se começou com 'F' e tem números (ex: F4, F123) -> Busca matrícula que COMEÇA com isso
        if termo_upper.startswith('F') and any(char.isdigit() for char in termo_upper):
            filtro = Q(matricula__istartswith=termo_upper) | Q(nome__icontains=termo_busca)

        # 2. Se digitou apenas números (ex: 41, 123) -> Busca CPF ou matrícula que começa com F + esse número
        elif termo_busca.isdigit():
            filtro = (
                Q(matricula__istartswith=f'F{termo_busca}') |
                Q(cpf__icontains=termo_busca) |
                Q(nome__icontains=termo_busca)
            )

        # 3. Caso padrão (texto) -> Busca por nome ou CPF formatado
        else:
            filtro = Q(nome__icontains=termo_busca) | Q(cpf__icontains=termo_busca)

        colaboradores = list(Colaborador.objects.filter(filtro).distinct())
    else:
        colaboradores = list(Colaborador.objects.all())

    # Aplica ordenação dinâmica
    colaboradores = aplicar_ordenacao_colaboradores(colaboradores, campo_ordenacao, direcao_ordenacao)

    return render(request, 'colaboradores/listar.html', {
        'colaboradores': colaboradores,
        'termo_busca': termo_busca,
        'campo_ordenacao': campo_ordenacao,
        'direcao_ordenacao': direcao_ordenacao,
    })


def editar_colaborador(request, id):
    """
    Edita um colaborador existente exibindo seus dados atuais nos campos.
    """
    colaborador = get_object_or_404(Colaborador, id=id)

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador atualizado com sucesso!')
            return redirect('colaboradores:listar')
        else:
            primeiro_campo = list(form.errors.keys())[0] if form.errors else ''
            msg_erro = form.errors[primeiro_campo][0] if primeiro_campo in form.errors else 'Verifique os campos preenchidos.'
            messages.error(request, f'Erro ao atualizar! {msg_erro}')
    else:
        form = ColaboradorForm(instance=colaborador)

    return render(request, 'colaboradores/cadastrar.html', {
        'form': form,
        'colaborador': colaborador,
        'titulo': 'Editar Colaborador',
        'botao_texto': 'Atualizar',
        'editando': True,
    })


def excluir_colaborador(request, id):
    """
    Exclui o colaborador após a confirmação do alerta.
    """
    colaborador = get_object_or_404(Colaborador, id=id)
    
    if request.method == 'POST':
        nome = colaborador.nome
        colaborador.delete()
        messages.success(request, f'Colaborador {nome} removido com sucesso!')
        return redirect('colaboradores:listar')

    return redirect('colaboradores:listar')


def alternar_status_colaborador(request, id):
    """
    Alterna o status do colaborador entre Ativo e Inativo.
    """
    colaborador = get_object_or_404(Colaborador, id=id)
    colaborador.ativo = not colaborador.ativo
    colaborador.save()
    status_txt = "ativado" if colaborador.ativo else "inativado"
    messages.success(request, f'Colaborador {colaborador.nome} foi {status_txt} com sucesso!')
    return redirect('colaboradores:listar')
