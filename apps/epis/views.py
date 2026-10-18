import unicodedata
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Equipamento
from .formulario import EquipamentoForm

# Create your views here.

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
            # Permanece na tela de cadastro limpa conforme requisito
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
    Remove acentos e converte para minúsculas para busca insensível a acentuação.
    Ex: 'Óculos de Proteção' -> 'oculos de protecao'
    """
    if not texto:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    ).lower()


def listar_equipamentos(request):
    """
    Lista todos os equipamentos com suporte a busca insensível a acentos por nome ou número do CA.
    """
    termo_busca = request.GET.get('busca', '').strip()
    todos = Equipamento.objects.all().order_by('-id')
    if termo_busca:
        termo_normalizado = remover_acentos(termo_busca)
        # Filtra os equipamentos ignorando acentuação e maiúsculas/minúsculas
        equipamentos = [
            e for e in todos
            if termo_normalizado in remover_acentos(e.nome)
            or termo_normalizado in remover_acentos(e.ca_numero)
        ]
    else:
        equipamentos = todos
    return render(request, 'epis/listar.html', {
        'equipamentos': equipamentos,
        'termo_busca': termo_busca,
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