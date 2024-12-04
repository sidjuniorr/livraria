from rest_framework.viewsets import ModelViewSet

from core.models import Compra
from core.serializers import CompraSerializer, CompraCreateUpdateSerializer, CompraListSerializer


class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CompraListSerializer  # Usar o serializador para listagem
        if self.action in ("create", "update"):
            return CompraCreateUpdateSerializer  # Usar o serializador para criação e atualização
        return CompraSerializer  # Usar o serializador padrão para outras ações (detalhamento)
