from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.app.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events.
    """
    # A inicialização do banco agora é feita exclusivamente via Alembic
    yield
    # Lógica de encerramento, se necessário

app = FastAPI(
    title="rel_gastos_organizze",
    description="A FastAPI backend for Organizze tracking and Apple Wallet webhook.",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    """
    Endpoint de verificação de saúde da aplicação.
    """
    return {"status": "ok"}
