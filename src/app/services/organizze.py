import httpx
import logging
import base64
from datetime import datetime, timedelta
from typing import List
from src.app.core.config import settings
from src.app.schemas.organizze import OrganizzeTransaction

logger = logging.getLogger(__name__)

ORGANIZZE_API_URL = "https://api.organizze.com.br/rest/v2/transactions"
ORGANIZZE_API_CATEGORIES_URL = "https://api.organizze.com.br/rest/v2/categories"

class SyncError(Exception):
    pass

async def sync_transactions() -> List[OrganizzeTransaction]:
    """
    Sincroniza transações da API v2 do Organizze.
    Lida com rate-limits e erros de rede graciosamente.
    """
    # O token no .env já está em base64 (email:token)
    headers = {
        "Authorization": f"Basic {settings.token_organizze}",
        "User-Agent": "rel_gastos_organizze/0.1"
    }

    hoje = datetime.now()
    start_date = (hoje - timedelta(days=90)).strftime('%Y-%m-%d')
    end_date = (hoje + timedelta(days=60)).strftime('%Y-%m-%d')

    transactions = []
    valid_cards = [1840776, 2423452] # IDs do Cartao_Santander_AA e Cartao_Itau_Azul

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            for card_id in valid_cards:
                # 1. Fetch invoices for this card
                inv_url = f"https://api.organizze.com.br/rest/v2/credit_cards/{card_id}/invoices?start_date={start_date}&end_date={end_date}"
                res_inv = await client.get(inv_url, headers=headers)
                res_inv.raise_for_status()
                invoices = res_inv.json()
                
                for inv in invoices:
                    inv_date_str = inv['date']
                    # 2. Fetch transactions for each invoice
                    tx_url = f"https://api.organizze.com.br/rest/v2/credit_cards/{card_id}/invoices/{inv['id']}"
                    res_tx = await client.get(tx_url, headers=headers)
                    res_tx.raise_for_status()
                    inv_data = res_tx.json()
                    
                    for item in inv_data.get('transactions', []):
                        item['invoice_date'] = inv_date_str
                        # Se credit_card_id não estiver presente no item, injetar para não quebrar a tipagem
                        if 'credit_card_id' not in item:
                            item['credit_card_id'] = card_id
                        transactions.append(OrganizzeTransaction(**item))
                
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

async def sync_categories() -> dict:
    """
    Busca categorias da API v2 do Organizze e retorna mapeamento {id: name}.
    """
    headers = {
        "Authorization": f"Basic {settings.token_organizze}",
        "User-Agent": "rel_gastos_organizze/0.1"
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(ORGANIZZE_API_CATEGORIES_URL, headers=headers)
            response.raise_for_status()
            data = response.json()
            return {item["id"]: item["name"] for item in data}
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from Organizze API Categories: {e.response.status_code}")
        raise SyncError(f"HTTP error: {e.response.status_code}") from e
    except httpx.RequestError as e:
        logger.error(f"Network error while connecting to Organizze API Categories: {str(e)}")
        raise SyncError(f"Network error: {str(e)}") from e
    except Exception as e:
        logger.exception("Unexpected error during Organizze categories sync")
        raise SyncError("Unexpected error") from e
