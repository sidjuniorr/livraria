from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated  # Importe AllowAny
from core.serializers import (
    LivroListSerializer,
    LivroSerializer,
    LivroRetrieveSerializer,
    LivroAlterarPrecoSerializer,
    LivroAjustarEstoqueSerializer,
)
from django.db.models.aggregates import Sum
from core.models import Livro, Favorito  # Importe o modelo Favorito
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["categoria__descricao", "editora__nome"]
    search_fields = ["titulo"]
    ordering_fields = ["titulo", "preco"]
    ordering = ["titulo"]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'mais_vendidos':  # Ação 'list' e 'mais_vendidos' permite acesso anônimo
            permission_classes = [AllowAny]
        else:  # Outras ações exigem autenticação
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return LivroListSerializer
        elif self.action == "retrieve":
            return LivroRetrieveSerializer
        return LivroSerializer

    @action(detail=True, methods=["patch"])
    def alterar_preco(self, request, pk=None):
        livro = self.get_object()

        serializer = LivroAlterarPrecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        livro.preco = serializer.validated_data["preco"]
        livro.save()

        return Response(
            {"detail": f"Preço do livro '{livro.titulo}' atualizado para {livro.preco}."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def ajustar_estoque(self, request, pk=None):
        livro = self.get_object()

        serializer = LivroAjustarEstoqueSerializer(data=request.data, context={"livro": livro})
        serializer.is_valid(raise_exception=True)

        quantidade_ajuste = serializer.validated_data["quantidade"]

        livro.quantidade += quantidade_ajuste
        livro.save()

        return Response(
            {"status": "Quantidade ajustada com sucesso", "novo_estoque": livro.quantidade},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def mais_vendidos(self, request):
        livros = Livro.objects.annotate(total_vendidos=Sum("itenscompra__quantidade")).filter(total_vendidos__gt=10)

        data = [
            {
                "id": livro.id,
                "titulo": livro.titulo,
                "total_vendidos": livro.total_vendidos,
            }
            for livro in livros
        ]

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def favoritar(self, request, pk=None):
        livro = self.get_object()
        usuario = request.user  # Obtenha o usuário da requisição

        # Verifica se já existe um registro de Favorito para este livro e usuário
        favorito_existente = Favorito.objects.filter(usuario=usuario, livro=livro).exists()

        livro.favorito = request.data.get('favorito', not livro.favorito)  # Toggle or set
        livro.save()

        if livro.favorito:  # Se o livro foi marcado como favorito
            if not favorito_existente:  # E não existe um registro de Favorito
                Favorito.objects.create(usuario=usuario, livro=livro)  # Crie um registro de Favorito
        else:  # Se o livro foi desmarcado como favorito
            if favorito_existente:  # E existe um registro de favorito
                Favorito.objects.filter(usuario=usuario, livro=livro).delete()  # Remova o registro de Favorito

        serializer = self.get_serializer(livro)  # Use the appropriate serializer
        return Response(serializer.data)