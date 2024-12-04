from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from core.models import Compra, ItensCompra


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

    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "total", "itens")


    @property
    def total(self):
        return sum(item.livro.preco * item.quantidade for item in self.instance.itens.all())


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")


class CompraCreateUpdateSerializer(ModelSerializer):
    itens = ItensCompraCreateUpdateSerializer(many=True)

    class Meta:
        model = Compra
        fields = ("usuario", "itens")

    def create(self, validated_data):
        itens_data = validated_data.pop("itens")
        compra = Compra.objects.create(**validated_data)
        for item_data in itens_data:
            ItensCompra.objects.create(compra=compra, **item_data)
        return compra

    def update(self, compra, validated_data):
        itens_data = validated_data.pop("itens")
        if itens_data:
            compra.itens.all().delete()
            for item_data in itens_data:
                ItensCompra.objects.create(compra=compra, **item_data)
        return super().update(compra, validated_data)
