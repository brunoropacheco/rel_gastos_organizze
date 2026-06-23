import os
from src.app.core.config import Settings

def test_webhook_api_key_loaded(monkeypatch):
    # Test that the config can load WEBHOOK_API_KEY
    monkeypatch.setenv("WEBHOOK_API_KEY", "supersecret")
    monkeypatch.setenv("TOKEN_ORGANIZZE", "organizze_secret")
    settings = Settings()
    assert settings.webhook_api_key == "supersecret"
    assert settings.token_organizze == "organizze_secret"
