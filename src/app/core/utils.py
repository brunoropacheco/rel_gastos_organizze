import hashlib
from unidecode import unidecode
from datetime import datetime, timezone

def normalize_string(text: str) -> str:
    """
    Normaliza a string: remove acentos, substitui espaços e hífens por underscore,
    converte para minúsculas e remove espaços das pontas.
    """
    if not text:
        return ""
    clean = unidecode(text).strip().lower()
    # Utilizar apenas a primeira palavra para permitir match similar (ex: "Uber (limpo)" vs "Uber")
    first_word = clean.split()[0] if clean else ""
    return first_word.replace('-', '_').replace(' ', '_')

def normalize_date(date_obj: datetime) -> str:
    """
    Normaliza a data para string a fim de evitar a "Timezone Roulette".
    Converte para UTC e mantém o isoformat para não quebrar compatibilidade com registros antigos.
    """
    if not date_obj:
        return ""
    if date_obj.tzinfo:
        date_obj = date_obj.astimezone(timezone.utc)
    else:
        date_obj = date_obj.replace(tzinfo=timezone.utc)
    return date_obj.isoformat()

def generate_hash_signature(amount_cents: int, date_obj: datetime, description: str) -> str:
    """Gera o hash_signature com base em valor, data normalizada e descrição normalizada."""
    norm_desc = normalize_string(description)
    date_str = normalize_date(date_obj)
    raw = f"{amount_cents}|{date_str}|{norm_desc}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
