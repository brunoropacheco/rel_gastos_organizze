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
