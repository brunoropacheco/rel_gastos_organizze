from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    """
    Configurações da aplicação, carregadas automaticamente de variáveis de ambiente
    ou de um arquivo .env.
    """
    database_url: str = "postgresql://user:pass@localhost:5432/db"  # Deve ser sobrescrito pelo .env
    webhook_api_key: str
    token_organizze: str
    callmebot_user: str
    
    @field_validator("database_url", mode="before")
    def assemble_db_connection(cls, v: str) -> str:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v
    
    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
