import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
from src.app.main import app
from src.app.db.session import get_session
from src.app.core.config import settings
from src.app.models.transaction import Transaction

# In-memory database for testing
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

def get_session_override():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    old_key = getattr(settings, "webhook_api_key", None)
    settings.webhook_api_key = "testkey"
    yield
    settings.webhook_api_key = old_key
    SQLModel.metadata.drop_all(engine)

def test_create_transaction_unauthorized():
    response = client.post(
        "/api/webhooks/transactions",
        json={"description": "Test", "amount_cents": 100, "date": "2026-06-20T10:00:00Z"}
    )
    assert response.status_code in (401, 403)

def test_create_transaction_success():
    payload = {
        "description": "Ifood",
        "amount_cents": 4500,
        "date": "2026-06-20T10:00:00Z"
    }
    response = client.post(
        "/api/webhooks/transactions",
        headers={"X-API-Key": "testkey"},
        json=payload
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Ifood"
    assert data["amount_cents"] == 4500
    assert data["source"] == "webhook"

def test_create_transaction_duplicate():
    payload = {
        "description": "Ifood",
        "amount_cents": 4500,
        "date": "2026-06-20T10:00:00Z"
    }
    # First request
    response1 = client.post(
        "/api/webhooks/transactions",
        headers={"X-API-Key": "testkey"},
        json=payload
    )
    assert response1.status_code == 201

    # Second request (duplicate)
    response2 = client.post(
        "/api/webhooks/transactions",
        headers={"X-API-Key": "testkey"},
        json=payload
    )
    # Should handle gracefully, returning either 200 or 201 without crashing
    assert response2.status_code in (200, 201)
    
    # Verifica que só há uma transação no banco
    with Session(engine) as session:
        count = session.exec(select(Transaction)).all()
        assert len(count) == 1
