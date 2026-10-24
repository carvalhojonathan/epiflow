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
        'exibir_ca_vencido_em_uso',
    )
    search_fields = (
        'colaborador__nome',
        'colaborador__matricula',
        'equipamento__nome',
        'equipamento__ca_numero',
        'status',
    )
    list_filter = ('status', 'data_emprestimo')

    @admin.display(boolean=True, description='CA Vencido em Uso?')
    def exibir_ca_vencido_em_uso(self, obj):
        return obj.ca_vencido_em_uso
