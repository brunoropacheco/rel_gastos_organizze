# API Relatório de Gastos de Cartão de Crédito (Organizze)

Este projeto é uma API em FastAPI projetada para automatizar a análise de transações financeiras dos cartões de crédito (Santander AA e Itaú Azul) associados ao aplicativo Organizze. 
Ele busca faturas e transações via API, armazena em um banco local (SQLite via SQLAlchemy/Alembic) e calcula os gastos totais comparando-os com limites pré-definidos (burn rate) por categoria.

## Estrutura do Projeto

- **`src/app/`**: Diretório principal contendo a aplicação FastAPI (modelos, schemas, serviços, banco de dados e rotas da API).
- **`alembic/` & `alembic.ini`**: Configurações de migração de banco de dados.
- **`requirements.txt`**: Lista de dependências do projeto.
- **`legacy/`**: Diretório contendo os scripts analíticos originais.
- **`tests/`**: Testes da aplicação.

## Dependências Principais

- `fastapi` & `uvicorn` (Servidor Web)
- `sqlalchemy` & `alembic` (ORM e Migrações)
- `pandas` & `numpy` (Processamento de dados)
- `requests` (Integração com Organizze)
- `google-api-python-client` (Integração opcional com Google Sheets)

Para instalar todas as dependências, execute:

```sh
pip install -r requirements.txt
```

## Configuração

Antes de executar o servidor da API, configure o seu arquivo `.env` na raiz do projeto com as seguintes variáveis:

- `TOKEN_ORGANIZZE`: Token gerado nas configurações da sua conta do Organizze (engrenagem -> desenvolvedor/API). Usado para o script buscar faturas/metas.
- `WEBHOOK_API_KEY`: Uma senha/token inventada por você. Esse token será exigido no header `X-API-Key` de todas as requisições que chegarem no seu Webhook (ex: vindas do Apple Shortcuts) para garantir segurança.
- `DATABASE_URL`: URL de conexão com o banco de dados. Para testes rápidos locais, recomendamos usar SQLite: `sqlite:///./local.db`.
- `PASSWORD_GMAIL`: (Opcional) Senha de aplicativo do Gmail para rotinas de disparo de e-mail.

### Configurando o Banco de Dados

Com as variáveis de ambiente configuradas e as dependências instaladas, crie as tabelas do banco de dados executando as migrações:

```sh
alembic upgrade head
```

## Execução

Para iniciar o servidor FastAPI e poder receber requisições (como as de webhooks):

```sh
uvicorn src.app.main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`. Você pode acessar `http://127.0.0.1:8000/docs` para ver e testar a documentação interativa (Swagger UI).

## Regras de Negócio e Sincronização

A API utiliza as seguintes regras de sincronização com o Organizze:

1. **Filtro de Cartões:** Apenas despesas de cartões de crédito monitorados são processadas (ex. Santander AA, Itaú Azul).
2. **Ciclo de Fatura:** Para garantir que transações movidas manualmente entre faturas sejam corretamente alocadas, o sistema busca os lançamentos pelo endpoint de **faturas** (`/invoices`), extraindo as transações agrupadas pela data de vencimento (`invoice_date`), não pela data exata da compra.
3. **Burn Rate:** O sistema agrupa os gastos por categoria convertendo valores para absoluto, em seguida os compara aos limites estabelecidos. Caso a planilha do Google Sheets não esteja disponível/configurada, é usado um dicionário de fallback embutido no código com limites definidos.
4. **Tratamento de Parcelas Futuras:** A API do Organizze não move automaticamente parcelas de compras parceladas caso a fatura vire antes. Isso deve ser feito manualmente no app Organizze; após essa ação, a API sincronizará corretamente com base na leitura da fatura.

## Contato

Para mais informações, entre em contato com brunoropacheco@gmail.com.
