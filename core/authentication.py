from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from core.models import User

# Desativar temporariamente o uso de Passage
# from passageidentity import Passage, PassageError
# psg = Passage(settings.PASSAGE_APP_ID, settings.PASSAGE_API_KEY, auth_strategy=settings.PASSAGE_AUTH_STRATEGY)


class TokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "core.authentication.TokenAuthentication"
    name = "tokenAuth"
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name="Authorization",
            token_prefix="Bearer",
        )


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request) -> tuple[User, None]:
        if not request.headers.get("Authorization"):
            return None

        token = request.headers.get("Authorization").split()[1]
        # Simulando uma validação de token simples
        psg_user_id: str = self._get_user_id(token)
        user: User = self._get_or_create_user(psg_user_id)

        return (user, None)

    def _get_or_create_user(self, psg_user_id) -> User:
        try:
            user: User = User.objects.get(passage_id=psg_user_id)
        except ObjectDoesNotExist:
            # Simular um usuário fictício para desenvolvimento
            user: User = User.objects.create_user(
                passage_id=psg_user_id,
                email=f"user{psg_user_id}@example.com",
            )

        return user

    def _get_user_id(self, token) -> str:
        # Simulando validação de token
        try:
            # Aqui, estamos apenas retornando o token como ID para testes
            psg_user_id = token  # Substitua pela lógica apropriada quando Passage for ativado
        except Exception as e:
            raise AuthenticationFailed("Invalid token") from e

        return psg_user_id
