from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import init_db
from app.routes import clientes, produtos, relatorios

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API para gerenciamento de relatórios técnicos",
    docs_url="/docs",  # Swagger UI em http://localhost:8000/docs
    redoc_url="/redoc"  # ReDoc em http://localhost:8000/redoc
)

# Configurar CORS (permite requisições do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Origens permitidas
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],  # Permite todos os headers
)

# Servir arquivos estáticos (imagens do upload)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Registrar routers
app.include_router(clientes.router)
app.include_router(produtos.router)
app.include_router(relatorios.router)

# Evento de inicialização (executado quando app inicia)
@app.on_event("startup")
def startup_event():
    """
    Cria tabelas no banco de dados ao iniciar a aplicação.
    
    IMPORTANTE: Em produção, use Alembic para migrations!
    """
    print("🚀 Iniciando Magnetic Report API...")
    print(f"📦 Criando tabelas no banco de dados...")
    init_db()
    print("✅ Banco de dados inicializado!")

# Rota raiz (health check)
@app.get("/", tags=["Health"])
def root():
    """
    Endpoint raiz - verifica se API está funcionando.
    """
    return {
        "message": "Magnetic Report API está rodando! 🚀",
        "version": settings.VERSION,
        "docs": "/docs"
    }

# Endpoint de health check
@app.get("/health", tags=["Health"])
def health_check():
    """
    Verifica saúde da aplicação.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION
    }

# Para rodar: uvicorn app.main:app --reload
# --reload: reinicia automaticamente ao detectar mudanças no código