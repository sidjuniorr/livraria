from .user import UserSerializer
from .categoria import CategoriaSerializer
from .editora import EditoraSerializer
from .autor import AutorSerializer
from .livro import LivroListSerializer, LivroSerializer, LivroRetrieveSerializer
from .compra import CompraSerializer
from .compra import CompraSerializer, CompraCreateUpdateSerializer, ItensCompraSerializer
from .compra import (
    CompraListSerializer, # novo
    CompraCreateUpdateSerializer,
    CompraSerializer,
    ItensCompraCreateUpdateSerializer,
    ItensCompraListSerializer, # novo
    ItensCompraSerializer,
)
