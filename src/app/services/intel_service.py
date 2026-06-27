import datetime
import calendar
from typing import Dict
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from src.app.models.limit import CategoryLimit
from src.app.models.transaction import Transaction
import logging

logger = logging.getLogger(__name__)

# Fallback limits as a dictionary. Keys are category names, values are limits in cents.
FALLBACK_LIMITS: Dict[str, int] = {
    "alimentacao": 200000, # 2000.00
    "transporte": 50000,   # 500.00
    "lazer": 30000,        # 300.00
    "moradia": 300000,     # 3000.00
    "saude": 20000,        # 200.00
}

async def get_monthly_limits(session: AsyncSession) -> Dict[str, int]:
    """
    Busca os limites mensais configurados na tabela CategoryLimit.
    Caso não existam limites cadastrados, retorna um dicionário padrão de fallback.
    
    Args:
        session (AsyncSession): Sessão ativa do banco de dados (SQLModel)
        
    Returns:
        Dict[str, int]: Dicionário mapeando categorias (str) para valores limites em centavos (int)
    """
    try:
        result = await session.exec(select(CategoryLimit))
        limits = result.all()
        
        merged_limits = FALLBACK_LIMITS.copy()
        if limits:
            for limit in limits:
                merged_limits[limit.category] = limit.limit_cents
        else:
            logger.warning("Nenhum limite configurado encontrado. Utilizando fallback padrão.")
            
        return merged_limits
    except OperationalError as e:
        logger.exception("Erro de conexão ao buscar limites mensais do banco. Utilizando fallback padrão.")
        return FALLBACK_LIMITS.copy()

async def get_total_limits(session: AsyncSession) -> int:
    """Calcula o limite total somando os limites de todas as categorias."""
    limits = await get_monthly_limits(session)
    return sum((v or 0) for v in limits.values())

async def get_current_month_spent(session: AsyncSession, reference_date: datetime.date = None) -> int:
    """
    Busca todas as transações do mês atual e soma seus valores (amount_cents).
    Usa reference_date se fornecido, caso contrário usa a data atual (UTC).
    """
    if reference_date is None:
        reference_date = datetime.datetime.now(datetime.timezone.utc).date()
        
    start_of_month = datetime.datetime(reference_date.year, reference_date.month, 1, tzinfo=datetime.timezone.utc)
    _, last_day = calendar.monthrange(reference_date.year, reference_date.month)
    end_of_month = datetime.datetime(reference_date.year, reference_date.month, last_day, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc)
    
    try:
        statement = select(func.sum(Transaction.amount_cents)).where(
            Transaction.date >= start_of_month,
            Transaction.date <= end_of_month
        )
        result = await session.exec(statement)
        total = result.one_or_none()
        return total or 0
    except SQLAlchemyError as e:
        logger.exception("Erro de banco de dados ao buscar gastos do mês. Retornando 0.")
        return 0

async def calculate_burn_rate_velocity(
    session: AsyncSession, 
    projected_fixed_expenses_cents: int = 0,
    reference_date: datetime.date = None
) -> Dict[str, int]:
    """
    Calcula a velocidade de queima de caixa (Burn-Rate Velocity).
    Subtrai gastos realizados e gastos fixos do limite total,
    e divide pelos dias restantes no mês.
    """
    if reference_date is None:
        reference_date = datetime.datetime.now(datetime.timezone.utc).date()
        
    total_budget_cents = await get_total_limits(session)
    total_spent_cents = await get_current_month_spent(session, reference_date)
    
    remaining_budget = total_budget_cents - total_spent_cents - projected_fixed_expenses_cents
    
    _, last_day = calendar.monthrange(reference_date.year, reference_date.month)
    days_remaining = last_day - reference_date.day + 1
    
    if days_remaining <= 0:
        daily_target = remaining_budget
    else:
        daily_target = remaining_budget // days_remaining
        
    return {
        "total_budget_cents": total_budget_cents,
        "total_spent_cents": total_spent_cents,
        "projected_fixed_expenses_cents": projected_fixed_expenses_cents,
        "remaining_budget_cents": remaining_budget,
        "days_remaining": days_remaining,
        "daily_target_cents": daily_target
    }
