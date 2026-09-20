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
        # Pular ignorados e que não são dos dois cartões de crédito rastreados
        valid_cards = [1840776, 2423452] # IDs do Cartao_Santander_AA e Cartao_Itau_Azul
        if org_tx.credit_card_id not in valid_cards:
            continue
            
        if org_tx.notes and "ignorar" in org_tx.notes.lower():
            continue
        if "deb._autom._de_fatura" in org_tx.description.lower():
            continue
            
        # org_tx.date is datetime
        signature = generate_hash_signature(org_tx.amount_cents, org_tx.date, org_tx.description)
        
        statement = select(Transaction).where(Transaction.hash_signature == signature)
        existing_tx = session.exec(statement).first()
        
        if not existing_tx and org_tx.amount_cents < 0:
            # Fallback para o hash antigo (sem abs) caso a transação já exista no banco
            from src.app.core.utils import normalize_string, normalize_date
            import hashlib
            norm_desc = normalize_string(org_tx.description)
            date_str = normalize_date(org_tx.date)
            old_raw = f"{org_tx.amount_cents}|{date_str}|{norm_desc}"
            old_signature = hashlib.sha256(old_raw.encode("utf-8")).hexdigest()
            existing_tx = session.exec(select(Transaction).where(Transaction.hash_signature == old_signature)).first()
            
            if existing_tx:
                # Atualiza para o hash correto (novo) para arrumar a base aos poucos
                existing_tx.hash_signature = signature
        
        if existing_tx:
            # Conciliação: Atualizar source se for diferente ou combinar
            if "organizze" not in existing_tx.source:
                existing_tx.source = existing_tx.source + "+organizze"
                
                # Preencher dados ricos que vêm do Organizze e o webhook não tinha
                existing_tx.invoice_date = org_tx.invoice_date
                existing_tx.installment = org_tx.installment
                existing_tx.total_installments = org_tx.total_installments
                existing_tx.credit_card_id = org_tx.credit_card_id
                
                cat_name = category_map.get(org_tx.category_id, "outros") if org_tx.category_id else "outros"
                existing_tx.category_name = cat_name
                
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
                credit_card_id=org_tx.credit_card_id,
                invoice_date=org_tx.invoice_date,
                category_name=cat_name
            )
            session.add(new_tx)
            
    session.commit()
