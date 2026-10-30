---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - _bmad-output/planning-artifacts/prd/v1/prd.md
  - _bmad-output/planning-artifacts/prd/v1/addendum.md
  - _bmad-output/planning-artifacts/prd/v1/.decision-log.md
  - _bmad-output/planning-artifacts/product-brief/brief.md
  - _bmad-output/planning-artifacts/product-brief/addendum.md
  - _bmad-output/project-context.md
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-06-13'
project_name: 'rel_gastos_organizze'
user_name: 'Bruno'
date: '2026-06-13'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
O sistema deve atuar como um "Shadow Hook" para gastos instantâneos (Apple Wallet) e um "Navigator" para relatórios preditivos. A arquitetura deve suportar ingestão via Webhook, sincronização periódica via API (Organizze) e processamento de inteligência financeira (Burn-rate).

**Non-Functional Requirements:**
Disponibilidade 24/7 é crítica para o Webhook. Segurança é mandatória: HTTPS, API Key no Webhook, SSL no Postgres e gestão rigorosa de variáveis de ambiente.

**Scale & Complexity:**
- Primary domain: Python Backend / Integration
- Complexity level: Medium (Real-time sync + Data Deduplication)
- Estimated architectural components: 4 (Webhook Receiver, Sync Engine, Intel Engine, Notification Dispatcher)

### Technical Constraints & Dependencies
- Python 3.x com Pandas/Numpy.
- PostgreSQL para persistência.
- APIs Externas: Organizze (v2), CallMeBot (Telegram).
- iOS Shortcuts como gatilho de entrada.

### Cross-Cutting Concerns Identified
- **Deduplicação de Dados:** Conciliação entre transações "instantâneas" e "oficiais".
- **Observabilidade:** Logs anônimos para depuração de falhas na sincronização.
- **Resiliência:** Tratamento de rate-limits da API do Organizze.

## Starter Template Evaluation

### Primary Technology Domain
**API / Backend de Integração** focado em processamento de dados financeiros e Webhooks.

### Starter Options Considered
1. **Full-Stack FastAPI Template:** Descartado por incluir Frontend (React/Vite) desnecessário para este projeto.
2. **FastAPI Production Starter v2:** Excelente, mas focado em SQLAlchemy puro.
3. **Custom SQLModel Starter (Selecionado):** Uma base enxuta que utiliza SQLModel para ORM e `uv` para gestão de pacotes, ideal para Railway.

### Selected Starter: FastAPI + SQLModel + Docker (Railway Optimized)

**Rationale for Selection:**
- **ORM:** SQLModel simplifica a gestão do banco PostgreSQL unificando modelos de dados e validação.
- **Deploy:** Railway detecta o `Dockerfile` automaticamente.
- **Performance:** Uso do gerenciador `uv` para builds ultra-rápidos e Python 3.12+.

## Core Architectural Decisions

### Data Architecture
- **Database:** PostgreSQL (latest stable).
- **ORM:** SQLModel v0.0.38+.
- **Migrations:** Alembic v1.18.4+.
- **Model Strategy:** Tabela única `Transaction` consolidando dados do Organizze e Webhooks.
- **Deduplication:** Hash signature (`valor + data + descrição`) para conciliação automática.

### Authentication & Security
- **Webhook Auth:** Header `X-API-Key` validado via dependência do FastAPI.
- **Secrets Management:** Variáveis de ambiente injetadas pelo Railway.
- **Encryption:** Conexões SSL obrigatórias para Postgres e HTTPS/TLS 1.2+.

### API & Communication Patterns
- **Framework:** FastAPI v0.136.3+.
- **Pattern:** REST para recepção de webhooks e trigger de relatórios.
- **Dispatch:** Síncrono para Telegram (CallMeBot) integrado ao fluxo.

## Implementation Patterns & Consistency Rules

### Naming Patterns
- Tabelas: `snake_case` (plural).
- Colunas/Funções/Variáveis: `snake_case`.
- Classes: `PascalCase`.

### Format Patterns
- API Response: `{"status": "success/error", "data/message": ...}`.
- Datas: ISO 8601 strings.
- Moeda: Float (exibição) / Inteiro (centavos - opcional para cálculos).

### Process Patterns
- Docstrings em Português obrigatórias (conforme `project-context.md`).
- Testes unitários para toda nova lógica de `Service`.

## Project Structure & Boundaries

### Complete Project Directory Structure

```text
rel_gastos_organizze/
├── pyproject.toml         # Configuração do uv e dependências
├── Dockerfile             # Multi-stage build para Railway
├── alembic.ini            # Configuração do Alembic
├── alembic/               # Migrações do banco de dados
├── src/
│   └── app/
│       ├── main.py        # Inicialização do FastAPI
│       ├── api/           # Rotas da API (webhooks, reports)
│       ├── core/          # Configuração, Segurança e Logging
│       ├── db/            # Engine e Sessão do Postgres
│       ├── models/        # Modelos SQLModel (Transactions, Limits)
│       ├── schemas/       # Schemas Pydantic para APIs
│       └── services/      # Lógica de Negócio (Sync, Intel, Notify)
└── tests/                 # Testes Automatizados
```

### Architectural Boundaries
- **API Boundary:** Webhooks isolados em `api/webhooks/` com validação de esquema Pydantic.
- **Service Boundary:** A lógica de conciliação é isolada em `services/sync_service.py`, protegendo a API de detalhes da API do Organizze.
- **Data Boundary:** Todo acesso ao Postgres centralizado via SQLModel em `models/` e sessões injetadas via `db/`.

### Requirements to Structure Mapping
- **FR-01/03 (Webhook iOS):** `app/api/webhooks/`
- **FR-02/04 (Conciliação):** `app/services/sync_service.py`
- **FR-05/06/07 (Burn-rate):** `app/services/intel_service.py`
- **FR-08/09 (Persistência):** `app/models/`

## Architecture Validation Results

### Coherence Validation ✅
Todas as tecnologias escolhidas (Python 3.12, FastAPI, SQLModel) pertencem ao mesmo ecossistema moderno, garantindo compatibilidade total e alto desempenho.

### Requirements Coverage Validation ✅
- **Funcional:** Cobertura total via Services especializados (Sync, Intel, Notify).
- **Não-Funcional:** Segurança e Disponibilidade garantidas pela arquitetura de Webhook e infraestrutura do Railway.

### Implementation Readiness Validation ✅
- **Status:** READY FOR IMPLEMENTATION
- **Confiança:** Alta
- **Pontos Fortes:** Separação de responsabilidades (Modularidade) e estratégia robusta de deduplicação de dados financeiros.

### Architecture Completeness Checklist
- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped
- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance considerations addressed
- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented
- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Implementation Handoff
**AI Agent Guidelines:**
- Priorizar a implementação do `models/transaction.py` e o `SyncService`.
- Todas as mensagens para o usuário (Telegram) devem seguir o tom definido no PRD.
- Seguir rigorosamente o padrão de docstrings em Português.

**First Implementation Priority:**
Inicializar o projeto usando a estrutura modular definida no Step 6 e configurar o `pyproject.toml` com as versões especificadas.
