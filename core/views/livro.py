from rest_framework.viewsets import ModelViewSet
from core.serializers import LivroListSerializer, LivroSerializer, LivroRetrieveSerializer

from core.models import Livro
from core.serializers import LivroSerializer


class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return LivroListSerializer
        elif self.action == "retrieve":
            return LivroRetrieveSerializer
        return LivroSerializer