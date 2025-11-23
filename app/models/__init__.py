"Apenas para centralizar os imports e facilitar a importação"

from .cliente import Cliente
from .produto import Produto
from .relatorio import Relatorio
from .foto import Foto

# Lista de todos os modelos (útil para imports)
__all__ = ["Cliente", "Produto", "Relatorio", "Foto"]