from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_validator
import unicodedata

class CategoryLimit(SQLModel, table=True):
    """
    Representa o limite de gastos mensal configurado para uma categoria.
    """
    __tablename__ = "Limits"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str = Field(min_length=1, index=True, unique=True, description="Nome da categoria (ex: 'Alimentacao')")
    limit_cents: int = Field(ge=0, description="Valor do limite em centavos para a categoria")

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Category cannot be empty")
        v = v.strip().lower()
        v = ''.join(c for c in unicodedata.normalize('NFD', v) if unicodedata.category(c) != 'Mn')
        return v
