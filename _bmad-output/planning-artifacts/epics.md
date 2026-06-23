---
stepsCompleted: [1, 2, 3]
inputDocuments: 
  - _bmad-output/planning-artifacts/prd/v1/prd.md
  - _bmad-output/planning-artifacts/architecture.md
---

# rel_gastos_organizze - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for rel_gastos_organizze, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR-01: O sistema deve expor um endpoint Webhook para receber dados de gastos do iOS.
FR-02: O sistema deve sincronizar periodicamente com a API Organizze (v2) para validar gastos manuais ou futuras parcelas.
FR-03: O sistema deve ler notificações da Apple Wallet via automação de "Atalhos" do iOS.
FR-04: Conciliação Automática: O sistema deve identificar e "mesclar" gastos capturados via Webhook com os que aparecerem posteriormente na API do Organizze (evitando duplicidade), usando valor, data e similaridade de descrição.
FR-05: Calcular o Burn-Rate Velocity (Média de gastos diários vs. Dias restantes).
FR-06: Projetar o saldo final de mês considerando gastos fixos já lançados no Organizze.
FR-07: Gerar o Gráfico Burn-down Textual para envio via WhatsApp.
FR-08: Armazenar todas as transações em um banco de dados PostgreSQL.
FR-09: O sistema deve ler os limites de categoria diretamente de uma tabela de configuração no PostgreSQL.

### NonFunctional Requirements

NFR-01 (Disponibilidade): O servidor Python deve estar disponível 24/7 (rodando em Docker/Railway [ASSUNÇÃO]).
NFR-02 (Criptografia em Trânsito): Toda comunicação (Webhook, APIs) deve obrigatoriamente utilizar HTTPS/TLS 1.2+ para proteger os dados contra interceptação.
NFR-03 (Autenticação do Webhook): O endpoint de recepção de gastos deve exigir um Token de Autenticação (API Key) no Header, configurado via Atalhos do iOS.
NFR-04 (Conexões Seguras): O banco de dados PostgreSQL deve utilizar conexões SSL obrigatórias para proteger os dados em trânsito.
NFR-05 (Proteção de Segredos): Uso estrito de variáveis de ambiente para tokens (Organizze, Postgres, CallMeBot). Credenciais NUNCA devem aparecer em logs da aplicação.
NFR-06 (Privacidade): O sistema deve anonimizar ou omitir valores sensíveis em logs de depuração (debug logs).
NFR-07 (Backup e Recuperação): O banco de dados deve possuir rotina de backup automático para evitar perda de dados históricos.

### Additional Requirements

- Starter Template: Custom SQLModel Starter (FastAPI + SQLModel + Docker, Railway Optimized). This impacts Epic 1 Story 1.
- Database: PostgreSQL (latest stable) with SQLModel v0.0.38+ and Alembic v1.18.4+.
- Model Strategy: Single table `Transaction` consolidating Organizze and Webhook data.
- Deduplication: Hash signature (`valor + data + descrição`).
- Framework: FastAPI v0.136.3+
- Dispatch: Synchronous for WhatsApp (CallMeBot) integrated into flow.
- Project Directory Structure initialized using the defined `rel_gastos_organizze` layout.

### UX Design Requirements

N/A

### FR Coverage Map

FR-01: Epic 1 - Endpoint Webhook (iOS)
FR-02: Epic 2 - Sincronização periódica Organizze
FR-03: Epic 1 - Leitura da Apple Wallet
FR-04: Epic 2 - Conciliação Automática
FR-05: Epic 3 - Burn-Rate Velocity
FR-06: Epic 3 - Projeção de Saldo Mensal
FR-07: Epic 3 - Gráfico via WhatsApp
FR-08: Epic 1 - Armazenamento no Postgres
FR-09: Epic 3 - Leitura de Limites

## Epic List

### Epic 1: Captura Instantânea de Gastos (O Shadow Hook)
O usuário consegue registrar seus gastos instantaneamente pelo Apple Wallet para não perder o controle do dinheiro em tempo real.
**FRs covered:** FR-01, FR-03, FR-08

### Epic 2: Sincronização e Conciliação com o Organizze
O sistema integra de forma inteligente seus gastos instantâneos com a consolidação oficial no Organizze, garantindo que não haja duplicidade de valores nas suas finanças.
**FRs covered:** FR-02, FR-04

### Epic 3: Inteligência Financeira e Relatório Matinal (O Navigator)
O usuário recebe diariamente no WhatsApp uma análise preditiva mostrando quanto ainda pode gastar por dia, garantindo o alcance das metas.
**FRs covered:** FR-05, FR-06, FR-07, FR-09

## Epic 1: Captura Instantânea de Gastos (O Shadow Hook)

O usuário consegue registrar seus gastos instantaneamente pelo Apple Wallet para não perder o controle do dinheiro em tempo real.

### Story 1.1: Configuração da Base e Tabela de Transações

As a desenvolvedor,
I want configurar o projeto FastAPI com a conexão segura ao PostgreSQL usando SQLModel e a entidade `Transaction`,
So that possamos ter o repositório correto para gravar as transações que chegarão do celular.

**Acceptance Criteria:**

**Given** as variáveis de ambiente configuradas no servidor
**When** o aplicativo FastAPI inicia
**Then** ele se conecta ao PostgreSQL exigindo SSL
**And** o log de inicialização não expõe credenciais sensíveis

### Story 1.2: Criação do Webhook Autenticado (API iOS)

As a integração do iOS (Atalhos da Apple Wallet),
I want realizar um POST com os dados da transação para a rota `/api/webhooks/transactions`,
So that o gasto instantâneo seja gravado no banco de dados no momento da compra.

**Acceptance Criteria:**

**Given** um payload com os dados financeiros (valor, data, estabelecimento)
**When** a automação do iOS envia uma requisição POST com header `X-API-Key` correto
**Then** o sistema salva com sucesso na tabela `Transaction`
**And** retorna status HTTP adequado para o iOS saber que deu certo

**Given** uma requisição sem a chave da API correta no Header
**When** o envio é feito
**Then** a API rejeita com status 401 ou 403

## Epic 2: Sincronização e Conciliação com o Organizze

O sistema integra de forma inteligente seus gastos instantâneos com a consolidação oficial no Organizze, garantindo que não haja duplicidade de valores nas suas finanças.

### Story 2.1: Sincronização com a API do Organizze

As a rotina do sistema backend (`sync_service`),
I want consultar periodicamente a API REST do Organizze (v2) resgatando as faturas/transações atuais,
So that possamos ter na base os gastos manuais, parcelados e despesas fixas oficiais da plataforma.

**Acceptance Criteria:**

**Given** o `TOKEN_ORGANIZZE` configurado em variável de ambiente
**When** a rotina de sincronização é disparada
**Then** o sistema faz uma requisição HTTP segura à API v2 do Organizze
**And** converte o payload retornado para uma estrutura compatível pronta para análise.

**Given** falha de rede ou rate-limit na API do Organizze
**When** a rotina tentar rodar
**Then** deve gerar um erro no log de forma graciosa sem travar o servidor (resiliência).

### Story 2.2: Algoritmo de Conciliação e Deduplicação (Anti-Duplicidade)

As a rotina do sistema backend,
I want comparar cada transação vinda do Organizze contra as já existentes no banco de dados, usando uma assinatura hash (`valor` + `data` + `similaridade de descrição`),
So that os gastos que já foram recebidos instantaneamente pelo Apple Wallet não sejam salvos como duplicados.

**Acceptance Criteria:**

**Given** que chegou uma transação pela API do Organizze
**When** existir no banco de dados um gasto via Apple Wallet do mesmo dia, com o exato mesmo valor e descrição similar
**Then** o sistema não deve criar um novo registro, mas sim atualizar o registro existente para marcar que foi conciliado com o Organizze
**And** priorizar manter o nome do estabelecimento do Webhook se for mais limpo.

**Given** uma transação que só existe no Organizze (ex: despesa recorrente)
**When** passar pela lógica de sincronização
**Then** um novo registro deve ser persistido no banco de dados com sucesso.

## Epic 3: Inteligência Financeira e Relatório Matinal (O Navigator)

O usuário recebe diariamente no WhatsApp uma análise preditiva mostrando quanto ainda pode gastar por dia, garantindo o alcance das metas.

### Story 3.1: Leitura de Metas e Limites

As a sistema backend (`intel_service`),
I want ler os limites mensais configurados na tabela do banco de dados (PostgreSQL),
So that eu possa ter a base de comparação (orçamento) para analisar os gastos atuais.

**Acceptance Criteria:**

**Given** o acesso ao banco de dados PostgreSQL
**When** a lógica de inteligência iniciar a avaliação do mês
**Then** deve buscar os valores das metas por categoria configurados na tabela `Limits`
**And** se não encontrar limites configurados, deve utilizar um limite padrão (fallback) de segurança.

### Story 3.2: Algoritmo de Inteligência (Burn-Rate e Projeção)

As a rotina de inteligência financeira,
I want processar todas as transações do ciclo atual para calcular o "Burn-Rate Velocity" e projetar o saldo final,
So that o sistema saiba matematicamente a velocidade dos gastos e se o limite do mês estourará.

**Acceptance Criteria:**

**Given** a soma de transações na base de dados
**When** a rotina realizar o cálculo
**Then** deve determinar o total gasto, subtrair do limite mensal e subtrair os gastos fixos projetados para calcular o que sobra
**And** dividir o restante pelos dias que faltam no mês para determinar a meta de gasto diária.

### Story 3.3: Gráfico Textual e Disparo via WhatsApp

As a serviço de notificação (`notify_service`),
I want gerar uma visualização em texto (Burn-down) e enviar via API do CallMeBot,
So that o usuário receba seu alerta matinal (ou sob demanda) de forma legível no WhatsApp.

**Acceptance Criteria:**

**Given** os cálculos consolidados da inteligência financeira
**When** o envio for acionado
**Then** deve formatar o sumário com emojis/ASCII simulando um gráfico burn-down
**And** disparar uma requisição HTTP via TLS 1.2+ para a API do CallMeBot, autenticando pela variável de ambiente

**Given** uma falha de conexão com o CallMeBot
**When** tentar o disparo
**Then** não deve expor dados sensíveis nos logs do sistema.
