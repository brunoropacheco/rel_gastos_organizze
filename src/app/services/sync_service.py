import logging
from sqlmodel import Session, select
from src.app.services.organizze import sync_transactions, sync_categories, SyncError
from src.app.core.utils import generate_hash_signature
from src.app.models.transaction import Transaction

logger = logging.getLogger(__name__)

async def run_sync_and_reconcile(session: Session):
    """
    Busca transações do Organizze e concilia com o banco de dados.
    """
    try:
        organizze_txs = await sync_transactions()
        category_map = await sync_categories()
    except SyncError as e:
        logger.error(f"Failed to sync transactions from Organizze: {e}")
        return
    
    for org_tx in organizze_txs:
        # Pular ignorados
        if org_tx.notes and "ignorar" in org_tx.notes.lower():
            continue
        if "deb._autom._de_fatura" in org_tx.description.lower():
            continue
            
        # org_tx.date is datetime
        signature = generate_hash_signature(org_tx.amount_cents, org_tx.date, org_tx.description)
        
        statement = select(Transaction).where(Transaction.hash_signature == signature)
        existing_tx = session.exec(statement).first()
        
        if existing_tx:
            # Conciliação: Atualizar source se for diferente ou combinar
            if "organizze" not in existing_tx.source:
                existing_tx.source = existing_tx.source + "+organizze"
                session.add(existing_tx)
            # Garantir que a descrição do webhook (se existir) seja mantida. 
            # A instrução diz "priorizar a descrição do webhook". Como já está no banco, não sobrescrevemos.
        else:
            # Não existe, criar novo
            cat_name = category_map.get(org_tx.category_id, "outros") if org_tx.category_id else "outros"
            
            new_tx = Transaction(
                description=org_tx.description,
                amount_cents=org_tx.amount_cents,
                date=org_tx.date,
                source="organizze",
                hash_signature=signature,
                installment=org_tx.installment,
                total_installments=org_tx.total_installments,
                category_name=cat_name
            )
            session.add(new_tx)
            
    session.commit()
