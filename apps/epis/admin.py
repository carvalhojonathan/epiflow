from django.contrib import admin
from .models import Equipamento

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ca_numero', 'validade_ca', 'saldo_estoque', 'ativo')
    search_fields = ('nome', 'ca_numero')
    list_filter = ('ativo',)

