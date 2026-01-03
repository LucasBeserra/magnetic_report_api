from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Cliente(Base):

    __tablename__ = "clientes"
    
    # Colunas
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=True, index=True)
    
    # Timestamps 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    # Um cliente pode ter vários relatórios
    relatorios = relationship("Relatorio", back_populates="cliente", cascade="all, delete-orphan")
    
    def __repr__(self):
        """Representação em string do objeto (útil para debug)"""
        return f"<Cliente(id={self.id}, nome='{self.nome}')>"