## Deferred from: code review (1-1-configuracao-da-base-e-tabela-de-transacoes.md)
- Vulnerabilidade de root privilege no Dockerfile — deferred, pre-existing

## Deferred from: code review 2-1-sincronizacao-com-a-api-do-organizze.md (2026-06-23)
- Fragile Hash Generation (Timezone Roulette) [src/app/api/webhooks.py] — deferred, pre-existing from 1.2
- Naive String Normalization / Delimiter collision [src/app/api/webhooks.py] — deferred, pre-existing from 1.2
- API Status Code Violation [src/app/api/webhooks.py] — deferred, pre-existing from 1.2
- Unhandled Concurrency Edge Case (500 Error Risk) [src/app/api/webhooks.py] — deferred, pre-existing from 1.2
- Config Empty String [src/app/core/config.py] — deferred, pre-existing from 1.2
- Inefficient HTTP Client Initialization [src/app/services/organizze.py] — deferred, architectural choice for cron-like jobs
- Dead Code (Missing Sync Trigger) [src/app/services/organizze.py] — deferred, expected to be implemented in a subsequent epic/story

## Deferred from: code review 2-2-algoritmo-de-conciliacao-e-deduplicacao-anti-duplicidade.md (2026-06-23)
- N+1 Query Problem in Sync Loop [src/app/services/sync_service.py] — deferred, pre-existing
- All-or-Nothing Batch Commits [src/app/services/sync_service.py] — deferred, pre-existing
- Concurrent webhook insertion (TOCTOU) [src/app/services/sync_service.py] — deferred, pre-existing

## Deferred from: code review 3-1-leitura-de-metas-e-limites.md (2026-06-25)
- Suporte a Multi-Tenant / Contexto de Usuário
- Substituir monkeypatch por `unittest.mock.patch.object` nos testes
- Adicionar asserções de verificação de logs (observability) nos testes

## Deferred from: code review 3-2-algoritmo-de-inteligencia-burn-rate-e-projecao.md (2026-06-25)
- Implicit Overwriting Gamble (no ORDER BY) [src/app/services/intel_service.py] — deferred, pre-existing
- Hardcoded Configuration (FALLBACK_LIMITS) [src/app/services/intel_service.py] — deferred, pre-existing
- Useless Exception Handling em get_monthly_limits [src/app/services/intel_service.py] — deferred, pre-existing
- Blinded by all Transactions (schema tem limitação) [src/app/services/intel_service.py] — deferred, pre-existing
- Unstructured Dictionary Returns [src/app/services/intel_service.py] — deferred, pre-existing
- Redundant Database Hits [src/app/services/intel_service.py] — deferred, pre-existing

## Deferred from: code review (3-3-grafico-textual-e-disparo-via-telegram.md)
- Inefficient Connection Thrashing (creating new AsyncClient per message).
- Redundant Function Reallocation (`cents_to_brl` inside format function).
- Inadequate Test Coverage for edge cases (negative currency, alerts, HTTPStatusError branches).
