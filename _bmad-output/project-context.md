---
project_name: 'rel_gastos_organizze'
user_name: 'Bruno'
date: '2026-06-04'
sections_completed: ['technology_stack', 'language_rules', 'critical_rules', 'usage_guidelines']
status: 'complete'
rule_count: 15
optimized_for_llm: true
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- **Python:** 3.x
- **Data Manipulation:**
    - `pandas` (v2.2.3)
    - `numpy` (v2.2.4)
- **APIs & Integration:**
    - `google-api-python-client` (v2.194.0) - Google Drive v3, Google Sheets v4
    - `requests` (v2.32.3) - Organizze REST v2
    - `smtplib` (Native) - Email reporting
- **Utilities:**
    - `python-dateutil` (v2.9.0.post0)
    - `httpx` (v0.28.1)
    - `PyYAML` (v6.0.3)
- **Environment Management:**
    - `os.environ` for credentials and tokens.

## Critical Implementation Rules

### Language-Specific Rules (Python)

- **Naming Conventions:** Use `snake_case` for functions and variables. The project uses a hybrid naming scheme (English and Portuguese); maintain consistency with existing names in the same module.
- **Documentation:** **Mandatory** docstrings in Portuguese for all functions, detailing arguments and return values.
- **Data Formatting:** Use `f-strings` for string interpolation.
- **Character Normalization:** Always normalize strings (lowercase, remove accents, replace spaces/hyphens with underscores) before using them for categorization or comparison.

### Critical Don't-Miss Rules & Anti-Patterns

- **Credential Security:** NEVER hardcode tokens or passwords. Use `os.environ.get()` for `TOKEN_ORGANIZZE`, `PASSWORD_GMAIL`, and `GOOGLE_DRIVE_CREDENTIALS`.
- **Manual Installment Management:** Be aware that the Organizze API does not automatically move future installments. Logic affecting installments must document that manual movement in the Organizze app is required.
- **Data Filtering:**
    - Always filter out `deb._autom._de_fatura` from descriptions.
    - Ignore transactions marked with "ignorar" in the notes field (case-insensitive).
- **Fallback Logic:** If Google Sheets authentication or data retrieval fails, the system **must** use the hardcoded default limits dictionary.
- **Duplicate Handling:** When merging transaction data, remove duplicates based on `description`, `date`, and `amount_cents`, keeping the most recent entry.

---

## Usage Guidelines

**For AI Agents:**

- Read this file before implementing any code.
- Follow ALL rules exactly as documented.
- When in doubt, prefer the more restrictive option.
- Update this file if new patterns emerge.

**For Humans:**

- Keep this file lean and focused on agent needs.
- Update when technology stack changes.
- Review quarterly for outdated rules.
- Remove rules that become obvious over time.
### Novas Regras de Negócio (Descobertas em 27/06/2026)

- **Filtro de Cartões de Crédito:** A sincronização com o Organizze deve buscar EXCLUSIVAMENTE os lançamentos associados aos cartões de crédito monitorados (IDs `1840776` para Santander AA e `2423452` para Itaú Azul). Despesas de conta corrente, PIX, etc., são ignoradas.
- **Valores Absolutos:** Todas as despesas importadas do Organizze vêm com sinal negativo. O algoritmo deve convertê-las para valor absoluto (`abs()`) antes de qualquer soma ou subtração.
- **Estratégia de Sincronização de Faturas:** Para garantir a correta alocação de parcelas e transações movidas manualmente entre faturas, NÃO se deve usar o endpoint de `/transactions` filtrando pela data da compra original. Em vez disso, a sincronização deve:
    1. Buscar as **faturas** (`/invoices`) de cada cartão dentro de uma janela larga de tempo (ex: -90 dias a +60 dias).
    2. Filtrar a fatura correta correspondente ao ciclo de faturamento desejado.
    3. Extrair as transações listadas **dentro dessa fatura específica**, salvando no banco a `invoice_date` (data de vencimento da fatura).
- **Ciclo de Fechamento (Dia 10):** O fechamento padrão é o dia 10 de cada mês. As consultas de *Burn Rate* devem somar transações baseadas na fatura associada àquele mês (a `invoice_date`), e não pela data exata da compra.
- **Limites Hardcoded:** Como fallback primário (ou substituição ao Google Sheets caso não configurado), o sistema possui uma lista estática atualizada com 17 categorias de gastos (Alimentacao casa: 1200, Casa: 2500, Viagem: 2600, etc.) embutida na aplicação.
