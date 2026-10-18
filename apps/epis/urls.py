from django.urls import path
from . import views

app_name = 'epis'

urlpatterns = [
    # Listagem de equipamentos -> /epis/
    path('', views.listar_equipamentos, name='listar'),

    # Cadastro -> /epis/cadastrar/
    path('cadastrar/', views.cadastrar_equipamento, name='cadastrar'),

    # Edição -> /epis/1/editar/
    path('<int:id>/editar/', views.editar_equipamento, name='editar'),

    # Exclusão -> /epis/1/excluir/
    path('<int:id>/excluir/', views.excluir_equipamento, name='excluir'),

    # Ativar/Inativar status -> /epis/1/status/
    path('<int:id>/status/', views.alternar_status_equipamento, name='alternar_status'),
]