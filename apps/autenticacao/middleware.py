from django.contrib.auth.middleware import LoginRequiredMiddleware


class SistemaLoginRequiredMiddleware(LoginRequiredMiddleware):
    """
    Middleware que protege todas as rotas do sistema por padrão.
    Isenta rotas do Django Admin (/admin/) para que o admin utilize
    seu próprio login nativo, rotas de autenticação e views com @login_not_required.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Permite acesso direto ao Django Admin (o admin gerencia sua própria autenticação)
        if request.path.startswith('/admin/'):
            return None
        return super().process_view(request, view_func, view_args, view_kwargs)