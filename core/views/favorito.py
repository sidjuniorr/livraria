from rest_framework import generics
from core.models import Favorito
from core.serializers import FavoritoSerializer
from rest_framework.permissions import IsAuthenticated

class FavoritoViewSet(generics.ListAPIView):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        return Favorito.objects.filter(usuario=usuario)