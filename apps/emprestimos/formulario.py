from django import forms
from django.utils import timezone
from .models import Emprestimo


class EmprestimoForm(forms.ModelForm):
    """
    Formulário de CRIAÇÃO de empréstimo/fornecimento.
    - Valida saldo em estoque (bloqueia se saldo <= 0).
    - Valida validade do CA (bloqueia se CA vencido).
    - Exibe saldo atual, estoque mínimo e status do CA nas opções do select.
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

        # Identificação amigável do Colaborador
        self.fields['colaborador'].label_from_instance = lambda obj: (
            f"{obj.nome} ({obj.matricula})"
            if obj.matricula
            else obj.nome
        )
        
        # Filtra apenas equipamentos ativos e ordenados por nome
        self.fields['equipamento'].queryset = self.fields['equipamento'].queryset.filter(ativo=True).order_by('nome')

        # Exibição rica do Equipamento com Saldo, Estoque Mínimo e Validade do CA
        def rotulo_equipamento(obj):
            partes = [f"{obj.nome} (CA: {obj.ca_numero})"]

            # Alerta de CA vencido
            if obj.validade_ca and obj.validade_ca < hoje:
                partes.append(f"⚠️ CA Vencido em {obj.validade_ca.strftime('%d/%m/%Y')}")

            # Alerta de Estoque
            if obj.saldo_estoque <= 0:
                partes.append("⚠️ Sem Estoque (0 un.)")
            elif obj.saldo_estoque <= obj.estoque_minimo:
                partes.append(f"⚠️ Estoque Baixo (Restam {obj.saldo_estoque} | Mínimo: {obj.estoque_minimo})")
            else:
                partes.append(f"Saldo: {obj.saldo_estoque} un.")

            return " — ".join(partes)

        self.fields['equipamento'].label_from_instance = rotulo_equipamento

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
        equipamento = cleaned_data.get('equipamento')
        status = cleaned_data.get('status')
        data_prevista = cleaned_data.get('data_devolucao_prevista')
        hoje = timezone.now().date()

        # 1. Validação de CA do Equipamento
        if equipamento and equipamento.validade_ca and equipamento.validade_ca < hoje:
            self.add_error(
                'equipamento',
                f"Não é permitido realizar empréstimo/fornecimento de EPI com CA vencido. "
                f"O CA nº {equipamento.ca_numero} venceu em {equipamento.validade_ca.strftime('%d/%m/%Y')}."
            )

        # 2. Validação de Saldo de Estoque (bloqueia apenas se estoque físico for zero)
        if equipamento and equipamento.saldo_estoque <= 0:
            self.add_error(
                'equipamento',
                f"Saldo insuficiente no estoque! O equipamento '{equipamento.nome}' possui saldo atual de 0 unidades."
            )

        # 3. Validação de Data Prevista para Itens Emprestados
        if status == 'Emprestado':
            if not data_prevista:
                self.add_error('data_devolucao_prevista', 'Informe a data prevista de devolução para itens emprestados.')
            elif data_prevista <= hoje:
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
