from django.contrib import admin
from .models import Equipamento


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'ca_numero',
        'validade_ca',
        'saldo_estoque',
        'estoque_minimo',
        'exibir_ca_vencido',
        'ativo',
    )
    search_fields = ('nome', 'ca_numero')
    list_filter = ('ativo',)

    @admin.display(boolean=True, description='CA Vencido?')
    def exibir_ca_vencido(self, obj):
        return obj.ca_vencido
