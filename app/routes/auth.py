from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    create_refresh_token,
    verify_token
)
from app.models.users import User
from app.models.schemas.user import (
    UserCreate, 
    UserLogin, 
    UserResponse, 
    Token, 
    TokenRefresh,
    PasswordResetRequest,
    PasswordReset,
    EmailVerification
)
from app.services.email_service import send_verification_email, send_password_reset_email
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    # Verifica se o email já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Cria o usuário
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Envia email de verificação (não dá erro se falhar)
    try:
        send_verification_email(new_user.email, new_user.full_name)
    except:
        pass  # Email não configurado ainda, sem problemas
    
    return new_user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Faz login e retorna tokens JWT"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    # Cria tokens
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Renova o access token usando refresh token"""
    email = verify_token(token_data.refresh_token, "refresh")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado"
        )
    
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado ou inativo"
        )
    
    # Cria novos tokens
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(verification: EmailVerification, db: Session = Depends(get_db)):
    """Verifica o email do usuário"""
    email = verify_token(verification.token, "verify")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de verificação inválido ou expirado"
        )
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    if user.is_verified:
        return {"message": "Email já verificado"}
    
    user.is_verified = True
    db.commit()
    
    return {"message": "Email verificado com sucesso"}


@router.post("/resend-verification", status_code=status.HTTP_200_OK)
async def resend_verification(current_user: User = Depends(get_current_user)):
    """Reenvia email de verificação"""
    if current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já verificado"
        )
    
    try:
        send_verification_email(current_user.email, current_user.full_name)
        return {"message": "Email de verificação reenviado"}
    except:
        return {"message": "Não foi possível enviar o email (configuração pendente)"}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """Solicita recuperação de senha"""
    user = db.query(User).filter(User.email == request.email).first()
    
    # Por segurança, sempre retorna sucesso (mesmo se email não existir)
    if user:
        try:
            send_password_reset_email(user.email, user.full_name)
        except:
            pass  # Email não configurado
    
    return {
        "message": "Se o email estiver cadastrado, você receberá instruções para redefinir sua senha"
    }


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(reset_data: PasswordReset, db: Session = Depends(get_db)):
    """Redefine a senha usando token"""
    email = verify_token(reset_data.token, "reset")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de recuperação inválido ou expirado"
        )
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Atualiza a senha
    user.hashed_password = get_password_hash(reset_data.new_password)
    db.commit()
    
    return {"message": "Senha redefinida com sucesso"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Retorna informações do usuário logado"""
    return current_user