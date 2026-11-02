from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_not_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme


@login_not_required
@require_http_methods(["GET", "POST"])
def login_view(request):
    # Se já estiver autenticado, vai direto para a tela inicial
    if request.user.is_authenticated:
        return redirect('nucleo:index')

    if request.method == 'GET':
        next_url = request.GET.get('next', '')
        return render(request, 'autenticacao/login.html', {'next': next_url})

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    next_url = request.POST.get('next') or request.GET.get('next', '')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            nome_exibicao = user.get_full_name() or user.username
            messages.success(request, f'Bem-vindo(a), {nome_exibicao}!')

            # Redireciona para a rota protegida que o usuário tentava acessar ou para o início
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('nucleo:index')
        else:
            messages.error(request, 'Esta conta de usuário está desativada.')
    else:
        messages.error(request, 'Usuário ou senha incorretos. Verifique suas credenciais.')

    return render(request, 'autenticacao/login.html', {
        'username': username,
        'next': next_url,
    })


@login_not_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema com sucesso.')
    return redirect('autenticacao:login')