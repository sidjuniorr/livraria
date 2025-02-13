"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Autor, Categoria, Compra, Editora, ItensCompra, Livro, User, Favorito # Importe Favorito


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name", "foto", "tipo_usuario", "passage_id")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
        (_("Groups"), {"fields": ("groups",)}),
        (_("User Permissions"), {"fields": ("user_permissions",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nome", "email")
    search_fields = ("nome", "email")
    list_filter = ("nome",)
    ordering = ("nome", "email")


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("descricao",)
    search_fields = ("descricao",)
    list_filter = ("descricao",)
    ordering = ("descricao",)


@admin.register(Editora)
class EditoraAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)
    list_filter = ("nome",)
    ordering = ("nome",)


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "editora", "categoria", "favorito")  # Adicione "favorito" aqui
    search_fields = ("titulo", "editora__nome", "categoria__descricao")
    list_filter = ("editora", "categoria", "favorito")  # Adicione "favorito" aqui
    ordering = ("titulo", "editora", "categoria")
    list_per_page = 25


class ItensCompraInline(admin.StackedInline):  # Ou use TabularInline
    model = ItensCompra
    extra = 1  # Quantidade de itens adicionais


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "status", "total")
    readonly_fields = ("data",)
    search_fields = ("usuario", "status")
    list_filter = ("usuario", "status")
    ordering = ("status", "usuario", "data", "total")
    list_per_page = 25
    inlines = [ItensCompraInline]
    
admin.site.register(Favorito) # Registre Favorito