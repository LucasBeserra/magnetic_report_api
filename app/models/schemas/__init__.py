"""
Importa todos os schemas para facilitar o uso.

Permite fazer: from app.schemas import ClienteCreate, ClienteResponse
"""

from app.models.schemas.cliente import (
    ClienteBase,
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse
)

from app.models.schemas.produto import (
    ProdutoBase,
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse
)

from app.models.schemas.relatorio import (
    FotoResponse,
    RelatorioBase,
    RelatorioCreate,
    RelatorioUpdate,
    RelatorioResponse,
    RelatorioListResponse
)

__all__ = [
    # Cliente
    "ClienteBase",
    "ClienteCreate",
    "ClienteUpdate",
    "ClienteResponse",
    
    # Produto
    "ProdutoBase",
    "ProdutoCreate",
    "ProdutoUpdate",
    "ProdutoResponse",
    
    # Relatorio
    "FotoResponse",
    "RelatorioBase",
    "RelatorioCreate",
    "RelatorioUpdate",
    "RelatorioResponse",
    "RelatorioListResponse",
]