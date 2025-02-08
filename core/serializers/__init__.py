from .user import UserSerializer
from .categoria import CategoriaSerializer
from .editora import EditoraSerializer
from .autor import AutorSerializer
from .livro import (
    LivroAlterarPrecoSerializer,
    LivroListSerializer,
    LivroAjustarEstoqueSerializer,
    LivroRetrieveSerializer,
    LivroSerializer,
    LivroAjustarEstoqueSerializer
)
from .livro import (
    LivroAlterarPrecoSerializer,
    LivroListSerializer,
    LivroRetrieveSerializer,
    LivroSerializer,
)
from .compra import CompraSerializer, CompraCreateUpdateSerializer, ItensCompraSerializer, ItensCompraCreateUpdateSerializer, CompraListSerializer, ItensCompraListSerializer