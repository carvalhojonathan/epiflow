from django import forms
from .models import Colaborador

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'cpf', 'matricula', 'funcao', 'telefone', 'email', 'ativo']
        
        labels = {
            'nome': 'Nome Completo',
            'cpf': 'CPF',
            'matricula': 'Matrícula',
            'funcao': 'Função / Cargo',
            'telefone': 'Telefone',
            'email': 'E-mail',
            'ativo': 'Colaborador Ativo',
        }
        
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo',
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
            }),
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 12345',
            }),
            'funcao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Operador Têxtil',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'colaborador@empresa.com',
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
