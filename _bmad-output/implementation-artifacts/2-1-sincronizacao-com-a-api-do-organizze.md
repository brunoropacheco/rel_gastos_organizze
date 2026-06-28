---
baseline_commit: "6829ada2f16e8d31ff543b06b04a994bcc23071f"
---

# Story 2.1: Sincronização com a API do Organizze

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a rotina do sistema backend (`sync_service`),
I want consultar periodicamente a API REST do Organizze (v2) resgatando as faturas/transações atuais,
so that possamos ter na base os gastos manuais, parcelados e despesas fixas oficiais da plataforma.

## Acceptance Criteria

1. **Given** o `TOKEN_ORGANIZZE` configurado em variável de ambiente
   **When** a rotina de sincronização é disparada
   **Then** o sistema faz uma requisição HTTP segura à API v2 do Organizze
   **And** converte o payload retornado para uma estrutura compatível pronta para análise.

2. **Given** falha de rede ou rate-limit na API do Organizze
   **When** a rotina tentar rodar
   **Then** deve gerar um erro no log de forma graciosa sem travar o servidor (resiliência).

3. **Given** uma transação que contenha a palavra 'ignorar' no campo 'notes' ou 'deb._autom._de_fatura' na descrição
   **When** a transação for processada na sincronização
   **Then** ela deve ser sumariamente descartada ou marcada para não entrar nos cálculos.

4. **Given** uma transação que seja uma compra parcelada
   **When** for sincronizada
   **Then** o sistema deve registrar a parcela atual e o total de parcelas (`installment` e `total_installments`).

## Tasks / Subtasks

- [x] Task 1 (AC: 1): Adicionar `TOKEN_ORGANIZZE` às configurações (`src/app/core/config.py`).
- [x] Task 2 (AC: 1): Criar um serviço HTTP client seguro (HTTPS/TLS 1.2+) e tolerante a falhas (ex: uso do pacote `httpx`) em `src/app/services/organizze.py`.
- [x] Task 3 (AC: 1): Criar os Pydantic schemas necessários para fazer o parser do response da API do Organizze.
- [x] Task 4 (AC: 1, 2): Criar a rotina/função principal de sincronização que busca as transações.
- [x] Task 5 (AC: 2): Implementar tratamento de erros (try/except) lidando com falha de rede e HTTP 429 (Rate-Limit), com logs seguros.
- [x] Task 6: Escrever testes automatizados verificando o path feliz e os comportamentos de erro usando *mock* da requisição HTTP (ex: `respx` ou `pytest-httpx`).

## Dev Notes

- **API Organizze v2:** Use autenticação Basic com o email/token ou header de autenticação conforme doc oficial da v2.
- **Resiliência:** Utilize try-except para erros do `httpx` (`httpx.RequestError`, `httpx.HTTPStatusError`). Não crashar a aplicação.
- **Segurança:** Nunca printe (log) o Token nem valores sensíveis. Use as práticas de segurança em trânsito estabelecidas no Epic 1.

### Project Structure Notes

- New folder: `src/app/services/` for business/external integrations logic.
- Alignment with `Transaction` model: A conversão do payload do Organizze deve ser compatível para inserção ou atualização no nosso banco de dados.

### References

- [Epic 1 Lessons]: Mantenha o tratamento rígido de exceções (conforme fizemos no Commit do Webhook) e teste sem vazamento de estado global.

### Dev Agent Record

### Agent Model Used
Google DeepMind Advanced Agentic Coding

### Debug Log References
- pyproject.toml updated with `httpx` and `respx`
- Added fallback dummy variable for testing `.env`

### Completion Notes List
- All tasks implemented using TDD methodology (Red-Green-Refactor)
- Handled network errors and rate limits robustly
- 3 new tests passing correctly with `respx` mocking HTTP requests

### File List
- pyproject.toml
- src/app/core/config.py
- src/app/schemas/organizze.py (new)
- src/app/services/organizze.py (new)
- tests/core/test_config.py
- tests/services/test_organizze.py (new)

### Review Findings
- [x] [Review][Decision] Silent Failure on Sync Errors / Dropped on 429 — Should it raise an exception or is returning `[]` intended? Returning `[]` masks errors and prevents retry queues.
- [x] [Review][Patch] Missing test dependencies — `respx`, `pytest-asyncio` are missing from `pyproject.toml`. [pyproject.toml]
- [x] [Review][Patch] Environment & Config State Pollution — Tests mutate `os.environ` and `settings` globally. [tests/core/test_config.py]
- [x] [Review][Patch] Broken Basic Auth Implementation — Requires Base64 encoding for Basic Auth instead of raw token. [src/app/services/organizze.py]
- [x] [Review][Patch] Swallowed Exception Tracebacks — Use `logger.exception` instead of `logger.error` to preserve stack traces. [src/app/services/organizze.py]
- [x] [Review][Patch] Weak Testing of Acceptance Criteria — Tests mock but don't assert logger on failures. [tests/services/test_organizze.py]
- [x] [Review][Patch] Schema/Model Type Mismatch — `OrganizzeTransaction.date` is `str` instead of `datetime` preventing automatic insertion compatibility. [src/app/schemas/organizze.py]
- [x] [Review][Patch] Paginated response dropped — Organizze API pagination ignored, dropping subsequent pages. [src/app/services/organizze.py]
- [x] [Review][Defer] Fragile Hash Generation (Timezone Roulette) [src/app/api/webhooks.py] — deferred, pre-existing
- [x] [Review][Defer] Naive String Normalization / Delimiter collision [src/app/api/webhooks.py] — deferred, pre-existing
- [x] [Review][Defer] API Status Code Violation [src/app/api/webhooks.py] — deferred, pre-existing
- [x] [Review][Defer] Unhandled Concurrency Edge Case (500 Error Risk) [src/app/api/webhooks.py] — deferred, pre-existing
- [x] [Review][Defer] Config Empty String [src/app/core/config.py] — deferred, pre-existing
- [x] [Review][Defer] Inefficient HTTP Client Initialization [src/app/services/organizze.py] — deferred, architectural choice for cron-like jobs
- [x] [Review][Defer] Dead Code (Missing Sync Trigger) [src/app/services/organizze.py] — deferred, expected to be implemented in a subsequent epic/story
