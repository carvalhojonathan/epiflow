import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
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
                'inputmode': 'numeric',
                'oninput': "this.value = this.value.replace(/\\D/g, '')",
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

    # 1. VALIDAÇÃO DO NOME DO EPI (no mínimo 2 letras)
    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        nome = re.sub(r'\s+', ' ', nome)

        # Conta apenas caracteres que são letras (suporta acentos: ç, á, õ, etc.)
        letras = re.findall(r'[a-zA-ZÀ-ÿ]', nome)
        if len(letras) < 2:
            raise ValidationError('O nome do EPI deve conter no mínimo 2 letras.')

        return nome

    # 2. VALIDAÇÃO DO Nº DO CA (apenas números)
    def clean_ca_numero(self):
        ca_numero = self.cleaned_data.get('ca_numero', '').strip()

        if not ca_numero:
            raise ValidationError('O número do CA é obrigatório.')

        if not ca_numero.isdigit():
            raise ValidationError('O número do CA deve conter apenas números.')

        return ca_numero

    # 3. VALIDAÇÃO DA VALIDADE DO CA (maior que a data atual)
    def clean_validade_ca(self):
        validade_ca = self.cleaned_data.get('validade_ca')

        if validade_ca:
            hoje = timezone.localdate()
            if validade_ca <= hoje:
                raise ValidationError('A validade do CA deve ser maior que a data atual.')

        return validade_ca

    # 4. VALIDAÇÃO DO SALDO EM ESTOQUE (maior que o estoque mínimo)
    def clean(self):
        cleaned_data = super().clean()
        saldo_estoque = cleaned_data.get('saldo_estoque')
        estoque_minimo = cleaned_data.get('estoque_minimo')

        if saldo_estoque is not None and estoque_minimo is not None:
            if saldo_estoque <= estoque_minimo:
                self.add_error(
                    'saldo_estoque',
                    'O saldo em estoque deve ser maior que o estoque mínimo.'
                )

        return cleaned_data
