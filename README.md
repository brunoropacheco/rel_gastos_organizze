# Relatório de Gastos de Cartão de Crédito (Organizze)

API em **FastAPI** que automatiza o acompanhamento dos gastos de cartão de crédito (Santander AA e Itaú Azul) do app [Organizze](https://organizze.com.br).

Ela:

1. Recebe transações em tempo real via **webhook** (ex.: Apple Wallet / Atalhos da Apple).
2. Sincroniza faturas e transações do Organizze via API e **deduplica** com as do webhook.
3. Calcula o **burn rate** (gasto vs. limite por categoria e meta diária).
4. Envia um resumo por mensagem (via [CallMeBot](https://www.callmebot.com/)) em horários agendados (cron).

## Arquitetura

```mermaid
flowchart LR
    A[Apple Wallet / Atalhos] -->|POST + X-API-Key| B[FastAPI]
    C[Cron no container] --> D[run_cron.py]
    D -->|API| E[Organizze]
    D --> F[(PostgreSQL)]
    B --> F
    D -->|resumo| G[CallMeBot]
```

## Estrutura do Projeto

| Caminho | Descrição |
|---|---|
| `src/app/main.py` | Aplicação FastAPI (`/health` e rotas de webhook) |
| `src/app/api/` | Rotas (`POST /api/webhooks/transactions`) |
| `src/app/core/` | Configuração (`config.py`), segurança e utilitários (hash de deduplicação) |
| `src/app/db/`, `models/`, `schemas/` | Sessão do banco, modelos SQLModel e schemas Pydantic |
| `src/app/services/` | Sync com Organizze, reconciliação, cálculo de burn rate e notificações |
| `src/scripts/run_cron.py` | Rotina agendada: migrações → sync → burn rate → notificação |
| `alembic/`, `alembic.ini` | Migrações do banco |
| `Dockerfile`, `entrypoint.sh` | Imagem usada no deploy (API + cron no mesmo container) |
| `migration/`, `legacy/` | SQL de classificação e scripts analíticos originais |
| `tests/` | Testes (pytest) |

## Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `DATABASE_URL` | Sim | URL do PostgreSQL. Prefixo `postgres://` é convertido automaticamente para `postgresql://`. |
| `TOKEN_ORGANIZZE` | Sim | Token da API do Organizze (Configurações → Desenvolvedor/API). |
| `WEBHOOK_API_KEY` | Sim | Chave inventada por você; exigida no header `X-API-Key` das chamadas ao webhook. |
| `CALLMEBOT_USER` | Sim | Usuário/alias do CallMeBot usado para enviar a notificação. |
| `PORT` | Não | Porta HTTP (o Railway define sozinho; padrão `8000`). |

## Deploy no Railway (PostgreSQL incluso)

Este é o setup usado em produção (branch `dev`). O Railway constrói a imagem a partir do `Dockerfile` automaticamente.

1. No [Railway](https://railway.app), crie um **New Project → Deploy from GitHub repo** e selecione este repositório e a branch desejada (**Settings → Source → Branch**).
2. No mesmo projeto, clique em **+ New → Database → Add PostgreSQL**.
3. No serviço da API, abra **Variables** e configure:
   - `DATABASE_URL` = `${{Postgres.DATABASE_URL}}` (referência ao serviço do banco; ajuste `Postgres` se o serviço tiver outro nome)
   - `TOKEN_ORGANIZZE`, `WEBHOOK_API_KEY`, `CALLMEBOT_USER`
4. Em **Settings → Networking**, clique em **Generate Domain** para expor a API publicamente.
5. Faça o deploy. No start, o container executa:

   ```sh
   alembic upgrade head && uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```

   Ou seja, **as migrações rodam automaticamente** a cada deploy.
6. Valide: `curl https://<seu-dominio>.up.railway.app/health` → `{"status":"ok"}`.

**Cron:** o `Dockerfile` instala o `cron` e agenda `python -m src.scripts.run_cron` (horários em UTC: `10:00` = 07:00 BRT, `00:00` = 21:00 BRT, e `13:22` = 10:22 BRT). O `entrypoint.sh` copia as variáveis de ambiente para `/etc/environment` para que o cron as enxergue, e os logs aparecem nos logs do serviço no Railway.

> Dica: se o serviço do app e o Postgres estão no mesmo projeto, prefira a URL interna (`DATABASE_PRIVATE_URL`/`postgres.railway.internal`) para evitar tráfego público e custos de egress. Para rodar localmente contra o banco do Railway, use a URL pública (`DATABASE_PUBLIC_URL`).

## Rodando Localmente

Requisitos: Python ≥ 3.12 e um PostgreSQL acessível.

### 1. Clonar e instalar

```sh
git clone <url-do-repositorio>
cd rel_gastos_organizze
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"        # ou: uv pip install -e ".[dev]"
```

### 2. Subir um PostgreSQL

Opção A — Docker:

```sh
docker run -d --name organizze-pg \
  -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=organizze \
  -p 5432:5432 postgres:16
```

Opção B — usar o banco do Railway (copie a `DATABASE_PUBLIC_URL`). Cuidado: você estará apontando para dados reais.

> O projeto usa Postgres (inclusive o job de cron usa `asyncpg`). SQLite não é suportado de forma confiável.

### 3. Criar o `.env` na raiz

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/organizze
TOKEN_ORGANIZZE=seu_token_do_organizze
WEBHOOK_API_KEY=uma_chave_secreta_qualquer
CALLMEBOT_USER=seu_usuario_callmebot
```

### 4. Migrar e iniciar

```sh
alembic upgrade head
uvicorn src.app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### 5. Executar a rotina de sync/notificação manualmente

```sh
python -m src.scripts.run_cron
```

### 6. Testes

```sh
pytest
```

## Usando o Webhook

```sh
curl -X POST http://127.0.0.1:8000/api/webhooks/transactions \
  -H "X-API-Key: $WEBHOOK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"description": "Padaria", "amount_cents": 1590, "date": "2026-01-15T12:30:00"}'
```

- `amount_cents`: valor em centavos (positivo; `1590` = R$ 15,90).
- Retorna `201` com a transação. Chamadas repetidas com os mesmos dados não duplicam o registro.

## Regras de Negócio e Sincronização

1. **Filtro de cartões:** apenas despesas de cartões monitorados são processadas (Santander AA, Itaú Azul).
2. **Ciclo de fatura:** o sistema busca lançamentos pelo endpoint de faturas (`/invoices`), agrupando pela data de vencimento (`invoice_date`) e não pela data da compra, para respeitar transações movidas manualmente entre faturas.
3. **Burn rate:** os gastos são agrupados por categoria (em valor absoluto) e comparados aos limites cadastrados no banco, gerando também a meta diária restante no mês.
4. **Deduplicação (Webhook × Organizze):** transações do Apple Wallet chegam via webhook com valor positivo e sem `invoice_date`. A assinatura de hash usa `abs()` do valor, permitindo casar com as despesas negativas do Organizze. Ao conciliar, a transação herda `invoice_date`, `category_name` etc. da API, entrando no cálculo do burn rate sem perder a descrição original.

## Contato

Dúvidas: brunoropacheco@gmail.com
**Nota:** Este README foi ajustado para refletir o funcionamento do código atual. Atualize conforme necessário para atender suas necessidades específicas.
dando um commit para voltar o actions
