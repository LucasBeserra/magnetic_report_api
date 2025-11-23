from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Mostra SQL no console apenas em modo debug
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_size=10,  # Número de conexões mantidas no pool
    max_overflow=20  # Conexões extras permitidas em picos de acesso
)

# SessionLocal: factory para criar sessões de banco de dados
SessionLocal = sessionmaker(
    autocommit=False,  # Transações manuais (mais controle)
    autoflush=False,  # Não salva automaticamente (mais controle)
    bind=engine
)

# Base: classe base para todos os modelos
# Todos os modelos herdarão desta classe
Base = declarative_base()

# Dependency: função geradora que fornece sessão de BD para as rotas
def get_db():
    """
    Dependency Injection do FastAPI.
    
    Cria uma sessão, fornece para a rota, e garante que seja fechada
    ao final da requisição (mesmo se houver erro).
    
    Uso nas rotas:
    @app.get("/clientes")
    def listar_clientes(db: Session = Depends(get_db)):
        ...
    """
    db = SessionLocal()
    try:
        yield db  # Fornece a sessão para a rota
    finally:
        db.close()  # Garante que a conexão seja fechada

# Função para criar todas as tabelas no banco
def init_db():
    """
    Cria todas as tabelas definidas nos modelos.
    
    Será chamada no main.py quando a aplicação iniciar.
    Em produção, você usaria Alembic para migrations ao invés disso.
    """
    Base.metadata.create_all(bind=engine)