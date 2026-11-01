from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime, timezone

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


    @field_validator("date", "invoice_date")
    @classmethod
    def _ensure_utc(cls, v: Optional[datetime]) -> Optional[datetime]:
        # Organizze returns date-only strings; the DB columns are timezone-aware.
        # Naive values are already treated as UTC by normalize_date, so hashes are unchanged.
        if v is not None and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v
