import unicodedata
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Emprestimo
from .formulario import EmprestimoForm, EmprestimoEdicaoForm


def remover_acentos(texto):
    """Remove acentos e converte para minúsculas para busca insensível a acentuação."""
    if not texto:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    ).lower()


def cadastrar_emprestimo(request):
    """
    Cadastra um novo empréstimo ou fornecimento de EPI.
    Permanece na tela de cadastro limpa após salvar com sucesso.
    """
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empréstimo registrado com sucesso!')
            return redirect('emprestimos:cadastrar')
        else:
            messages.error(request, 'Erro ao registrar empréstimo! Verifique os dados preenchidos.')
    else:
        form = EmprestimoForm()

    return render(request, 'emprestimos/cadastrar.html', {
        'form': form,
        'titulo': 'Registrar Empréstimo de EPI',
        'botao_texto': 'SALVAR',
    })


def listar_emprestimos(request):
    """
    Lista todos os empréstimos com suporte a busca por colaborador ou equipamento.
    """
    termo_busca = request.GET.get('busca', '').strip()
    todos = Emprestimo.objects.select_related('colaborador', 'equipamento').all()

    if termo_busca:
        termo_normalizado = remover_acentos(termo_busca)
        emprestimos = [
            e for e in todos
            if termo_normalizado in remover_acentos(e.colaborador.nome)
            or termo_normalizado in remover_acentos(e.equipamento.nome)
        ]
    else:
        emprestimos = todos

    return render(request, 'emprestimos/listar.html', {
        'emprestimos': emprestimos,
        'termo_busca': termo_busca,
    })


def editar_emprestimo(request, id):
    """
    Edita um empréstimo existente / dá baixa na devolução.
    """
    emprestimo = get_object_or_404(Emprestimo, id=id)

    if request.method == 'POST':
        form = EmprestimoEdicaoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empréstimo atualizado com sucesso!')
            return redirect('emprestimos:listar')
        else:
            messages.error(request, 'Erro ao atualizar empréstimo! Verifique os dados.')
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
    """
    emprestimo = get_object_or_404(Emprestimo, id=id)
    if request.method == 'POST':
        descricao = f"{emprestimo.equipamento.nome} para {emprestimo.colaborador.nome}"
        emprestimo.delete()
        messages.success(request, f'Empréstimo de "{descricao}" removido com sucesso!')
        return redirect('emprestimos:listar')

    return redirect('emprestimos:listar')