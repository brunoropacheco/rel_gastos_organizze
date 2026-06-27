import pytest
from unittest.mock import patch, MagicMock
import httpx
from src.app.services.notify_service import format_telegram_message, send_telegram_message
from src.app.core.config import settings

def test_format_telegram_message():
    stats = {
        "total_budget_cents": 300000,
        "total_spent_cents": 150000,
        "projected_fixed_expenses_cents": 50000,
        "remaining_budget_cents": 100000,
        "days_remaining": 10,
        "daily_target_cents": 10000
    }
    
    message = format_telegram_message(stats)
    
    assert "3.000,00" in message
    assert "1.500,00" in message
    assert "500,00" in message
    assert "1.000,00" in message
    assert "10" in message
    assert "100,00" in message
    assert "🔥" in message or "📊" in message or "💰" in message # Emojis check

@pytest.mark.asyncio
@patch("src.app.services.notify_service.httpx.AsyncClient.get")
async def test_send_telegram_message_success(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    with patch.object(settings, 'callmebot_user', '123456789'):
        
        result = await send_telegram_message("Test Message")
        assert result is True
        
        mock_get.assert_called_once()
        url_called = mock_get.call_args[0][0]
        assert "api.callmebot.com" in url_called
        assert "user=123456789" in url_called
        assert "text=Test%20Message" in url_called

@pytest.mark.asyncio
@patch("src.app.services.notify_service.httpx.AsyncClient.get")
async def test_send_telegram_message_failure_no_log_leak(mock_get, caplog):
    mock_get.side_effect = httpx.RequestError("Network error", request=httpx.Request("GET", "https://api.callmebot.com/text.php?user=123456789&text=Test"))
    
    with patch.object(settings, 'callmebot_user', '123456789'):
        
        result = await send_telegram_message("Test Message")
        assert result is False
        
        # Ensure the phone and apikey are not in the log output
        for record in caplog.records:
            assert "123456789" not in record.message
