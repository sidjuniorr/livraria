from rest_framework.serializers import ModelSerializer, CharField
from core.models import Compra, ItensCompra
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade

    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total")
        depth = 1


class CompraSerializer(ModelSerializer):
    """Serializer para compras com itens detalhados."""
    status = CharField(source="get_status_display", read_only=True)  # Exibe o nome do status
    usuario = CharField(source="usuario.email", read_only=True)  # Exibe o email do usuário
    itens = ItensCompraSerializer(many=True, read_only=True)  # Inclui os itens da compra
    fields = ("id", "usuario", "status", "total", "itens")

    class Meta:
        model = Compra
        fields = "__all__"  # Inclui todos os campos do modelo Compra
    @property
    def total(self):
        # total = 0
        # for item in self.itens.all():
        #     total += item.livro.preco * item.quantidade
        # return total
        return sum(item.livro.preco * item.quantidade for item in self.itens.all())
