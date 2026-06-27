import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool
from sqlalchemy.exc import OperationalError
from src.app.models.limit import CategoryLimit
from src.app.services.intel_service import get_monthly_limits, FALLBACK_LIMITS

@pytest_asyncio.fixture
async def async_engine():
    """Cria uma engine assíncrona isolada para os testes usando SQLite em memória."""
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.mark.asyncio
async def test_get_monthly_limits_from_db(async_engine):
    """Verifica se os limites cadastrados no banco são retornados corretamente e mesclados com o fallback."""
    async with AsyncSession(async_engine) as session:
        session.add(CategoryLimit(category="alimentacao", limit_cents=150000))
        session.add(CategoryLimit(category="transporte", limit_cents=50000))
        await session.commit()
        
        limits = await get_monthly_limits(session)
        assert limits["alimentacao"] == 150000
        assert limits["transporte"] == 50000
        # Check that fallback is merged
        assert limits["lazer"] == 30000

@pytest.mark.asyncio
async def test_get_monthly_limits_fallback_empty(async_engine):
    """Verifica se o fallback é utilizado integralmente quando a tabela de limites está vazia."""
    async with AsyncSession(async_engine) as session:
        limits = await get_monthly_limits(session)
        assert limits == FALLBACK_LIMITS

@pytest.mark.asyncio
async def test_get_monthly_limits_fallback_error(async_engine, monkeypatch):
    """Verifica se o fallback é acionado quando ocorre um erro de banco de dados (OperationalError)."""
    async with AsyncSession(async_engine) as session:
        # Simulate a database error
        async def mock_exec(*args, **kwargs):
            raise OperationalError("Mock connection error", params=None, orig=None)
            
        monkeypatch.setattr(session, "exec", mock_exec)
        
        limits = await get_monthly_limits(session)
        assert limits == FALLBACK_LIMITS

import datetime
from src.app.models.transaction import Transaction
from src.app.services.intel_service import (
    get_total_limits,
    get_current_month_spent,
    calculate_burn_rate_velocity,
)

@pytest.mark.asyncio
async def test_get_total_limits(async_engine):
    """Verifica se o total de limites é a soma correta dos valores com fallback."""
    async with AsyncSession(async_engine) as session:
        # Fallback values sum to 6000.00 -> 600000 cents
        session.add(CategoryLimit(category="saude", limit_cents=50000)) # Was 20000, +30000
        await session.commit()
        
        total = await get_total_limits(session)
        assert total == 630000  # 600000 + 30000

@pytest.mark.asyncio
async def test_get_current_month_spent(async_engine):
    """Verifica se as transações do mês correto são somadas."""
    async with AsyncSession(async_engine) as session:
        ref_date = datetime.date(2026, 6, 15)
        
        # Valid transactions
        t1 = Transaction(description="A", amount_cents=1000, hash_signature="1", date=datetime.datetime(2026, 6, 1, 10, tzinfo=datetime.timezone.utc))
        t2 = Transaction(description="B", amount_cents=2000, hash_signature="2", date=datetime.datetime(2026, 6, 30, 23, tzinfo=datetime.timezone.utc))
        
        # Invalid transactions (wrong month/year)
        t3 = Transaction(description="C", amount_cents=5000, hash_signature="3", date=datetime.datetime(2026, 5, 31, 23, tzinfo=datetime.timezone.utc))
        t4 = Transaction(description="D", amount_cents=10000, hash_signature="4", date=datetime.datetime(2027, 6, 15, 10, tzinfo=datetime.timezone.utc))
        
        session.add_all([t1, t2, t3, t4])
        await session.commit()
        
        spent = await get_current_month_spent(session, ref_date)
        assert spent == 3000

@pytest.mark.asyncio
async def test_calculate_burn_rate_velocity(async_engine):
    """Verifica o cálculo da velocidade de queima de caixa."""
    async with AsyncSession(async_engine) as session:
        # Month: June (30 days)
        # Reference: June 15 (16 days remaining: 30 - 15 + 1)
        ref_date = datetime.date(2026, 6, 15)
        
        # Setup DB limits: say fallback total is 500,000 cents
        # Setup DB transactions for June: 50,000 cents
        t1 = Transaction(description="A", amount_cents=50000, hash_signature="1", date=datetime.datetime(2026, 6, 10, tzinfo=datetime.timezone.utc))
        session.add(t1)
        await session.commit()
        
        # projected fixed expenses = 100,000 cents
        # Total budget = 600,000
        # Spent = 50,000
        # Fixed = 100,000
        # Remaining = 600,000 - 50,000 - 100,000 = 450,000
        # Days remaining = 16
        # Daily target = 450,000 / 16 = 28,125
        
        result = await calculate_burn_rate_velocity(
            session, 
            projected_fixed_expenses_cents=100000, 
            reference_date=ref_date
        )
        
        assert result["total_budget_cents"] == 600000
        assert result["total_spent_cents"] == 50000
        assert result["projected_fixed_expenses_cents"] == 100000
        assert result["remaining_budget_cents"] == 450000
        assert result["days_remaining"] == 16
        assert result["daily_target_cents"] == 28125

from unittest import mock

@pytest.mark.asyncio
async def test_get_current_month_spent_fallback_date(async_engine):
    """Verifica se a ausência de reference_date utiliza a data atual do sistema."""
    # Como não podemos prever a data do sistema facilmente, vamos apenas garantir 
    # que a função não falha ao ser chamada sem reference_date
    async with AsyncSession(async_engine) as session:
        spent = await get_current_month_spent(session)
        assert isinstance(spent, int)

@pytest.mark.asyncio
async def test_calculate_burn_rate_velocity_residual(async_engine):
    """Verifica se a divisão da meta diária trunca corretamente os resíduos."""
    async with AsyncSession(async_engine) as session:
        ref_date = datetime.date(2026, 6, 15)
        # 16 days remaining
        # total_budget = 600,000
        # Spent = 1, remaining = 599,999
        # 599999 // 16 = 37499
        t1 = Transaction(description="A", amount_cents=1, hash_signature="1", date=datetime.datetime(2026, 6, 10, tzinfo=datetime.timezone.utc))
        session.add(t1)
        await session.commit()
        
        result = await calculate_burn_rate_velocity(session, reference_date=ref_date)
        
        assert result["remaining_budget_cents"] == 599999
        assert result["days_remaining"] == 16
        assert result["daily_target_cents"] == 37499
