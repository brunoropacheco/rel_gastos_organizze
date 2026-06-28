---
baseline_commit: "latest"
---

# Story 4.2: Deploy da API FastAPI no Railway via Docker

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a administrador do sistema,
I want fazer o deploy do código da aplicação no Railway usando o Dockerfile,
So that a API fique publicamente acessível via HTTPS de forma contínua.

## Acceptance Criteria

1. **Given** o código atualizado no repositório
   **When** o Railway fizer o build e deploy
   **Then** a API deve estar online e respondendo na rota root e `/docs`
   **And** as variáveis de ambiente devem estar devidamente configuradas no painel do Railway.

## Tasks / Subtasks

- [x] Task 1: Revisar o `Dockerfile` para garantir compatibilidade com o ambiente de produção do Railway (uso do `PORT` do Railway, vinculação a `0.0.0.0`).
- [x] Task 2: Conectar o repositório GitHub ao projeto Railway existente (onde o banco já foi criado na História 4.1).
- [x] Task 3: Configurar todas as variáveis de ambiente sensíveis no painel do Railway (ex: `DATABASE_URL`, `TOKEN_ORGANIZZE`, chaves da API, etc).
- [x] Task 4: Aguardar o build e monitorar os logs do Railway para garantir inicialização bem-sucedida.
- [x] Task 5: Acessar a URL pública gerada pelo Railway (`https://<railway-app-url>/docs`) e confirmar que a documentação está acessível e a API responde corretamente.

## Dev Notes

### Technical Requirements
- **Hospedagem:** Railway.
- **Port Binding:** O Railway fornece a porta através da variável de ambiente `PORT`. A aplicação FastAPI precisa iniciar no `0.0.0.0` utilizando a porta fornecida.
- **Dockerfile:** A aplicação deve utilizar o Dockerfile otimizado já existente no repositório, ou ajustá-lo caso o Uvicorn não consiga utilizar a variável `$PORT`.

### Architecture Compliance
- O Railway suporta nativamente builds via `Dockerfile`.
- O banco de dados PostgreSQL foi criado na história `4.1` (epic-4). A comunicação entre os serviços no Railway preferencialmente deve usar variáveis de rede privadas, mas a URL do banco (DATABASE_URL) já está definida e validada.

### Developer Context & Guidelines
- Essa história requer acesso ao painel do Railway (DevOps/Operacional). 
- O agente desenvolvedor não conseguirá criar configurações na interface do Railway de forma autônoma.
- O Agente precisará auditar o `Dockerfile` e validar localmente se ele atende os requisitos do Railway.
- O Agente deve instruir e orientar o usuário sobre como injetar as variáveis de ambiente necessárias (como CallMeBot, Token do Organizze, e chaves de segurança) via painel do Railway.

## Previous Story Intelligence
- Na História `4.1`, o PostgreSQL foi implantado com sucesso no Railway e a string de conexão (`DATABASE_URL`) já está funcional. As tabelas (`transactions` e `Limits`) já estão disponíveis no banco em produção.
- O código atual inclui todos os `services` necessários (Sync, Intel, Notify) integrados e prontos (commit `e494dc8`).

## Git Intelligence
- O último commit integrou grande quantidade de código (Epics 2, 3). É fundamental assegurar que o arquivo `requirements.txt` ou o arquivo do gerenciador de dependências (`uv`/`pyproject.toml`) está totalmente atualizado para não falhar no Build do Railway.

## Project Context Reference
- **Documentação de Projeto**: Seguir o padrão de docstrings em Português e não comitar credenciais estáticas. Credenciais (`TOKEN_ORGANIZZE`, senhas) DEVEM ser passadas via ambiente e configuradas no painel do Railway (FR-05).

## Dev Agent Record

### Agent Model Used
Gemini 3.1 Pro (High)

### Completion Notes List
- O Dockerfile precisou de um ajuste para o `hatchling` (`uv`) encontrar o `README.md`.
- `pyproject.toml` ajustado para declarar explicitamente o `packages = ["src/app"]`.
- Deploy concluído com sucesso e API validada online, OpenAPI JSON carregado sem erros.
