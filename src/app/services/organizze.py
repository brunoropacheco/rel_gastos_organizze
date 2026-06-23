import httpx
import logging
import base64
from typing import List
from src.app.core.config import settings
from src.app.schemas.organizze import OrganizzeTransaction

logger = logging.getLogger(__name__)

ORGANIZZE_API_URL = "https://api.organizze.com.br/rest/v2/transactions"

class SyncError(Exception):
    pass

async def sync_transactions() -> List[OrganizzeTransaction]:
    """
    Sincroniza transações da API v2 do Organizze.
    Lida com rate-limits e erros de rede graciosamente.
    """
    # Encode for Basic Auth
    token_bytes = settings.token_organizze.encode("utf-8")
    base64_auth = base64.b64encode(token_bytes).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {base64_auth}",
        "User-Agent": "rel_gastos_organizze/0.1"
    }

    transactions = []
    url = ORGANIZZE_API_URL

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            while url:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                transactions.extend([OrganizzeTransaction(**item) for item in data])
                
                # Check for pagination (e.g. link header or custom body)
                # Usually APIs use Links header for pagination: response.links.get("next", {}).get("url")
                url = response.links.get("next", {}).get("url")
                
            return transactions

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            logger.error("Rate limit exceeded on Organizze API")
            raise SyncError("Rate limit exceeded") from e
        else:
            logger.error(f"HTTP error from Organizze API: {e.response.status_code}")
            raise SyncError(f"HTTP error: {e.response.status_code}") from e
    except httpx.RequestError as e:
        logger.error(f"Network error while connecting to Organizze API: {str(e)}")
        raise SyncError(f"Network error: {str(e)}") from e
    except Exception as e:
        logger.exception("Unexpected error during Organizze sync")
        raise SyncError("Unexpected error") from e
