from django.contrib import admin
from .models import Colaborador

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'cpf', 'funcao', 'ativo')
    search_fields = ('nome', 'cpf', 'matricula')
    list_filter = ('ativo', 'funcao')
