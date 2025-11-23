from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Relatorio, Foto, Cliente, Produto
from app.models.schemas.relatorio import (
    RelatorioCreate, 
    RelatorioUpdate, 
    RelatorioResponse,
    RelatorioListResponse,
    FotoResponse
)
from app.services.upload_service import UploadService
from app.services.pdf_service import PDFService
import os

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.post("/", response_model=RelatorioResponse, status_code=status.HTTP_201_CREATED)
def criar_relatorio(relatorio: RelatorioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo relatório técnico.
    """
    # Verificar se cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == relatorio.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verificar se produto existe
    produto = db.query(Produto).filter(Produto.id == relatorio.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Verificar código de pedido único
    existe = db.query(Relatorio).filter(
        Relatorio.codigo_pedido == relatorio.codigo_pedido
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Código de pedido já existe")
    
    # Criar relatório
    db_relatorio = Relatorio(**relatorio.model_dump())
    db.add(db_relatorio)
    db.commit()
    db.refresh(db_relatorio)
    
    return db_relatorio

@router.get("/", response_model=List[RelatorioListResponse])
def listar_relatorios(
    skip: int = 0,
    limit: int = 100,
    status_filtro: str = None,
    db: Session = Depends(get_db)
):
    """
    Lista todos os relatórios com filtro opcional por status.
    """
    query = db.query(Relatorio)
    
    if status_filtro:
        query = query.filter(Relatorio.status == status_filtro)
    
    relatorios = query.offset(skip).limit(limit).all()
    return relatorios

@router.get("/{relatorio_id}", response_model=RelatorioResponse)
def buscar_relatorio(relatorio_id: int, db: Session = Depends(get_db)):
    """
    Busca relatório completo por ID (inclui cliente, produto e fotos).
    """
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    return relatorio

@router.put("/{relatorio_id}", response_model=RelatorioResponse)
def atualizar_relatorio(
    relatorio_id: int,
    relatorio_update: RelatorioUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza dados do relatório.
    """
    db_relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    
    if not db_relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    update_data = relatorio_update.model_dump(exclude_unset=True)
    
    # Validar cliente_id se fornecido
    if "cliente_id" in update_data:
        cliente = db.query(Cliente).filter(Cliente.id == update_data["cliente_id"]).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Validar produto_id se fornecido
    if "produto_id" in update_data:
        produto = db.query(Produto).filter(Produto.id == update_data["produto_id"]).first()
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Verificar código de pedido duplicado
    if "codigo_pedido" in update_data:
        existe = db.query(Relatorio).filter(
            Relatorio.codigo_pedido == update_data["codigo_pedido"],
            Relatorio.id != relatorio_id
        ).first()
        if existe:
            raise HTTPException(status_code=400, detail="Código de pedido já existe")
    
    for key, value in update_data.items():
        setattr(db_relatorio, key, value)
    
    db.commit()
    db.refresh(db_relatorio)
    
    return db_relatorio

@router.delete("/{relatorio_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_relatorio(relatorio_id: int, db: Session = Depends(get_db)):
    """
    Deleta um relatório e suas fotos associadas.
    """
    db_relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    
    if not db_relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    # Deletar arquivos de foto do disco
    for foto in db_relatorio.fotos:
        UploadService.deletar_imagem(foto.caminho)
    
    db.delete(db_relatorio)
    db.commit()
    
    return None

# =============== ENDPOINTS DE FOTOS ===============

@router.post("/{relatorio_id}/fotos", response_model=FotoResponse, status_code=status.HTTP_201_CREATED)
async def adicionar_foto(
    relatorio_id: int,
    file: UploadFile = File(...),
    descricao: str = None,
    db: Session = Depends(get_db)
):
    """
    Adiciona uma foto ao relatório.
    """
    # Verificar se relatório existe
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    # Salvar arquivo
    nome_arquivo, caminho, tamanho = await UploadService.salvar_imagem(file)
    
    # Criar registro no banco
    db_foto = Foto(
        relatorio_id=relatorio_id,
        nome_original=file.filename,
        nome_arquivo=nome_arquivo,
        caminho=caminho,
        tamanho=tamanho,
        mime_type=file.content_type,
        descricao=descricao,
        ordem=len(relatorio.fotos)  # Adiciona no final
    )
    
    db.add(db_foto)
    db.commit()
    db.refresh(db_foto)
    
    return db_foto

@router.get("/{relatorio_id}/fotos", response_model=List[FotoResponse])
def listar_fotos(relatorio_id: int, db: Session = Depends(get_db)):
    """
    Lista todas as fotos de um relatório.
    """
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    return relatorio.fotos

@router.delete("/{relatorio_id}/fotos/{foto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_foto(relatorio_id: int, foto_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma foto do relatório.
    """
    foto = db.query(Foto).filter(
        Foto.id == foto_id,
        Foto.relatorio_id == relatorio_id
    ).first()
    
    if not foto:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    # Deletar arquivo do disco
    UploadService.deletar_imagem(foto.caminho)
    
    # Deletar do banco
    db.delete(foto)
    db.commit()
    
    return None

# =============== GERAÇÃO DE PDF ===============

@router.get("/{relatorio_id}/pdf")
def gerar_pdf(relatorio_id: int, db: Session = Depends(get_db)):
    """
    Gera PDF do relatório e retorna para download.
    """
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    # Preparar dados para o PDF
    relatorio_data = {
        'codigo_pedido': relatorio.codigo_pedido,
        'titulo': relatorio.titulo,
        'descricao': relatorio.descricao,
        'observacoes': relatorio.observacoes,
        'cliente': {
            'nome': relatorio.cliente.nome,
            'empresa': relatorio.cliente.empresa
        },
        'produto': {
            'nome': relatorio.produto.nome,
            'codigo': relatorio.produto.codigo
        },
        'dados_tabela': relatorio.dados_tabela,
        'fotos': [
            {
                'caminho': foto.caminho,
                'descricao': foto.descricao
            } for foto in relatorio.fotos
        ]
    }
    
    # Gerar PDF
    pdf_filename = f"relatorio_{relatorio.codigo_pedido}.pdf"
    pdf_path = os.path.join("uploads", pdf_filename)
    
    PDFService.gerar_relatorio_pdf(relatorio_data, pdf_path)
    
    # Retornar arquivo para download
    return FileResponse(
        pdf_path,
        media_type='application/pdf',
        filename=pdf_filename
    )