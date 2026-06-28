from typing import Optional, Literal
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class Transaction(SQLModel, table=True):
    """
    Modelo base para transações financeiras consolidando dados do Organizze
    e do Webhook (Apple Wallet).
    """
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(max_length=255)
    amount_cents: int = Field(ge=0)
    date: datetime
    hash_signature: str = Field(unique=True, index=True, max_length=255)
    installment: Optional[int] = Field(default=None)
    total_installments: Optional[int] = Field(default=None)
    credit_card_id: Optional[int] = Field(default=None)
    invoice_date: Optional[datetime] = Field(default=None)
    category_name: Optional[str] = Field(default=None, max_length=100)
    source: str = Field(default="webhook", max_length=50)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __str__(self):
        return f"Transaction(id={self.id}, desc={self.description}, amount_cents={self.amount_cents}, date={self.date})"
