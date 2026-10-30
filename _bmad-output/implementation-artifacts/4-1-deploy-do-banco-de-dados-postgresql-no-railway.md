---
baseline_commit: "latest"
---

# Story 4.1: Deploy do Banco de Dados PostgreSQL no Railway

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a administrador do sistema,
I want provisionar um banco de dados PostgreSQL no Railway e executar as migrações,
So that o aplicativo tenha um banco de dados em produção pronto para receber dados.

## Acceptance Criteria

1. **Given** uma conta no Railway
   **When** provisionarmos o banco
   **Then** devemos ter a URL de conexão (DATABASE_URL)
   **And** devemos rodar o Alembic para criar as tabelas `Transaction` e `Limits`.

## Tasks / Subtasks

- [x] Task 1: Provisionar o serviço PostgreSQL no dashboard do Railway.
- [x] Task 2: Obter a string de conexão (DATABASE_URL).
- [x] Task 3: Configurar a DATABASE_URL temporariamente no ambiente local para rodar as migrações.
- [x] Task 4: Executar `alembic upgrade head` para criar as tabelas `Transaction` e `Limits` no banco de produção.
- [x] Task 5: Validar a criação das tabelas conectando-se ao banco.

## Dev Notes

### Technical Requirements
- **Banco de Dados:** PostgreSQL (via Railway).
- **Migrações:** Alembic.
- **Segurança:** Nunca comite a `DATABASE_URL` de produção no repositório. Mantenha as chaves seguras e use apenas via variáveis de ambiente.

### Architecture Compliance
- O sistema usa `SQLModel` e precisa das tabelas já provisionadas antes da API subir na Story 4.2.
- Railway Database URLs costumam vir no formato `postgresql://...`, o asyncpg pode exigir `postgresql+asyncpg://...`. O Alembic (síncrono) geralmente usa `postgresql://...`. Fique atento aos drivers de conexão.

### Execution Guide
Esta história é majoritariamente operacional (DevOps). O agente desenvolvedor pode precisar usar comandos de shell para testar a conexão com o banco e aplicar as migrações, ou o próprio usuário pode ter que prover a URL do banco que criou manualmente no painel do Railway.

## Dev Agent Record

### Agent Model Used
Gemini 3.1 Pro (High)

### Completion Notes List
- O usuário criou o banco PostgreSQL no Railway e forneceu a `DATABASE_URL`.
- As migrações foram rodadas com sucesso usando `alembic upgrade head`.
- As tabelas `alembic_version`, `Limits`, e `transactions` foram devidamente criadas no banco de produção.
