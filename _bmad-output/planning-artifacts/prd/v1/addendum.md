# Addendum - Detalhes Técnicos do PRD

## Estrutura Sugerida do Postgres (Rascunho)
* **Table: transactions** (id, date, amount, description, category, source[organizze/apple_wallet])
* **Table: categories_limits** (category_name, monthly_limit, alert_threshold)

## Detalhes do Webhook
* O endpoint deve ser protegido por uma API Key simples enviada no header pelo iOS para evitar spam.

## Lógica de Burn-down
* `Daily_Budget = (Limit - Spent_So_Far) / Days_Remaining`
