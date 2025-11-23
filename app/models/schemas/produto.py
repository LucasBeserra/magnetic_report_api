from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

"""
Schemas para validação de dados de Produto.
"""

class ProdutoBase(BaseModel):
    """Schema base com campos comuns"""
    nome: str = Field(..., min_length=1, max_length=200)
    codigo: str = Field(..., min_length=1, max_length=100, description="Código único do produto")
    descricao: Optional[str] = None
    categoria: Optional[str] = Field(None, max_length=100)
    template_tabela: Optional[Dict[str, Any]] = Field(
        None, 
        description="Template JSON da tabela dinâmica para este produto"
    )

class ProdutoCreate(ProdutoBase):
    """Schema para criar produto"""
    pass

class ProdutoUpdate(BaseModel):
    """Schema para atualizar produto - todos campos opcionais"""
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    codigo: Optional[str] = Field(None, min_length=1, max_length=100)
    descricao: Optional[str] = None
    categoria: Optional[str] = Field(None, max_length=100)
    template_tabela: Optional[Dict[str, Any]] = None

class ProdutoResponse(ProdutoBase):
    """Schema de resposta da API"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True