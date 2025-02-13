from django.contrib import admin
from django.urls import include, path
from uploader.router import router as uploader_router
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import UserViewSet, CategoriaViewSet, EditoraViewSet, AutorViewSet, LivroViewSet, CompraViewSet, FavoritoViewSet  # Importe FavoritoViewSet
from core.serializers import FavoritoSerializer # Importe o serializer

router = DefaultRouter()
router.register(r"livros", LivroViewSet, basename="livro")  # Adicione o basename
router.register(r"categorias", CategoriaViewSet, basename="categoria")  # Adicione o basename
router.register(r"editoras", EditoraViewSet, basename="editora")  # Adicione o basename
router.register(r"autores", AutorViewSet, basename="autor")  # Adicione o basename
router.register(r"compras", CompraViewSet, basename="compra")  # Adicione o basename
router.register(r"usuarios", UserViewSet, basename="usuario")  # Use singular para o basename
# Não Registre o FavoritoViewSet aqui

urlpatterns = [
    path("admin/", admin.site.urls),
    # OpenAPI 3
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/media/", include(uploader_router.urls)),

    # Swagger UI
    path("api/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Simple JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # API
    path("api/", include(router.urls)),  # Inclua as URLs do router aqui
    path('api/favoritos/', FavoritoViewSet.as_view(), name='favoritos-usuario'),  # Rota direta para FavoritoViewSet
]

urlpatterns += static(settings.MEDIA_ENDPOINT, document_root=settings.MEDIA_ROOT)