import pytest
from fastapi import HTTPException
from fastapi.security import APIKeyHeader
from src.app.core.security import verify_webhook_api_key
from src.app.core.config import settings

def test_verify_api_key_valid(monkeypatch):
    monkeypatch.setattr(settings, "webhook_api_key", "secret_key")
    assert verify_webhook_api_key("secret_key") == "secret_key"

def test_verify_api_key_invalid(monkeypatch):
    monkeypatch.setattr(settings, "webhook_api_key", "secret_key")
    with pytest.raises(HTTPException) as excinfo:
        verify_webhook_api_key("wrong_key")
    assert excinfo.value.status_code == 401
    assert "Invalid API Key" in excinfo.value.detail
