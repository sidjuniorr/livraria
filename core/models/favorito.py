from django.db import models
from django.conf import settings
from .livro import Livro  # Importe o modelo Livro

class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='favoritos')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'livro')  # Impede que um usuário favorite o mesmo livro várias vezes

    def __str__(self):
        return f'{self.usuario.name} favoritou {self.livro.titulo}'