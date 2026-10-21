from django.contrib import admin
from .models import Emprestimo

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = (
        'colaborador',
        'equipamento',
        'data_emprestimo',
        'data_devolucao_prevista',
        'data_devolucao_real',
        'status',
    )
    search_fields = (
        'colaborador__nome',
        'colaborador__matricula',
        'equipamento__nome',
        'equipamento__ca_numero',
        'status',
    )
    list_filter = ('status', 'data_emprestimo')