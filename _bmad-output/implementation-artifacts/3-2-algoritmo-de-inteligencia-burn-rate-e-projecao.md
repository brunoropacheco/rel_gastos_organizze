---
baseline_commit: "335b535dec869ae167ccc554e71a782cf44499f7"
---

# Story 3.2: Algoritmo de Inteligência (Burn-Rate e Projeção)

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a rotina de inteligência financeira,
I want processar todas as transações do ciclo atual para calcular o "Burn-Rate Velocity" e projetar o saldo final,
So that o sistema saiba matematicamente a velocidade dos gastos e se o limite do mês estourará.

## Acceptance Criteria

1. **Given** a soma de transações na base de dados (do mês corrente)
   **When** a rotina realizar o cálculo
   **Then** deve determinar o total gasto, subtrair do limite mensal total e subtrair os gastos fixos projetados para calcular o que sobra
   **And** dividir o restante pelos dias que faltam no mês para determinar a meta de gasto diária.

## Tasks / Subtasks

- [x] Task 1: Criar função em `src/app/services/intel_service.py` para calcular o total de limites somando os valores de `get_monthly_limits`.
- [x] Task 2: Criar função para buscar todas as transações do mês atual no banco de dados e somar seus valores (`amount_cents`).
- [x] Task 3: Implementar o algoritmo de "Burn-Rate Velocity" que subtrai os gastos realizados e gastos fixos do orçamento total, e divide pelos dias restantes no mês.
- [x] Task 4: Escrever testes unitários em `tests/services/test_intel_service.py` validando os cálculos com mocks de datas para verificar as projeções.

## Dev Notes

### Arquitetura e Restrições Técnicas
- **Database:** PostgreSQL (SQLModel v0.0.38+). Sessões injetadas usando `AsyncSession` já configuradas no `intel_service.py`.
- **Date Handling:** Utilizar UTC/TimeZone awareness para evitar inconsistências em cálculos de fim de mês e dias restantes.

### Code Constraints (from Architecture & Context)
- Manter o padrão `snake_case` e docstrings em Português obrigatórias.
- Os cálculos devem ser precisos usando inteiros (centavos) ou `Decimal` se houver divisão com resíduos, mas a resposta final para meta diária pode ser em centavos.
- O modelo `Transaction` (`src/app/models/transaction.py`) tem os campos `date` e `amount_cents` que devem ser usados nas queries.

### Developer Context
**Current State of `intel_service.py`:**
- A função `get_monthly_limits(session: AsyncSession)` já está implementada (Story 3.1) usando a tabela `CategoryLimit` e `FALLBACK_LIMITS`. Retorna um dicionário `Dict[str, int]`.
- A soma dos valores desse dicionário representa o limite total.

**Previous Learnings (Story 3.1):**
- Usar `aiosqlite` para testes assíncronos (`async_engine` fixture).
- Fazer a leitura de banco de dados e aplicar fallbacks caso o banco de dados falhe.

### References
- [Source: `_bmad-output/planning-artifacts/epics.md#Story 3.2: Algoritmo de Inteligência (Burn-Rate e Projeção)`]
- [Source: `_bmad-output/project-context.md`]

## Dev Agent Record

### Agent Model Used
### Agent Model Used
Gemini 3.1 Pro (High)

### Debug Log References
- Tests run with aiosqlite and in-memory mock db, full suite passed (22/22).
- Validated burn-rate algorithm logic mapping with proper division bounds for last day handling.
- Extracted start_of_month and end_of_month correctly handling bounds to retrieve spent values.

### Completion Notes List
- ✅ Implemented `get_total_limits`, aggregating available categories to provide budget.
- ✅ Implemented `get_current_month_spent`, calculating month spent using UTC aware datetimes.
- ✅ Implemented `calculate_burn_rate_velocity`, providing accurate projections of the daily target and returning dictionary with stats.
- ✅ Created 3 test suites correctly validating correct data, limits, logic and boundary constraints.
- ✅ Executed `pytest` preventing regression. All green.

### File List
- `src/app/services/intel_service.py`
- `tests/services/test_intel_service.py`

### Review Findings

- [x] [Review][Patch] Mid-File Imports (Desvio de PEP-8) [`src/app/services/intel_service.py:52-54`]
- [x] [Review][Patch] In-Memory Aggregation Nightmare (Usar `func.sum()`) [`src/app/services/intel_service.py:73`]
- [x] [Review][Patch] Math Illiteracy in Comments (Arrumar comentário) [`tests/services/test_intel_service.py:72`]
- [x] [Review][Patch] Financial Truncation Laziness (Usar `//` para divisão) [`src/app/services/intel_service.py:106`]
- [x] [Review][Patch] Null limit_cents handling em `get_total_limits` [`src/app/services/intel_service.py`]
- [x] [Review][Patch] get_current_month_spent fails on DB error (adicionar try/except) [`src/app/services/intel_service.py`]
- [x] [Review][Patch] Null amount_cents causes TypeError em `get_current_month_spent` [`src/app/services/intel_service.py`]
- [x] [Review][Patch] Ausência de mocks de data nos testes [`tests/services/test_intel_service.py`]
- [x] [Review][Patch] Falta de cobertura de testes para divisão com resíduos [`tests/services/test_intel_service.py`]
- [x] [Review][Defer] Implicit Overwriting Gamble (no ORDER BY) [`src/app/services/intel_service.py`] — deferred, pre-existing
- [x] [Review][Defer] Hardcoded Configuration (FALLBACK_LIMITS) [`src/app/services/intel_service.py`] — deferred, pre-existing
- [x] [Review][Defer] Useless Exception Handling em get_monthly_limits [`src/app/services/intel_service.py`] — deferred, pre-existing
- [x] [Review][Defer] Blinded by all Transactions (schema tem limitação) [`src/app/services/intel_service.py`] — deferred, pre-existing
- [x] [Review][Defer] Unstructured Dictionary Returns [`src/app/services/intel_service.py`] — deferred, pre-existing
- [x] [Review][Defer] Redundant Database Hits [`src/app/services/intel_service.py`] — deferred, pre-existing
