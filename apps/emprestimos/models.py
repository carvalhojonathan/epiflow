from django.db import models
from apps.colaboradores.models import Colaborador
from apps.epis.models import Equipamento


class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('Emprestado', 'Emprestado'),
        ('Fornecido', 'Fornecido'),
        ('Devolvido', 'Devolvido'),
        ('Danificado', 'Danificado'),
        ('Perdido', 'Perdido'),
    ]

    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.PROTECT,
        related_name='emprestimos',
        verbose_name='Colaborador',
    )
    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.PROTECT,
        related_name='emprestimos',
        verbose_name='Equipamento',
    )
    data_emprestimo = models.DateField(verbose_name='Data do Empréstimo')
    data_devolucao_prevista = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data Prevista de Devolução'
    )
    data_devolucao_real = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data da Devolução',
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Emprestado',
        verbose_name='Status',
    )
    observacao = models.TextField(
        blank=True,
        default='',
        verbose_name='Observação na Devolução',
    )

    class Meta:
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
        ordering = ['-id']

    def __str__(self):
        return f'{self.colaborador.nome} — {self.equipamento.nome} ({self.status})'

    @property
    def ca_vencido_em_uso(self):
        """
        Retorna True se o empréstimo estiver com status 'Emprestado'
        e a data de validade do CA do equipamento já tiver expirado.
        """
        from django.utils import timezone
        if self.status == 'Emprestado' and self.equipamento and self.equipamento.validade_ca:
            return self.equipamento.validade_ca < timezone.now().date()
        return False