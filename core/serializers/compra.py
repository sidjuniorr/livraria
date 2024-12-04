from rest_framework.serializers import ModelSerializer, CharField
from core.models import Compra, ItensCompra


class ItensCompraSerializer(ModelSerializer):
    """Serializer para itens da compra."""
    class Meta:
        model = ItensCompra
        fields = "__all__"  # Inclui todos os campos do modelo ItensCompra


class CompraSerializer(ModelSerializer):
    """Serializer para compras com itens detalhados."""
    status = CharField(source="get_status_display", read_only=True)  # Exibe o nome do status
    usuario = CharField(source="usuario.email", read_only=True)  # Exibe o email do usuário
    itens = ItensCompraSerializer(many=True, read_only=True)  # Inclui os itens da compra

    class Meta:
        model = Compra
        fields = "__all__"  # Inclui todos os campos do modelo Compra
