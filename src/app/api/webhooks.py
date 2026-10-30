import hashlib
from sqlalchemy.exc import IntegrityError
from unidecode import unidecode
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from src.app.db.session import get_session
from src.app.core.security import verify_webhook_api_key
from src.app.schemas.transaction import TransactionCreate, TransactionResponse
from src.app.models.transaction import Transaction

router = APIRouter(
    prefix="/api/webhooks/transactions",
    tags=["Webhooks"],
    dependencies=[Depends(verify_webhook_api_key)]
)

from src.app.core.utils import generate_hash_signature

@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate, 
    session: Session = Depends(get_session)
):
    """
    Cria uma nova transação a partir do webhook.
    Realiza o cálculo de deduplicação antes da inserção.
    """
    # Calcula assinatura
    signature = generate_hash_signature(payload.amount_cents, payload.date, payload.description)
    
    # Verifica duplicidade no banco
    statement = select(Transaction).where(Transaction.hash_signature == signature)
    existing_tx = session.exec(statement).first()
    
    if existing_tx:
        # Já existe. Ignora mas retorna OK
        return existing_tx
        
    # Cria nova transação
    db_tx = Transaction(
        description=payload.description,
        amount_cents=payload.amount_cents,
        date=payload.date,
        source="webhook",
        hash_signature=signature
    )
    
    session.add(db_tx)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        # Se ocorreu IntegrityError no momento do commit, significa que houve inserção simultânea.
        # Recuperamos o registro recém-criado pela concorrência.
        existing_concurrent_tx = session.exec(select(Transaction).where(Transaction.hash_signature == signature)).first()
        if existing_concurrent_tx:
            return existing_concurrent_tx
    
    session.refresh(db_tx)
    
    return db_tx
