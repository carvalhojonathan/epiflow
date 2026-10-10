from django.urls import path
from . import views

app_name = 'colaboradores'

urlpatterns = [
    # Listagem de colaboradores (com pesquisa) -> /colaboradores/
    path('', views.listar_colaboradores, name='listar'),

    # Cadastro -> /colaboradores/cadastrar/
    path('cadastrar/', views.cadastrar_colaborador, name='cadastrar'),

    # Edição -> /colaboradores/1/editar/
    path('<int:id>/editar/', views.editar_colaborador, name='editar'),

    # Exclusão -> /colaboradores/1/excluir/
    path('<int:id>/excluir/', views.excluir_colaborador, name='excluir'),

    # Status -> /colaboradores/1/status/
    path('<int:id>/status/', views.alternar_status_colaborador, name='alternar_status'),
]
