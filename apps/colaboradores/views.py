from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Colaborador
from .formulario import ColaboradorForm

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
            # Permanece na tela de cadastro (com o form limpo)
            return redirect('colaboradores:cadastrar')
        else:
            # Pega o primeiro campo com erro para mostrar no alerta conforme o wireframe
            primeiro_erro = list(form.errors.keys())[0] if form.errors else ''
            nome_campo = form.fields[primeiro_erro].label if primeiro_erro in form.fields else primeiro_erro
            messages.error(request, f'Usuário não foi cadastrado! Preencher o campo: {nome_campo}')
    else:
        form = ColaboradorForm()

    return render(request, 'colaboradores/cadastrar.html', {
        'form': form,
        'titulo': 'Cadastrar Colaborador',
        'botao_texto': 'SALVAR',
    })


def listar_colaboradores(request):
    """
    Lista colaboradores com suporte a pesquisa por nome.
    """
    termo_busca = request.GET.get('busca', '').strip()
    
    if termo_busca:
        colaboradores = Colaborador.objects.filter(nome__icontains=termo_busca)
    else:
        colaboradores = Colaborador.objects.all().order_by('-id')

    return render(request, 'colaboradores/listar.html', {
        'colaboradores': colaboradores,
        'termo_busca': termo_busca,
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
            messages.error(request, 'Erro ao atualizar colaborador. Verifique os campos.')
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

    # Caso alguém tente acessar direto por GET, volta pra lista
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