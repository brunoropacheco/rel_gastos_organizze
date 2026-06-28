import asyncio
import logging
import subprocess
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Session
from src.app.core.config import settings
from src.app.db.session import engine
from src.app.services.sync_service import run_sync_and_reconcile
from src.app.services.intel_service import calculate_burn_rate_velocity
from src.app.services.notify_service import format_telegram_message, send_telegram_message

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import sys

def run_migrations():
    logger.info("Executando migrações do banco de dados (Alembic)...")
    try:
        subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)
        logger.info("Migrações concluídas com sucesso.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar migrações: {e}")

async def run_jobs():
    logger.info("Iniciando rotina CRON de 7h/21h...")
    run_migrations()
    
    # 1. Run sync (Synchronous session for db, but awaits sync_transactions)
    logger.info("Executando sincronizacao do Organizze...")
    with Session(engine) as sync_session:
        await run_sync_and_reconcile(sync_session)
    logger.info("Sincronizacao finalizada.")
    
    # 2. Run intel & notify
    logger.info("Calculando Burn-Rate Velocity...")
    
    # As the intel service requires AsyncSession, we convert the sync URL to asyncpg
    async_db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    connect_args = {"ssl": "require"} if "postgres" in async_db_url else {}
    if "sqlite" in async_db_url:
        async_db_url = "sqlite+aiosqlite:///" + settings.database_url.split("///")[-1]
        
    async_engine = create_async_engine(async_db_url, connect_args=connect_args)
    
    try:
        async with AsyncSession(async_engine) as async_session:
            stats = await calculate_burn_rate_velocity(async_session)
            
        # 3. Format and send Telegram message
        logger.info("Enviando notificacao no Telegram...")
        msg = format_telegram_message(stats)
        success = await send_telegram_message(msg)
        
        if success:
            logger.info("Notificacao enviada com sucesso!")
        else:
            logger.error("Falha ao enviar notificacao via Telegram.")
            
    finally:
        await async_engine.dispose()
        
    logger.info("Rotina CRON finalizada.")

if __name__ == "__main__":
    asyncio.run(run_jobs())
