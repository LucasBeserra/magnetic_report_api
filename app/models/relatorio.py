from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Relatorio(Base):
    """
    Modelo principal de Relatório Técnico.
    
    Armazena informações do relatório e se relaciona com Cliente,
    Produto e Fotos.
    """
    __tablename__ = "relatorios"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo_pedido = Column(String(100), unique=True, nullable=False, index=True)
    titulo = Column(String(300), nullable=True)
    descricao = Column(Text, nullable=True)
    observacoes = Column(Text, nullable=True)
    
    # Chaves estrangeiras (Foreign Keys)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    
    # Dados da tabela dinâmica (estrutura + valores)
    # Exemplo: {
    #   "estrutura": {"colunas": ["Medida", "Valor"], ...},
    #   "dados": [["100mm", "50kg"], ["200mm", "75kg"]]
    # }
    dados_tabela = Column(JSON, nullable=True)
    
    # Status do relatório
    status = Column(String(50), default="rascunho")  # rascunho, concluido, aprovado
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="relatorios")
    produto = relationship("Produto", back_populates="relatorios")
    fotos = relationship("Foto", back_populates="relatorio", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Relatorio(id={self.id}, codigo_pedido='{self.codigo_pedido}')>"