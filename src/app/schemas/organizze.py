from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrganizzeTransaction(BaseModel):
    id: int
    description: str
    date: datetime
    amount_cents: int
    type: str  # e.g., 'expense', 'income'
    category_id: Optional[int] = None
