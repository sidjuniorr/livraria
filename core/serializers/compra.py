from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from core.models import Compra, ItensCompra
from rest_framework.serializers import (
    CharField,
    CurrentUserDefault, # novo
    DateTimeField, # novo
    HiddenField, # novo
    ModelSerializer,
    SerializerMethodField,
    ValidationError, # novo
)


class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source="livro.titulo", read_only=True)  # Exibe o título do livro
    quantidade = CharField(read_only=True)  # Exibe a quantidade do item

    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")  # Exibe título do livro e quantidade


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    def get_total(self, instance):
        return instance.livro.preco * instance.quantidade

    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total")
        depth = 1


class CompraListSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email", read_only=True)  # Exibe o e-mail do usuário
    itens = ItensCompraListSerializer(many=True, read_only=True)  # Listagem dos itens de compra

    class Meta:
        model = Compra
        fields = ("id", "usuario", "itens")  # Campos para a listagem


class CompraSerializer(ModelSerializer):
    """Serializer para compras com itens detalhados."""
    status = CharField(source="get_status_display", read_only=True)  # Exibe o nome do status
    data = DateTimeField(read_only=True) # novo campo
    usuario = CharField(source="usuario.email", read_only=True)  # Exibe o email do usuário
    itens = ItensCompraSerializer(many=True, read_only=True)  # Inclui os itens da compra

    class Meta:
        model = Compra
        fields = ("id", "usuario", "status", "total", "data", "itens") # modificado

    @property
    def total(self):
        return sum(item.livro.preco * item.quantidade for item in self.instance.itens.all())


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")
        
    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError("A quantidade deve ser maior do que zero.")
        return quantidade
    
    def validate(self, item):
        if item["quantidade"] > item["livro"].quantidade:
            raise ValidationError("Quantidade de itens maior do que a quantidade em estoque.")
        return item


class CompraCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = ItensCompraCreateUpdateSerializer(many=True)

    class Meta:
        model = Compra
        fields = ("usuario", "itens")

    def create(self, validated_data):
        itens = validated_data.pop("itens")
        compra = Compra.objects.create(**validated_data)
        for item in itens:
            item["preco"] = item["livro"].preco # nova linha
            ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return compra

    def update(self, compra, validated_data):
        itens = validated_data.pop("itens")
        if itens:
            compra.itens.all().delete()
            for item in itens:
                item["preco"] = item["livro"].preco  # nova linha
                ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return super().update(compra, validated_data)
    
class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source="livro.titulo", read_only=True)

    class Meta:
        model = ItensCompra
        fields = ("quantidade", "livro")
        depth = 1
