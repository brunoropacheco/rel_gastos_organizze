---
baseline_commit: "335b535dec869ae167ccc554e71a782cf44499f7"
---

# Story 2.2: Algoritmo de Conciliação e Deduplicação (Anti-Duplicidade)

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a rotina do sistema backend,
I want comparar cada transação vinda do Organizze contra as já existentes no banco de dados, usando uma assinatura hash (`valor` + `data` + `similaridade de descrição`),
so that os gastos que já foram recebidos instantaneamente pelo Apple Wallet não sejam salvos como duplicados.

## Acceptance Criteria

1. **Given** que chegou uma transação pela API do Organizze
   **When** existir no banco de dados um gasto via Apple Wallet do mesmo dia, com o exato mesmo valor e descrição similar
   **Then** o sistema não deve criar um novo registro, mas sim atualizar o registro existente para marcar que foi conciliado com o Organizze
   **And** priorizar manter o nome do estabelecimento do Webhook se for mais limpo.

2. **Given** uma transação que só existe no Organizze (ex: despesa recorrente)
   **When** passar pela lógica de sincronização
   **Then** um novo registro deve ser persistido no banco de dados com sucesso.

## Tasks / Subtasks

- [x] Task 1 (AC: 1, 2): Criar módulo/serviço `sync_engine.py` (ou dentro de `sync_service.py`) que receba a lista de `OrganizzeTransaction` vindas de `organizze.py`.
- [x] Task 2 (AC: 1): Implementar a lógica de geração de `hash_signature` para as transações vindas do Organizze para permitir a busca no banco. (Reaproveitar a lógica/modelo de `webhooks.py` se possível, ou abstrair para um `utils.py`).
- [x] Task 3 (AC: 1): Implementar a checagem no banco de dados: se existir hash equivalente, atualizar o campo `source` (ex: `webhook+organizze`) ou criar flag de conciliado; caso não exista, criar o registro.
- [x] Task 4 (AC: 1): Garantir que a descrição "limpa" do webhook seja preservada caso já exista no banco (não sobrescrever com a descrição "suja" do extrato, caso ocorra).
- [x] Task 5 (AC: 1, 2): Escrever testes unitários comprovando que (A) transações novas são salvas e (B) transações duplicadas (mesmo valor, mesma data, string similar) atualizam a original em vez de duplicar.

## Dev Notes

- **Architecture:** O serviço `sync_service.py` deve centralizar a orquestração: chama `organizze.sync_transactions()` e depois concilia com o banco.
- **Source Tree:** 
  - `src/app/services/sync_service.py` (New or refactored)
  - `src/app/models/transaction.py` (To update status/source if needed)
  - `src/app/api/webhooks.py` (Para extrair a função `generate_hash_signature` para um lugar comum, ex: `src/app/core/utils.py`).
- **Testing Standards:** Testes assíncronos via `pytest` validando o comportamento no banco (usar SQLite in-memory ou session mock).

### Project Structure Notes

- A função `generate_hash_signature` hoje reside em `src/app/api/webhooks.py`. Precisamos movê-la para um escopo global (`src/app/core/utils.py` ou dentro do próprio `Transaction` model) para que o Organizze sync também possa gerar hashes exatamente da mesma forma.

### Previous Story Intelligence

- **Learnings from 2.1:** A sincronização já puxa os dados do Organizze paginados, usando `httpx` e tratando o Rate-Limit com `SyncError`. Precisamos injetar essa lista de Pydantic Models na nossa lógica de conciliação.
- **Learnings from 1.2:** A `date` no Organizze pode vir com fuso diferente ou ser ingênua (naive), enquanto no webhook forçamos `isoformat()`. Cuidado com a "Timezone Roulette" (deferida anteriormente) - o hash_signature deve padronizar a data (ex: sempre truncar no dia ou usar data UTC estrita) para que os hashes coincidam.
- **Learnings from Review:** Normalização de strings (`normalize_string`) deve tratar melhor espaços/pontuações ou podemos manter a que já existe por enquanto, mas garantir que a função seja a mesma para ambos (Webhook e Organizze).

### References

- [Architecture Document]: Section `Data Architecture` - Hash signature (`valor + data + descrição`) para conciliação automática.
- [Epic 2]: Conciliação Automática.

## Dev Agent Record

### Agent Model Used

Google DeepMind Antigravity

### Debug Log References

- Tests run successfully: 16 passed
- Implemented `sync_service.py` with `run_sync_and_reconcile`.
- Refactored `generate_hash_signature` and `normalize_string` to `src/app/core/utils.py`.
- Updated `src/app/api/webhooks.py` to use `utils.py`.
- Added unit tests in `tests/services/test_sync_service.py` to cover new transactions and duplicate conciliations.

### Completion Notes List

- ✅ All tasks and subtasks complete.
- ✅ `generate_hash_signature` successfully generalized and logic reused.
- ✅ The deduplication strategy updates the `source` to `webhook+organizze` preserving the clean webhook description as prioritized.

### File List

- `src/app/core/utils.py` (new)
- `src/app/services/sync_service.py` (new)
- `src/app/api/webhooks.py` (modified)
- `tests/services/test_sync_service.py` (new)

### Review Findings

- [x] [Review][Decision] Legitimate identical transactions for the same day — Are legitimate identical transactions on the same day (e.g., two coffees of the exact same price) considered duplicates by the business rule, or should they both be allowed?
- [x] [Review][Patch] Hash generation enforces exact match instead of similar description [src/app/core/utils.py]
- [x] [Review][Patch] Hash generation format change breaks existing database records [src/app/core/utils.py]
- [x] [Review][Patch] Broken String Normalization (.replace before .strip) [src/app/core/utils.py]
- [x] [Review][Patch] Timezone standardization missing in normalize_date [src/app/core/utils.py]
- [x] [Review][Patch] Missing Rate Limit Error Handling for sync_transactions [src/app/services/sync_service.py]
- [x] [Review][Patch] Incomplete Source Update State Machine [src/app/services/sync_service.py]
- [x] [Review][Patch] Missing None check for date_obj in normalize_date [src/app/core/utils.py]
- [x] [Review][Defer] N+1 Query Problem in Sync Loop [src/app/services/sync_service.py] — deferred, pre-existing
- [x] [Review][Defer] All-or-Nothing Batch Commits [src/app/services/sync_service.py] — deferred, pre-existing
- [x] [Review][Defer] Concurrent webhook insertion (TOCTOU) [src/app/services/sync_service.py] — deferred, pre-existing
