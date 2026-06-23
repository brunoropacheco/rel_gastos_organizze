from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

class TransactionCreate(BaseModel):
    """Schema para criação de uma nova transação a partir do webhook."""
    description: str = Field(..., max_length=255, description="Descrição do gasto")
    amount_cents: int = Field(..., ge=0, le=2147483647, description="Valor em centavos (ex: 1000 = R$ 10,00)")
    date: datetime = Field(..., description="Data e hora da transação")

class TransactionResponse(BaseModel):
    """Schema de resposta após criação de transação."""
    id: int
    description: str
    amount_cents: int
    date: datetime
    source: Literal["webhook", "organizze"]
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }
