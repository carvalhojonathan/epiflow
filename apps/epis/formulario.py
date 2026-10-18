from django import forms
from .models import Equipamento

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'ca_numero', 'validade_ca', 'saldo_estoque', 'estoque_minimo', 'ativo']
        labels = {
            'nome': 'Nome do EPI',
            'ca_numero': 'Nº do CA (Certificado de Aprovação)',
            'validade_ca': 'Validade do CA',
            'saldo_estoque': 'Saldo em Estoque',
            'estoque_minimo': 'Estoque Mínimo',
            'ativo': 'Equipamento Ativo',
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Óculos de Proteção',
                'maxlength': '100',
            }),
            'ca_numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 12345',
                'maxlength': '30',
            }),
            'validade_ca': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'saldo_estoque': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0',
            }),
            'estoque_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '5',
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }