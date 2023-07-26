# models.py

from django.db import models


class Categoria(models.Model):
    NOME = (
        ('RC', 'Receitas'),
        ('GF', 'Gastos Fixos'),
        ('GV', 'Gastos Variáveis'),
        ('I', 'Investimentos'),
    )
    nome = models.CharField(max_length=2, choices=NOME)

    def __str__(self):
        return f'{self.nome}'

class Subcategoria(models.Model):
    nome = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome} - {self.categoria}'

class Transacao(models.Model):
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    data = models.DateField()
    montante = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.subcategoria.categoria.nome} - {self.subcategoria.nome} - {self.montante} - {self.data}'
