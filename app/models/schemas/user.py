from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Schema base com dados comuns
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


# Schema para criar usuário (registro)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Senha com no mínimo 8 caracteres")


# Schema para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema para retornar dados do usuário (sem a senha!)
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Permite converter do SQLAlchemy para Pydantic


# Schema para atualizar dados do usuário
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


# Schema para mudança de senha
class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)


# Schema para pedir reset de senha
class PasswordResetRequest(BaseModel):
    email: EmailStr


# Schema para definir nova senha
class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


# Schema para os tokens JWT
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Schema para renovar token
class TokenRefresh(BaseModel):
    refresh_token: str


# Schema para verificação de email
class EmailVerification(BaseModel):
    token: str