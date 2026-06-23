---
baseline_commit: ""
---
# Story 1.2: Criação do Webhook Autenticado (API iOS)

## Story Requirements

**User Story:**
As a integração do iOS (Atalhos da Apple Wallet),
I want realizar um POST com os dados da transação para a rota `/api/webhooks/transactions`,
So that o gasto instantâneo seja gravado no banco de dados no momento da compra.

**Acceptance Criteria:**
- Given um payload com os dados financeiros (valor, data, estabelecimento)
- When a automação do iOS envia uma requisição POST com header `X-API-Key` correto
- Then o sistema salva com sucesso na tabela `Transaction`
- And retorna status HTTP adequado para o iOS saber que deu certo

- Given uma requisição sem a chave da API correta no Header
- When o envio é feito
- Then a API rejeita com status 401 ou 403

## Developer Context

**Epic Context:** Epic 1: Captura Instantânea de Gastos (O Shadow Hook) - O usuário consegue registrar seus gastos instantaneamente pelo Apple Wallet para não perder o controle do dinheiro em tempo real.
This story exposes the `/api/webhooks/transactions` endpoint over FastAPI to consume the JSON payload from the Apple Wallet automation.

### Technical Requirements
- Utilize `FastAPI` APIRouter for route grouping (e.g. `src/app/api/webhooks.py`).
- Read API Key from environment via `src/app/core/config.py` (e.g., `WEBHOOK_API_KEY`).
- Implement FastAPI `Depends` (Dependency Injection) to validate the `X-API-Key` header.
- Pydantic models for incoming JSON payload (e.g. `src/app/schemas/transaction.py`).
- Save the transaction to PostgreSQL using the `Transaction` SQLModel and `Session` injected from `src/app/db/session.py`.
- Deduplication hash (`hash_signature`): Calculate a unique hash using `hashlib.sha256` or similar based on `amount_cents`, `date`, and `description` string similarity before saving. If duplicate, handle gracefully (e.g., update or ignore, returning success to the iOS client so it doesn't loop).

### Architecture Compliance
- Project Structure Boundaries:
  - Rotas devem ficar em `src/app/api/`
  - Dependências de auth devem ficar em `src/app/core/security.py` ou na própria rota se for simples
  - Pydantic models (Input/Output schemas) devem ficar em `src/app/schemas/`
  - Toda chamada de banco usa SQLModel.
- Authentication: Token in Header `X-API-Key`.
- Security: NEVER log the actual API key. Don't log sensitive amounts in raw debug logs if possible.

### File Structure Requirements
- NEW: `src/app/api/webhooks.py`, `src/app/schemas/transaction.py`, `src/app/core/security.py`
- UPDATE: `src/app/main.py` (to include the new router), `src/app/core/config.py` (to add `WEBHOOK_API_KEY`)

### Project Context Rules
- Naming Conventions: `snake_case` functions/variables, `PascalCase` classes.
- Documentation: Mandatory docstrings in Portuguese.
- String Data: Normalize strings (lowercase, no accents, spaces/hyphens to underscores) before categorization.

## Tasks/Subtasks
- [ ] Task 1: Adicionar `WEBHOOK_API_KEY` ao `src/app/core/config.py`.
- [ ] Task 2: Criar Pydantic schema `TransactionCreate` e `TransactionResponse` em `src/app/schemas/transaction.py`.
- [ ] Task 3: Criar a função de validação de autenticação do header `X-API-Key` em `src/app/core/security.py` usando `fastapi.security.APIKeyHeader`.
- [ ] Task 4: Implementar o endpoint `POST /api/webhooks/transactions` no roteador `src/app/api/webhooks.py`, recebendo o schema e a injeção do BD.
- [ ] Task 5: Implementar a lógica de cálculo do `hash_signature` usando valor, data e descrição.
- [ ] Task 6: Implementar a lógica de salvamento e tratamento de violação de duplicidade (IntegrityError ou select prévio).
- [ ] Task 7: Registrar o roteador de webhooks no `src/app/main.py`.

## Dev Agent Record
### Debug Log
- 

### Completion Notes
- 

## File List
- 

## Change Log
- 

## Status
- **Status:** ready-for-dev
- **Completion Note:** Ultimate context engine analysis completed - comprehensive developer guide created.
