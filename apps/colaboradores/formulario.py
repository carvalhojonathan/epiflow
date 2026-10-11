import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Colaborador

# Preposições que devem permanecer em minúsculas
PREPOSICOES = {'de', 'da', 'do', 'das', 'dos', 'e', 'em'}


def formatar_titulo(texto):
    """
    Capitaliza cada palavra mantendo preposições em minúsculas.
    Ex: 'joão DA silva' -> 'João da Silva'
    """
    palavras = texto.split()
    palavras_formatadas = []
    for i, palavra in enumerate(palavras):
        palavra_lower = palavra.lower()
        if i > 0 and palavra_lower in PREPOSICOES:
            palavras_formatadas.append(palavra_lower)
        else:
            # Capitaliza preservando possíveis hífens internos (ex: Jean-Luc)
            partes_hifen = palavra_lower.split('-')
            partes_capitalizadas = [p.capitalize() for p in partes_hifen]
            palavras_formatadas.append('-'.join(partes_capitalizadas))
    return ' '.join(palavras_formatadas)


def validar_cpf_matematico(cpf_numeros):
    """Valida os dígitos verificadores do CPF."""
    if len(cpf_numeros) != 11 or cpf_numeros == cpf_numeros[0] * 11:
        return False

    # Primeiro dígito verificador
    soma = sum(int(cpf_numeros[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito1 = 0 if resto == 10 else resto
    if digito1 != int(cpf_numeros[9]):
        return False

    # Segundo dígito verificador
    soma = sum(int(cpf_numeros[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito2 = 0 if resto == 10 else resto
    if digito2 != int(cpf_numeros[10]):
        return False

    return True


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
                'maxlength': '100',
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'maxlength': '14',
            }),
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'F00000',
                'maxlength': '6',
            }), 
            'funcao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Operador Têxtil',
                'maxlength': '50',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
                'maxlength': '15',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'colaborador@empresa.com',
                'maxlength': '60',
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    # 1. VALIDAÇÃO DO NOME COMPLETO
    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()

        # Remove múltiplos espaços internos
        nome = re.sub(r'\s+', ' ', nome)

        if len(nome) > 100:
            raise ValidationError('O nome completo deve ter no máximo 100 caracteres.')

        # Permite letras (com acentos), apóstrofo, hífen, ponto e espaço
        padrao = r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'\-\.]+$"
        if not re.match(padrao, nome):
            raise ValidationError('O nome deve conter apenas letras, apóstrofo, hífen e ponto. Números e outros símbolos não são permitidos.')

        palavras = nome.split()
        if len(palavras) < 2:
            raise ValidationError('Informe o nome completo (no mínimo nome e sobrenome).')

        for palavra in palavras:
            letras_apenas = re.sub(r"['\-\.]", "", palavra)
            if len(letras_apenas) < 2:
                raise ValidationError(f'A palavra "{palavra}" é muito curta. Cada palavra deve ter no mínimo 2 letras.')

        return formatar_titulo(nome)

    # 2. VALIDAÇÃO DO CPF
    def clean_cpf(self):
        cpf_bruto = self.cleaned_data.get('cpf', '').strip()
        # Extrai apenas números
        cpf_numeros = re.sub(r'\D', '', cpf_bruto)

        if len(cpf_numeros) != 11:
            raise ValidationError('O CPF deve conter exatamente 11 dígitos numéricos.')

        if not validar_cpf_matematico(cpf_numeros):
            raise ValidationError('CPF inválido. Os dígitos verificadores não conferem.')

        # Formata para padrão: 000.000.000-00
        cpf_formatado = f'{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}'

        # Unicidade (ignora o próprio colaborador na edição)
        consulta = Colaborador.objects.filter(cpf=cpf_formatado)
        if self.instance.pk:
            consulta = consulta.exclude(pk=self.instance.pk)

        if consulta.exists():
            raise ValidationError('Já existe um colaborador cadastrado com este CPF.')

        return cpf_formatado

    # 3. VALIDAÇÃO DA MATRÍCULA (Obrigatório começar com 'F' + 5 números)
    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula', '').strip().upper()

        # Valida se começa com F maiúsculo seguido de exatamente 5 dígitos
        padrao = r'^F\d{5}$'
        if not re.match(padrao, matricula):
            raise ValidationError("A matrícula deve começar com a letra 'F' seguida de 5 números (ex: F12345).")

        # Unicidade (ignora o próprio colaborador na edição)
        consulta = Colaborador.objects.filter(matricula=matricula)
        if self.instance.pk:
            consulta = consulta.exclude(pk=self.instance.pk)

        if consulta.exists():
            raise ValidationError('Esta matrícula já está em uso por outro colaborador.')

        return matricula

    # 4. VALIDAÇÃO DA FUNÇÃO / CARGO
    def clean_funcao(self):
        funcao = self.cleaned_data.get('funcao', '').strip()
        funcao = re.sub(r'\s+', ' ', funcao)

        if not funcao:
            raise ValidationError('A função/cargo é obrigatória.')

        if len(funcao) > 50:
            raise ValidationError('A função/cargo deve ter no máximo 50 caracteres.')

        padrao = r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'\-\.]+$"
        if not re.match(padrao, funcao):
            raise ValidationError('A função/cargo deve conter apenas letras, apóstrofo, hífen e ponto. Números não são permitidos.')

        palavras = funcao.split()
        for palavra in palavras:
            letras_apenas = re.sub(r"['\-\.]", "", palavra)
            if len(letras_apenas) < 2:
                raise ValidationError(f'A palavra "{palavra}" é muito curta. Cada palavra deve ter no mínimo 2 letras.')

        return formatar_titulo(funcao)


    # 5. VALIDAÇÃO DO TELEFONE
    def clean_telefone(self):
        telefone_bruto = self.cleaned_data.get('telefone', '').strip()
        tel_numeros = re.sub(r'\D', '', telefone_bruto)

        if len(tel_numeros) != 11:
            raise ValidationError('O telefone deve conter exatamente 11 números com DDD (ex: 71988887777).')

        # Formata para (00) 00000-0000
        return f'({tel_numeros[:2]}) {tel_numeros[2:7]}-{tel_numeros[7:]}'

    # 6. VALIDAÇÃO DO EMAIL
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError('O campo e-mail é obrigatório.')

        padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(padrao_email, email):
            raise ValidationError('Informe um endereço de e-mail válido (ex: colaborador@empresa.com).')

        return email
