from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Cliente
from app.models.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """
    Cria um novo cliente.
    """
    # Verificar se email já existe
    if cliente.email:
        existe = db.query(Cliente).filter(Cliente.email == cliente.email).first()
        if existe:
            raise HTTPException(
                status_code=400,
                detail="Email já cadastrado"
            )
    
    # Criar cliente
    db_cliente = Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    
    return db_cliente

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os clientes com paginação.
    
    - skip: quantos registros pular (padrão: 0)
    - limit: quantos registros retornar (padrão: 100)
    """
    clientes = db.query(Cliente).offset(skip).limit(limit).all()
    return clientes

@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Busca cliente por ID.
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )
    
    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza dados do cliente.
    """
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Atualizar apenas campos fornecidos
    update_data = cliente_update.model_dump(exclude_unset=True)
    
    # Verificar email duplicado se estiver sendo atualizado
    if "email" in update_data and update_data["email"]:
        existe = db.query(Cliente).filter(
            Cliente.email == update_data["email"],
            Cliente.id != cliente_id
        ).first()
        if existe:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    for key, value in update_data.items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    
    return db_cliente

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Deleta um cliente.
    """
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(db_cliente)
    db.commit()
    
    return None