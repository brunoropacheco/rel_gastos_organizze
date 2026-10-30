from sqlmodel import SQLModel, create_engine, Session
from src.app.core.config import settings

# Engine global da aplicação
connect_args = {}
if "postgres" in settings.database_url:
    connect_args["sslmode"] = "require"
elif "sqlite" in settings.database_url:
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url, 
    echo=False,
    connect_args=connect_args
)

def init_db():
    """
    Inicializa a base de dados (Cria tabelas se não existirem).
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Generator para injetar sessões do banco de dados nas rotas do FastAPI.
    """
    with Session(engine) as session:
        yield session
