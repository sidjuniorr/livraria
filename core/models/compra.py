from django.db import models
from .livro import Livro
from .user import User

class Compra(models.Model):
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, "Carrinho"
        FINALIZADO = 2, "Realizado"
        PAGO = 3, "Pago"
        ENTREGUE = 4, "Entregue"
    
    class TipoPagamento(models.IntegerChoices):
        CARTAO_CREDITO = 1, "Cartão de Crédito"
        CARTAO_DEBITO = 2, "Cartão de Débito"
        PIX = 3, "PIX"
        BOLETO = 4, "Boleto"
        TRANSFERENCIA_BANCARIA = 5, "Transferência Bancária"
        DINHEIRO = 6, "Dinheiro"
        OUTRO = 7, "Outro"

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="compras")
    status = models.IntegerField(choices=StatusCompra.choices,  default=StatusCompra.CARRINHO)
    tipo_pagamento = models.IntegerField(choices=TipoPagamento.choices, default=TipoPagamento.CARTAO_CREDITO)
    data = models.DateTimeField(auto_now_add=True)
    @property
    def total(self):
            # total = 0
            # for item in self.itens.all():
            #     total += item.livro.preco * item.quantidade
            # return total
            return sum(item.livro.preco * item.quantidade for item in self.itens.all())

class ItensCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="itens")
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="itens_compra")
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade = models.IntegerField(default=1)
    @property
    def total(self):
            # total = 0
            # for item in self.itens.all():
            #     total += item.livro.preco * item.quantidade
            # return total
            return sum(item.preco * item.quantidade for item in self.itens.all())