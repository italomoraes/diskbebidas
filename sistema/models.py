from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Produto(models.Model):
    codigo_de_barras = models.CharField(max_length=13, unique=True)
    descricao = models.CharField(max_length=200)
    valor_de_venda = models.DecimalField(validators=[MinValueValidator(0)],max_digits=7, decimal_places=2)
    valor_de_compra = models.DecimalField(validators=[MinValueValidator(0)],max_digits=7, decimal_places=2)
    quantidade_em_estoque = models.IntegerField(validators=[MinValueValidator(0)])

class Pack(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_do_pack = models.IntegerField(validators=[MinValueValidator(1,"Digite um valor maior que 1")])

class Venda(models.Model):
    FORMAS_DE_PAGAMENTO = [('CR', 'Crédito'), ('DE','Débito'), ('DI','Dinheiro')]
    data_e_hora = models.DateTimeField(auto_now=True)
    valor_total = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
    forma_de_pagamento = models.CharField(max_length=2, choices=FORMAS_DE_PAGAMENTO)

class ProdutoVendido(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    codigo_de_barras = models.CharField(max_length=13)
    descricao = models.CharField(max_length=200)
    valor_de_venda = models.DecimalField(validators=[MinValueValidator(0)],max_digits=7, decimal_places=2)
    valor_de_compra = models.DecimalField(validators=[MinValueValidator(0)],max_digits=7, decimal_places=2)
    quantidade_vendida = models.IntegerField(validators=[MinValueValidator(0)])
