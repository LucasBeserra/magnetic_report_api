from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Produto(Base):
    """
    Modelo de Produto.
    
    Cada tipo de produto pode ter uma estrutura de tabela diferente,
    armazenada em JSON no campo 'template_tabela'.
    """
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    codigo = Column(String(100), unique=True, nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=True)
    
    # Template da tabela dinâmica para este tipo de produto
    # Exemplo: {"colunas": ["Medida", "Valor", "Status"], "tipos": ["text", "number", "select"]}
    template_tabela = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    relatorios = relationship("Relatorio", back_populates="produto")
    
    def __repr__(self):
        return f"<Produto(id={self.id}, nome='{self.nome}', codigo='{self.codigo}')>"