from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configurações da aplicação, carregadas automaticamente de variáveis de ambiente
    ou de um arquivo .env.
    """
    database_url: str = "postgresql://user:pass@localhost:5432/db"  # Deve ser sobrescrito pelo .env
    
    model_config = {"env_file": ".env"}

settings = Settings()
