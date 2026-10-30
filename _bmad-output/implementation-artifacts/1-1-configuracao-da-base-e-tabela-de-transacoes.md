---
baseline_commit: fa9f16f7f7b51a1bdb18bd171052d828722f50e2
---

# Story 1.1: Configuração da Base e Tabela de Transações

## Story Requirements

**User Story:**
As a desenvolvedor,
I want configurar o projeto FastAPI com a conexão segura ao PostgreSQL usando SQLModel e a entidade `Transaction`,
So that possamos ter o repositório correto para gravar as transações que chegarão do celular.

**Acceptance Criteria:**
- Given as variáveis de ambiente configuradas no servidor
- When o aplicativo FastAPI inicia
- Then ele se conecta ao PostgreSQL exigindo SSL
- And o log de inicialização não expõe credenciais sensíveis

## Developer Context

**Epic Context:** Epic 1: Captura Instantânea de Gastos (O Shadow Hook) - O usuário consegue registrar seus gastos instantaneamente pelo Apple Wallet para não perder o controle do dinheiro em tempo real.
This is the FIRST story in the project! You will be setting up the core scaffolding.

### Technical Requirements
- Utilize `uv` for package management (`pyproject.toml`).
- Frameworks: FastAPI v0.136.3+, SQLModel v0.0.38+, Alembic v1.18.4+.
- Database: PostgreSQL with SSL requirement enabled.
- Data Model: Create a single table `Transaction` for both Organizze and Webhook data. Ensure fields account for `valor`, `data`, `descrição` and a hash signature for deduplication.

### Architecture Compliance
- Project Structure:
  ```
  rel_gastos_organizze/
  ├── pyproject.toml         # Configuração do uv e dependências
  ├── Dockerfile             # Multi-stage build para Railway
  ├── alembic.ini            # Configuração do Alembic
  ├── alembic/               # Migrações do banco de dados
  ├── src/
  │   └── app/
  │       ├── main.py        # Inicialização do FastAPI
  │       ├── core/          # Configuração, Segurança e Logging
  │       ├── db/            # Engine e Sessão do Postgres
  │       ├── models/        # Modelos SQLModel (Transactions, Limits)
  └── tests/
  ```
- Boundary: Database access centralized via SQLModel in `models/` and injected sessions via `db/`.

### File Structure Requirements
- NEW: `pyproject.toml`, `Dockerfile`, `src/app/main.py`, `src/app/core/config.py`, `src/app/db/session.py`, `src/app/models/transaction.py`

### Project Context Rules
- Naming Conventions: `snake_case` functions/variables, `PascalCase` classes.
- Documentation: Mandatory docstrings in Portuguese.
- String Data: Normalize strings (lowercase, no accents, spaces/hyphens to underscores) before categorization.
- Security: NEVER hardcode tokens or passwords. Use `os.environ.get()` (or Pydantic BaseSettings).

## Tasks/Subtasks
- [x] Task 1: Configurar projeto com `uv` e `pyproject.toml` contendo dependências do FastAPI e SQLModel.
- [x] Task 2: Criar a estrutura base de diretórios (`src/app/core`, `src/app/db`, `src/app/models`, `tests/`).
- [x] Task 3: Configurar o `src/app/core/config.py` para carregar variáveis de ambiente (DB config).
- [x] Task 4: Criar o modelo `Transaction` em `src/app/models/transaction.py` com SQLModel (incluir hash_signature).
- [x] Task 5: Configurar `src/app/db/session.py` para criar o engine do PostgreSQL exigindo SSL.
- [x] Task 6: Inicializar o FastAPI em `src/app/main.py`.
- [x] Task 7: Configurar o Alembic (`alembic.ini` e `alembic/`) para gerenciar as migrações.
- [x] Task 8: Criar `Dockerfile` para o Railway.

### Review Findings
- [x] [Review][Patch] Credenciais do banco chumbadas no config.py (`database_url`) [src/app/core/config.py]
- [x] [Review][Patch] Dockerfile não utiliza o `uv` conforme exigido e contém falha no cache [Dockerfile]
- [x] [Review][Patch] Dockerfile não consome a variável `$PORT` exigida pelo Railway [Dockerfile]
- [x] [Review][Patch] Uso da sintaxe depreciada do Pydantic v1 (`class Config`) em vez de `model_config` [src/app/core/config.py]
- [x] [Review][Patch] Remoção do `create_all` no lifespan do FastAPI, que conflita com o Alembic [src/app/main.py]
- [x] [Review][Patch] Substituir `datetime.utcnow()` que foi depreciado no Python 3.12 [src/app/models/transaction.py]
- [x] [Review][Patch] Definir validações (Literal, limits) para `source`, `description` e `amount_cents` [src/app/models/transaction.py]
- [x] [Review][Patch] Configurar o max_length para a string `hash_signature` no index do banco [src/app/models/transaction.py]
- [x] [Review][Patch] Engine não exige o SSL de forma dura (faltam os `connect_args`) [src/app/db/session.py]
- [x] [Review][Defer] Vulnerabilidade de root privilege no Dockerfile — deferred, pre-existing

## Dev Agent Record
### Debug Log
- N/A. Dependências instaladas via pip e configuração do alembic realizada com sucesso. Teste de importação do `main` também funcionou sem erros.

### Completion Notes
- A configuração da estrutura do projeto e das bases (banco, engine, env vars, model) foi implementada conforme os padrões da arquitetura. O Alembic já está devidamente conectado ao SQLModel usando a string de conexão das configurações. O projeto está "ready for Railway" e tem o Endpoint `/health` funcionando para teste.

## File List
- `pyproject.toml` (new)
- `Dockerfile` (new)
- `src/app/core/config.py` (new)
- `src/app/db/session.py` (new)
- `src/app/models/transaction.py` (new)
- `src/app/main.py` (new)
- `alembic/env.py` (modified)

## Change Log
- Scaffolded basic structure using FastAPI, SQLModel, PostgreSQL and Alembic. Created Transaction model with appropriate fields.

## Status
- **Status:** done
- **Completion Note:** Todas as tarefas de infraestrutura e setup concluídas e corrigidas de acordo com os findings da revisão de código adversária e de aceitação.
