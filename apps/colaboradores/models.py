from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    matricula = models.CharField(max_length=10)
    funcao = models.CharField(max_length=30)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=60)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome
