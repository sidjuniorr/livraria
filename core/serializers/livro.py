from rest_framework import serializers
from ..models import Livro  # Correct relative import
from uploader.models import Image
from uploader.serializers import ImageSerializer

class LivroSerializer(serializers.ModelSerializer):  # Use serializers.ModelSerializer
    favorito = serializers.BooleanField(required=False)  # Use serializers.BooleanField

    class Meta:
        model = Livro
        fields = "__all__"
        depth = 1

    capa_attachment_key = serializers.SlugRelatedField(  # Use serializers.SlugRelatedField
        source="capa",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
        write_only=True,
    )
    capa = ImageSerializer(
        required=False,
        read_only=True
    )

class LivroAlterarPrecoSerializer(serializers.Serializer):  # Use serializers.Serializer
    preco = serializers.DecimalField(max_digits=10, decimal_places=2)  # Use serializers.DecimalField

    def validate_preco(self, value):
        """Valida se o preço é um valor positivo."""
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser um valor positivo.")  # Use serializers.ValidationError
        return value

class LivroAjustarEstoqueSerializer(serializers.Serializer): # Use serializers.Serializer
    quantidade = serializers.IntegerField()  # Use serializers.IntegerField

    def validate_quantidade(self, value):
        livro = self.context.get("livro")
        if livro:
            nova_quantidade = livro.quantidade + value
            if nova_quantidade < 0:
                raise serializers.ValidationError("A quantidade em estoque não pode ser negativa.") # Use serializers.ValidationError
        return value

class LivroListSerializer(serializers.ModelSerializer): # Use serializers.ModelSerializer
    favorito = serializers.BooleanField(read_only=True)  # Use serializers.BooleanField

    class Meta:
        model = Livro
        fields = ("id", "titulo", "preco", "favorito")
        depth = 1

class LivroRetrieveSerializer(serializers.ModelSerializer): # Use serializers.ModelSerializer
    favorito = serializers.BooleanField(read_only=True)  # Use serializers.BooleanField

    class Meta:
        model = Livro
        fields = "__all__"
        depth = 1