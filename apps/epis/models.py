from django.db import models


class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    ca_numero = models.CharField(max_length=30)
    validade_ca = models.DateField()
    saldo_estoque = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=5)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    @property
    def ca_vencido(self):
        """Retorna True se o CA já expirou em relação à data atual."""
        from django.utils import timezone
        if self.validade_ca:
            return self.validade_ca < timezone.now().date()
        return False
