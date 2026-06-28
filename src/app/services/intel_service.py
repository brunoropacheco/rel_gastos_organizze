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
    "alimentacao_casa": 100000,
    "anuidade": 23600,
    "assinaturas": 44600,
    "beleza": 43000,
    "casa": 80000,
    "compras": 92000,
    "diversao-lazer": 57500,
    "diversao-comida": 75000,
    "delivery": 90000,
    "educacao": 260000,
    "marketing": 79900,
    "esporte": 0,
    "outros": 10000,
    "saude": 80500,
    "seguro_carro": 40300,
    "transp(ub+gas+vel+ccr)": 193000,
    "viagem": 250000
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

async def get_current_month_spent(session: AsyncSession, reference_date: datetime.date = None) -> dict:
    """
    Busca todas as transações do ciclo da fatura atual e soma seus valores (amount_cents).
    Também conta parcelamentos e compras na última parcela.
    O ciclo é definido pelo dia 10 (data de fechamento).
    """
    if reference_date is None:
        reference_date = datetime.datetime.now(datetime.timezone.utc).date()
        
    dia_limite = 10
    
    if reference_date.day <= dia_limite:
        end_date = datetime.datetime(reference_date.year, reference_date.month, dia_limite, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc)
        start_month = reference_date.month - 1
        start_year = reference_date.year
        if start_month < 1:
            start_month = 12
            start_year -= 1
        start_date = datetime.datetime(start_year, start_month, dia_limite + 1, tzinfo=datetime.timezone.utc)
    else:
        start_date = datetime.datetime(reference_date.year, reference_date.month, dia_limite + 1, tzinfo=datetime.timezone.utc)
        end_month = reference_date.month + 1
        end_year = reference_date.year
        if end_month > 12:
            end_month = 1
            end_year += 1
        end_date = datetime.datetime(end_year, end_month, dia_limite, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc)
    
    try:
        statement = select(Transaction).where(
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
        result = await session.exec(statement)
        transactions = result.all()
        
        total = sum(tx.amount_cents for tx in transactions)
        
        spent_by_category = {}
        qtde_parcelado = 0
        qtde_ultima_parcela = 0
        for tx in transactions:
            cat = tx.category_name or "outros"
            # Normalize to avoid case mismatch if needed (fallback keys are lowercase)
            cat = cat.lower()
            spent_by_category[cat] = spent_by_category.get(cat, 0) + tx.amount_cents
            
            if tx.total_installments and tx.total_installments > 1:
                qtde_parcelado += 1
                if tx.installment == tx.total_installments:
                    qtde_ultima_parcela += 1
                    
        return {
            "total": total,
            "spent_by_category": spent_by_category,
            "qtde_parcelado": qtde_parcelado,
            "qtde_ultima_parcela": qtde_ultima_parcela,
            "end_date": end_date
        }
    except SQLAlchemyError as e:
        logger.exception("Erro de banco de dados ao buscar gastos do mês.")
        return {"total": 0, "spent_by_category": {}, "qtde_parcelado": 0, "qtde_ultima_parcela": 0, "end_date": reference_date}

async def calculate_burn_rate_velocity(
    session: AsyncSession, 
    projected_fixed_expenses_cents: int = 0,
    reference_date: datetime.date = None
) -> dict:
    """
    Calcula a velocidade de queima de caixa (Burn-Rate Velocity).
    Subtrai gastos realizados e gastos fixos do limite total,
    e divide pelos dias restantes no mês (até o dia 10).
    """
    if reference_date is None:
        reference_date = datetime.datetime.now(datetime.timezone.utc).date()
        
    total_budget_cents = await get_total_limits(session)
    spent_data = await get_current_month_spent(session, reference_date)
    total_spent_cents = spent_data["total"]
    
    remaining_budget = total_budget_cents - total_spent_cents - projected_fixed_expenses_cents
    
    end_date = spent_data.get("end_date")
    if isinstance(end_date, datetime.datetime):
        end_date = end_date.date()
        
    days_remaining = (end_date - reference_date).days
    
    if days_remaining <= 0:
        daily_target = remaining_budget
    else:
        daily_target = remaining_budget // days_remaining
        
    monthly_limits = await get_monthly_limits(session)
    spent_by_category = spent_data.get("spent_by_category", {})
    categories_data = {}
    
    for cat, limit_cents in monthly_limits.items():
        if limit_cents == 0 and spent_by_category.get(cat, 0) == 0:
            continue # ignora categorias vazias que nao gastaram nada
            
        c_spent = spent_by_category.get(cat, 0)
        c_rem = limit_cents - c_spent
        categories_data[cat] = {
            "limit_cents": limit_cents,
            "spent_cents": c_spent,
            "remaining_cents": c_rem,
            "daily_target": c_rem // days_remaining if days_remaining > 0 else c_rem
        }
        
    return {
        "total_budget_cents": total_budget_cents,
        "total_spent_cents": total_spent_cents,
        "projected_fixed_expenses_cents": projected_fixed_expenses_cents,
        "remaining_budget_cents": remaining_budget,
        "days_remaining": days_remaining,
        "daily_target_cents": daily_target,
        "qtde_parcelado": spent_data["qtde_parcelado"],
        "qtde_ultima_parcela": spent_data["qtde_ultima_parcela"],
        "categories_data": categories_data
    }
