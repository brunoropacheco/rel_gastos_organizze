from datetime import datetime
import pytest
from pydantic import ValidationError
from src.app.schemas.transaction import TransactionCreate, TransactionResponse

def test_transaction_create_valid():
    payload = {
        "description": "Compra no mercado",
        "amount_cents": 15000,
        "date": "2026-06-20T10:00:00Z"
    }
    tx = TransactionCreate(**payload)
    assert tx.description == "Compra no mercado"
    assert tx.amount_cents == 15000

def test_transaction_create_negative_amount():
    payload = {
        "description": "Compra no mercado",
        "amount_cents": -50,
        "date": "2026-06-20T10:00:00Z"
    }
    with pytest.raises(ValidationError):
        TransactionCreate(**payload)

def test_transaction_response():
    data = {
        "id": 1,
        "description": "Teste",
        "amount_cents": 100,
        "date": datetime(2026, 6, 20, 10, 0, 0),
        "source": "webhook",
        "created_at": datetime(2026, 6, 20, 10, 0, 0)
    }
    tx = TransactionResponse(**data)
    assert tx.id == 1
    assert tx.description == "Teste"
