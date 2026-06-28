import logging
import urllib.parse
from typing import Dict
import httpx
from src.app.core.config import settings

logger = logging.getLogger(__name__)

def format_telegram_message(stats: Dict[str, int]) -> str:
    """
    Formata as estatísticas financeiras em uma mensagem textual legível com emojis
    para envio via Telegram.
    
    Args:
        stats (Dict[str, int]): Dicionário com dados do intel_service
        
    Returns:
        str: Mensagem formatada
    """
    def cents_to_brl(cents: int) -> str:
        # Lidar com negativos
        is_negative = cents < 0
        abs_cents = abs(cents)
        reais = abs_cents // 100
        centavos = abs_cents % 100
        # Formatação simplificada (ex: 3.000,00)
        reais_str = f"{reais:,}".replace(",", ".")
        val = f"R$ {reais_str},{centavos:02d}"
        return f"-{val}" if is_negative else val

    t_budget = stats.get('total_budget_cents', 0)
    t_spent = stats.get('total_spent_cents', 0)
    fixed = stats.get('projected_fixed_expenses_cents', 0)
    rem = stats.get('remaining_budget_cents', 0)
    days = stats.get('days_remaining', 0)
    target = stats.get('daily_target_cents', 0)
    
    pct = 0.0
    if t_budget > 0:
        pct = min(1.0, max(0.0, t_spent / t_budget))
    bar_len = 10
    filled = int(bar_len * pct)
    bar = "█" * filled + "░" * (bar_len - filled)
    
    msg = (
        "📊 *Relatório Burn-down Diário* 📊\n"
        "\n"
        f"Progresso: [{bar}] {int(pct * 100)}%\n"
        f"💰 Orçamento Total: {cents_to_brl(t_budget)}\n"
        f"💸 Total Gasto: {cents_to_brl(t_spent)}\n"
        f"📉 Gastos Fixos Proj.: {cents_to_brl(fixed)}\n"
        f"💵 Saldo Restante: {cents_to_brl(rem)}\n"
        "\n"
        f"⏳ Dias Restantes: {days}\n"
        f"🎯 Meta Diária: {cents_to_brl(target)}\n"
        "\n"
        f"💳 Transações Parceladas: {stats.get('qtde_parcelado', 0)}\n"
        f"✅ Na última parcela: {stats.get('qtde_ultima_parcela', 0)}\n"
    )
    
    if rem < 0:
        msg += "\n🚨 *ALERTA:* Você ultrapassou o orçamento!"
    elif target < 0:
        msg += "\n⚠️ *CUIDADO:* Meta diária negativa."
    else:
        msg += "\n🔥 Mantenha o foco!"
        
    return msg

async def send_telegram_message(text: str) -> bool:
    """
    Envia uma mensagem via CallMeBot API (Telegram).
    
    Args:
        text (str): Texto da mensagem
        
    Returns:
        bool: True se sucesso, False caso contrário
    """
    if not text:
        logger.error("Tentativa de enviar mensagem vazia.")
        return False

    user_alias = settings.callmebot_user
    
    if not user_alias:
        logger.error("Credencial (usuário) do CallMeBot ausente.")
        return False
        
    # URL encode user and text
    encoded_user = urllib.parse.quote(user_alias)
    encoded_text = urllib.parse.quote(text)
    url = f"https://api.callmebot.com/text.php?user={encoded_user}&text={encoded_text}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            
            if "error" in response.text.lower():
                logger.error("CallMeBot retornou 200 OK mas reportou um erro no payload.")
                return False
                
            logger.info("Mensagem Telegram enviada com sucesso.")
            return True
    except httpx.RequestError as exc:
        # Censure sensitive data in the log
        safe_url = str(exc.request.url).replace(encoded_user, "[REDACTED]").replace(user_alias, "[REDACTED]")
        logger.error(f"Falha de conexão ao enviar Telegram: Falha ao acessar {safe_url}")
        return False
    except httpx.HTTPStatusError as exc:
        safe_url = str(exc.request.url).replace(encoded_user, "[REDACTED]").replace(user_alias, "[REDACTED]")
        logger.error(f"Erro HTTP {exc.response.status_code} ao enviar Telegram para {safe_url}")
        return False
    except Exception as exc:
        # logger.error without exc_info=True prevents traceback data leak
        logger.error("Erro inesperado ao enviar Telegram (dados censurados).")
        return False
