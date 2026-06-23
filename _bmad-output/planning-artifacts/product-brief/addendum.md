# Addendum - Detalhes Técnicos e Ideias de Futuro

## Ideias Descartadas / Em Espera
* **Interface Web:** Descartada inicialmente para manter o foco em notificações e baixo custo.
* **Múltiplos Usuários:** O sistema será focado em uma única conta Organizze para simplificar a lógica de tokens.

## Detalhes de Implementação (do Brainstorming)
* **Fallback de Canal:** Se o CallMeBot falhar, usar Telegram como redundância.
* **Cálculo de Probabilidade:** Usar média móvel simples de gastos diários por categoria para gerar o "Boletim de Probabilidade".
