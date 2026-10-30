import secrets
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from src.app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_webhook_api_key(api_key_header: str = Security(api_key_header)):
    """Verifica se a chave da API fornecida via header é válida."""
    if not secrets.compare_digest(api_key_header, settings.webhook_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key_header
