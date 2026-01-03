from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

"""
Schemas para validação de dados de Cliente.

Base: campos comuns
Create: dados necessários para criar
Update: dados que podem ser atualizados (todos opcionais)
Response: dados retornados pela API
"""

class ClienteBase(BaseModel):
    """Schema base com campos comuns"""
    nome: str = Field(..., min_length=1, max_length=200, description="Nome do cliente")
    email: Optional[EmailStr] = Field(None, description="Email válido")

class ClienteCreate(ClienteBase):
    """
    Schema para criar cliente.
    Herda todos os campos de ClienteBase.
    """
    pass

class ClienteUpdate(BaseModel):
    """
    Schema para atualizar cliente.
    Todos os campos são opcionais (você pode atualizar só o que quiser).
    """
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None

class ClienteResponse(ClienteBase):
    """
    Schema de resposta da API.
    Inclui campos calculados/gerados pelo banco (id, timestamps).
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        """
        Configuração do Pydantic.
        from_attributes=True permite converter objetos SQLAlchemy para Pydantic.
        """
        from_attributes = True