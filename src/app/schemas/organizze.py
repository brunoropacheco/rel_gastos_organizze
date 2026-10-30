from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrganizzeTransaction(BaseModel):
    id: int
    description: str
    date: datetime
    amount_cents: int
    type: Optional[str] = None
    category_id: Optional[int] = None
    notes: Optional[str] = None
    credit_card_id: Optional[int] = None
    account_id: Optional[int] = None
    installment: Optional[int] = None
    total_installments: Optional[int] = None
    invoice_date: Optional[datetime] = None
