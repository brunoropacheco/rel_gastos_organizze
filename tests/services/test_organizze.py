import pytest
import respx
import httpx
import base64
from src.app.services.organizze import sync_transactions, SyncError
from src.app.core.config import settings

@pytest.mark.asyncio
async def test_sync_transactions_success():
    token_bytes = settings.token_organizze.encode("utf-8")
    expected_auth = f"Basic {base64.b64encode(token_bytes).decode('utf-8')}"
    
    with respx.mock:
        # Mock organizze API
        route = respx.get("https://api.organizze.com.br/rest/v2/transactions").mock(
            return_value=httpx.Response(200, json=[
                {
                    "id": 1,
                    "description": "Compra Teste",
                    "date": "2023-10-10T00:00:00Z",
                    "amount_cents": 15000,
                    "type": "expense",
                    "category_id": 123
                }
            ])
        )
        transactions = await sync_transactions()
        assert len(transactions) == 1
        assert transactions[0].description == "Compra Teste"
        assert transactions[0].amount_cents == 15000
        assert route.called
        assert route.calls[0].request.headers["Authorization"] == expected_auth

@pytest.mark.asyncio
async def test_sync_transactions_rate_limit(caplog):
    with respx.mock:
        route = respx.get("https://api.organizze.com.br/rest/v2/transactions").mock(
            return_value=httpx.Response(429, json={"error": "Rate limit exceeded"})
        )
        with pytest.raises(SyncError, match="Rate limit exceeded"):
            await sync_transactions()
            
        assert route.called
        assert "Rate limit exceeded on Organizze API" in caplog.text

@pytest.mark.asyncio
async def test_sync_transactions_network_error(caplog):
    with respx.mock:
        route = respx.get("https://api.organizze.com.br/rest/v2/transactions").mock(
            side_effect=httpx.ConnectError("Network error")
        )
        with pytest.raises(SyncError, match="Network error"):
            await sync_transactions()
            
        assert route.called
        assert "Network error while connecting to Organizze API" in caplog.text
