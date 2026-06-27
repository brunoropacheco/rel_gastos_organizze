from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configurações da aplicação, carregadas automaticamente de variáveis de ambiente
    ou de um arquivo .env.
    """
    database_url: str = "postgresql://user:pass@localhost:5432/db"  # Deve ser sobrescrito pelo .env
    webhook_api_key: str
    token_organizze: str
    callmebot_user: str
    
    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
