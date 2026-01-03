from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Usa Pydantic para validar e carregar variáveis de ambiente automaticamente.
    
    # Informações da aplicação
    APP_NAME: str = "Magnetic Report API"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # Banco de dados
    DATABASE_URL: str
    
    # Segurança e JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Upload de arquivos
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    # CORS - Origens permitidas (frontend)
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # ===== NOVAS CONFIGURAÇÕES DE AUTENTICAÇÃO =====
    
    # Email
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "noreply@magneticreport.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "Magnetic Report"
    
    # Frontend URL
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Tokens de Verificação
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24
    
    class Config:
        # Configuração do Pydantic para carregar variáveis do arquivo .env
        env_file = ".env"
        case_sensitive = True

# Instância global das configurações
# Será importada em outros arquivos como: from app.config import settings
settings = Settings()

# Criar diretório de uploads se não existir
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)