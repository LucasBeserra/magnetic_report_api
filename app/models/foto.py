from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Foto(Base):
    """
    Modelo de Foto anexada ao relatório.
    
    Armazena metadados da foto. O arquivo físico fica na pasta 'uploads/'.
    """
    __tablename__ = "fotos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Chave estrangeira para o relatório
    relatorio_id = Column(Integer, ForeignKey("relatorios.id"), nullable=False)
    
    # Informações do arquivo
    nome_original = Column(String(300), nullable=False)  # Nome do arquivo enviado
    nome_arquivo = Column(String(300), nullable=False, unique=True)  # Nome único no servidor
    caminho = Column(String(500), nullable=False)  # Caminho completo do arquivo
    tamanho = Column(Integer, nullable=False)  # Tamanho em bytes
    mime_type = Column(String(100), nullable=False)  # image/jpeg, image/png, etc
    
    # Metadados opcionais
    descricao = Column(String(500), nullable=True)  # Descrição da foto
    ordem = Column(Integer, default=0)  # Ordem de exibição no relatório
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento
    relatorio = relationship("Relatorio", back_populates="fotos")
    
    def __repr__(self):
        return f"<Foto(id={self.id}, nome='{self.nome_original}')>"