from django.urls import path
from . import views

app_name = 'emprestimos'

urlpatterns = [
    # Listagem de empréstimos -> /emprestimos/
    path('', views.listar_emprestimos, name='listar'),

    # Cadastro de novo empréstimo -> /emprestimos/cadastrar/
    path('cadastrar/', views.cadastrar_emprestimo, name='cadastrar'),

    # Edição / Baixa do empréstimo -> /emprestimos/1/editar/
    path('<int:id>/editar/', views.editar_emprestimo, name='editar'),

    # Exclusão do empréstimo -> /emprestimos/1/excluir/
    path('<int:id>/excluir/', views.excluir_emprestimo, name='excluir'),

    # Relatórios -> /emprestimos/relatorios/
    path('relatorios/', views.relatorio_emprestimos, name='relatorios'),
]