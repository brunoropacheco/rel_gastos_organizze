---
baseline_commit: "335b535dec869ae167ccc554e71a782cf44499f7"
---

# Story 3.1: Leitura de Metas e Limites

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a sistema backend (`intel_service`),
I want ler os limites mensais configurados na tabela do banco de dados (PostgreSQL),
so that eu possa ter a base de comparação (orçamento) para analisar os gastos atuais.

## Acceptance Criteria

1. **Given** o acesso ao banco de dados PostgreSQL
   **When** a lógica de inteligência iniciar a avaliação do mês
   **Then** deve buscar os valores das metas por categoria configurados na tabela `Limits`
   **And** se não encontrar limites configurados, deve utilizar um limite padrão (fallback) de segurança.

## Tasks / Subtasks

- [x] Task 1 (AC: 1): Criar o modelo SQLModel `Limits` (ou `CategoryLimit`) no arquivo `src/app/models/limit.py` mapeando as categorias para valores de limite mensal.
- [x] Task 2 (AC: 1): Adicionar o novo modelo aos imports de inicialização do banco (`src/app/models/__init__.py`) para que o Alembic possa rastrear.
- [x] Task 3 (AC: 1): Criar a função em `src/app/services/intel_service.py` (ex: `get_monthly_limits()`) para consultar a tabela de limites via sessão de banco de dados.
- [x] Task 4 (AC: 1): Implementar a lógica de fallback (limites padrão em dicionário) caso a tabela esteja vazia ou não tenha limites configurados.
- [x] Task 5 (AC: 1): Escrever testes unitários em `tests/services/test_intel_service.py` validando o retorno de limites do banco e o cenário de fallback, garantindo a resiliência.

## Dev Notes

### Arquitetura e Restrições Técnicas
- **Database:** PostgreSQL (SQLModel v0.0.38+).
- **Service Isolation:** A lógica de acesso deve ser encapsulada em `intel_service.py`, chamando a sessão injetada, preservando os limites de módulos.
- **Data Security:** Sempre utilizar conexões seguras, evitando hardcodes e fazendo uso de `os.environ` (verificado por `NFR-04`, `NFR-05` e `project-context.md`).
- **Limites Fallback:** "If Google Sheets authentication or data retrieval fails, the system must use the hardcoded default limits dictionary." (Adaptado para: se o PostgreSQL falhar ou não tiver dados, usar dicionário padrão).

### Project Structure Notes
- O novo model de limite deve ser salvo em `src/app/models/limit.py`.
- O novo serviço e sua lógica ficam em `src/app/services/intel_service.py`.
- Assegurar docstrings em Português para todas as funções adicionadas.
- Manter o padrão de naming `snake_case` para os nomes dos arquivos, métodos e propriedades. Modelos usam `PascalCase`.

### Previous Story Intelligence
- Na story anterior (Epic 2), a conciliação estabeleceu o padrão de usar sessões injetadas e mocks com SQLite in-memory para testes assíncronos. Seguir o mesmo padrão rigoroso de testes.
- Manter a abordagem de tratar possíveis erros de timeout, logando sem travar a aplicação, e ativando o fallback de forma graciosa.

### References
- [Source: `_bmad-output/planning-artifacts/epics.md#Story 3.1: Leitura de Metas e Limites`]
- [Source: `_bmad-output/planning-artifacts/architecture.md#Requirements to Structure Mapping`]
- [Source: `_bmad-output/project-context.md#Fallback Logic`]

## Dev Agent Record

### Agent Model Used
Gemini 3.1 Pro (High)

### Debug Log References
- Tests pass locally using SQLite memory DB: `pytest tests/services/test_intel_service.py` passed with 3 edge cases
- Full suite executed properly without regressions (19/19 tests passing).

### Completion Notes List
- ✅ Implemented `CategoryLimit` SQLModel successfully.
- ✅ Updated `src/app/models/__init__.py` to include `CategoryLimit`.
- ✅ Implemented `intel_service.py` with `get_monthly_limits()` using the requested fallback dictionary behavior.
- ✅ Added exception handling logic to safely utilize the fallback if an operational database error occurs.
- ✅ Tested DB success, empty DB fallback, and mocked error fallback.

### File List
- `src/app/models/limit.py`
- `src/app/models/__init__.py`
- `src/app/services/intel_service.py`
- `tests/services/test_intel_service.py`

### Review Findings

- [x] [Review][Patch] Mesclar categorias faltantes do banco com fallback [`src/app/services/intel_service.py:34`]
- [x] [Review][Patch] Especificar erro do banco em vez de usar Exception genérica [`src/app/services/intel_service.py:31`]
- [x] [Review][Patch] Adicionar validação para proibir limite negativo (`limit_cents`) [`src/app/models/limit.py:9`]
- [x] [Review][Patch] Normalizar chaves de categoria (lowercase, sem acento) [`src/app/models/limit.py:9`]
- [x] [Review][Patch] Preservar stack trace nos logs (`logger.exception`) [`src/app/services/intel_service.py`]
- [x] [Review][Patch] Remover export `Transaction` não relacionado [`src/app/models/__init__.py`]
- [x] [Review][Patch] Adicionar docstrings obrigatórias nas funções de teste [`tests/services/test_intel_service.py`]
- [x] [Review][Patch] Configurar `__tablename__ = "Limits"` no model [`src/app/models/limit.py`]
- [x] [Review][Patch] Refatorar para sessões assíncronas (`AsyncSession`, `async def`) [`src/app/services/intel_service.py`]
- [x] [Review][Defer] Suporte a Multi-Tenant / Contexto de Usuário — deferred, pre-existing
- [x] [Review][Defer] Substituir monkeypatch por `unittest.mock.patch.object` nos testes — deferred, pre-existing
- [x] [Review][Defer] Adicionar asserções de verificação de logs (observability) nos testes — deferred, pre-existing
