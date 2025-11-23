from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.schemas.cliente import ClienteResponse
from app.models.schemas.produto import ProdutoResponse

"""
Schemas para validação de dados de Relatório e Foto.
"""

class FotoResponse(BaseModel):
    """Schema para fotos anexadas ao relatório"""
    id: int
    nome_original: str
    nome_arquivo: str
    caminho: str
    tamanho: int
    mime_type: str
    descricao: Optional[str] = None
    ordem: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RelatorioBase(BaseModel):
    """Schema base com campos comuns"""
    codigo_pedido: str = Field(..., min_length=1, max_length=100)
    titulo: Optional[str] = Field(None, max_length=300)
    descricao: Optional[str] = None
    observacoes: Optional[str] = None
    cliente_id: int = Field(..., gt=0)
    produto_id: int = Field(..., gt=0)
    dados_tabela: Optional[Dict[str, Any]] = Field(
        None,
        description="Estrutura e dados da tabela dinâmica"
    )
    status: Optional[str] = Field("rascunho", max_length=50)

class RelatorioCreate(RelatorioBase):
    """Schema para criar relatório"""
    pass

class RelatorioUpdate(BaseModel):
    """Schema para atualizar relatório - todos campos opcionais"""
    codigo_pedido: Optional[str] = Field(None, min_length=1, max_length=100)
    titulo: Optional[str] = Field(None, max_length=300)
    descricao: Optional[str] = None
    observacoes: Optional[str] = None
    cliente_id: Optional[int] = Field(None, gt=0)
    produto_id: Optional[int] = Field(None, gt=0)
    dados_tabela: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, max_length=50)

class RelatorioResponse(RelatorioBase):
    """
    Resposta completa do relatório.
    Inclui dados relacionados de cliente, produto e fotos.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Dados relacionados (populated automaticamente pelo SQLAlchemy)
    cliente: ClienteResponse
    produto: ProdutoResponse
    fotos: List[FotoResponse] = []
    
    class Config:
        from_attributes = True

class RelatorioListResponse(BaseModel):
    """
    Versão simplificada para listagem (sem todos os relacionamentos).
    Retorna mais rápido quando você lista muitos relatórios.
    """
    id: int
    codigo_pedido: str
    titulo: Optional[str]
    status: str
    cliente_id: int
    produto_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True