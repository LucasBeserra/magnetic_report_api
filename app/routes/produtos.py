from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Produto
from app.models.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo produto.
    """
    # Verificar se código já existe
    existe = db.query(Produto).filter(Produto.codigo == produto.codigo).first()
    if existe:
        raise HTTPException(status_code=400, detail="Código de produto já existe")
    
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    
    return db_produto

@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os produtos.
    """
    produtos = db.query(Produto).offset(skip).limit(limit).all()
    return produtos

@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    """
    Busca produto por ID.
    """
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return produto

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto_update: ProdutoUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza dados do produto.
    """
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    update_data = produto_update.model_dump(exclude_unset=True)
    
    # Verificar código duplicado
    if "codigo" in update_data:
        existe = db.query(Produto).filter(
            Produto.codigo == update_data["codigo"],
            Produto.id != produto_id
        ).first()
        if existe:
            raise HTTPException(status_code=400, detail="Código já existe")
    
    for key, value in update_data.items():
        setattr(db_produto, key, value)
    
    db.commit()
    db.refresh(db_produto)
    
    return db_produto

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    """
    Deleta um produto.
    """
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(db_produto)
    db.commit()
    
    return None