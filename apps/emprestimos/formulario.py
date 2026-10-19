from django import forms
from django.utils import timezone
from .models import Emprestimo


class EmprestimoForm(forms.ModelForm):
    """
    Formulário de CRIAÇÃO de empréstimo/fornecimento.
    - Status como campo select.
    - Colaborador e Equipamento com ordenação alfabética.
    """
    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'equipamento', 'status', 'data_emprestimo', 'data_devolucao_prevista']
        widgets = {
            'colaborador': forms.Select(attrs={
                'class': 'form-select',
            }),
            'equipamento': forms.Select(attrs={
                'class': 'form-select',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'data_emprestimo': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'data_devolucao_prevista': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hoje = timezone.now().date()

        # Ordem alfabética
        self.fields['colaborador'].label_from_instance = lambda obj: (
            f"{obj.nome} ({obj.matricula})"
            if obj.matricula
            else obj.nome
        )
        self.fields['equipamento'].queryset = self.fields['equipamento'].queryset.order_by('nome')

        # Aviso visual de CA no Equipamento (sem bloquear o cadastro)
        self.fields['equipamento'].label_from_instance = lambda obj: (
            f"{obj.nome} (CA: {obj.ca_numero}) — ⚠️ CA Vencido em {obj.validade_ca.strftime('%d/%m/%Y')}"
            if obj.validade_ca and obj.validade_ca < hoje
            else f"{obj.nome} (CA: {obj.ca_numero})"
        )

        self.fields['colaborador'].empty_label = ""
        self.fields['equipamento'].empty_label = ""
        
        # Apenas Emprestado e Fornecido na criação
        self.fields['status'].choices = [
            ('Emprestado', 'Emprestado'),
            ('Fornecido', 'Fornecido'),
        ]
        self.fields['data_devolucao_prevista'].required = False
        
        # Data de empréstimo padrão como data de hoje
        if not self.instance.pk and not self.initial.get('data_emprestimo'):
            self.initial['data_emprestimo'] = hoje
            self.initial['status'] = 'Emprestado'

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        data_prevista = cleaned_data.get('data_devolucao_prevista')

        if status == 'Emprestado':
            if not data_prevista:
                self.add_error('data_devolucao_prevista', 'Informe a data prevista de devolução para itens emprestados.')
            elif data_prevista <= timezone.now().date():
                self.add_error('data_devolucao_prevista', 'A data prevista para devolução deve ser posterior à data atual.')
        elif status == 'Fornecido':
            cleaned_data['data_devolucao_prevista'] = None

        return cleaned_data


class EmprestimoEdicaoForm(forms.ModelForm):
    """
    Formulário de EDIÇÃO / BAIXA.
    Apenas os campos editáveis: status, data de devolução e observação.
    """
    class Meta:
        model = Emprestimo
        fields = ['status', 'data_devolucao_real', 'observacao']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'data_devolucao_real': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva observações da devolução ou motivo de dano/perda...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [
            ('--- Em aberto ---', [
                ('Emprestado', 'Emprestado'),
                ('Fornecido', 'Fornecido'),
            ]),
            ('--- Baixa ---', [
                ('Devolvido', 'Devolvido'),
                ('Danificado', 'Danificado'),
                ('Perdido', 'Perdido'),
            ]),
        ]
        # Se não houver data de devolução preenchida, sugere a de hoje por padrão
        if not self.instance.data_devolucao_real:
            self.initial['data_devolucao_real'] = timezone.now().date()