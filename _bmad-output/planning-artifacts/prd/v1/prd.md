---
title: PRD - Co-Piloto Financeiro Organizze
status: draft
created: 2026-06-13
updated: 2026-06-13
version: v1.0
---

# PRD: Co-Piloto Financeiro Organizze

## 1. Visão Geral
Este documento detalha os requisitos para o sistema de inteligência financeira pessoal que integra a API do Organizze com captura em tempo real via iOS e persistência em PostgreSQL. O objetivo é fornecer consciência situacional diária e preditiva sobre a saúde financeira.

## 2. Objetivos e Sucesso
*   **Consciência em Tempo Real:** Capturar gastos no momento em que ocorrem via Apple Wallet.
*   **Inteligência Preditiva:** Projetar o fechamento do mês baseado na "velocidade" (burn-rate) atual.
*   **Interatividade de Baixo Custo:** Utilizar Telegram (CallMeBot) para interface primária.
*   **Métrica de Sucesso:** 100% dos gastos da Apple Wallet capturados e processados; Recebimento do relatório matinal até às 09:00.
*   **Conciliação:** Os gastos da Apple Wallet vão aparecer na api do organizze depois. Precisa ser feita esta conciliação.

## 3. Experiência do Usuário (User Journeys)

### 3.1. O Gasto Instantâneo (Shadow Hook)
*   **Protagonista:** Bruno realiza uma compra usando Apple Pay/Carteira.
*   **Fluxo:** O iOS detecta a notificação -> Atalho do iOS extrai [Valor, Estabelecimento] -> Envia via HTTP POST para o servidor Python -> Python registra no Postgres e envia um "OK/Impacto" via Telegram.

### 3.2. O Relatório Matinal (The Navigator)
*   **Fluxo:** Às 08:30, o servidor processa os gastos do mês -> Compara com os limites no Postgres -> Calcula a projeção de final de mês -> Envia um resumo no Telegram: "Bom dia! Você tem R$ X para gastar hoje para manter sua meta de aporte."

## 4. Requisitos Funcionais (FRs)

### 4.1. Integração e Captura
*   **FR-01:** O sistema deve expor um endpoint Webhook para receber dados de gastos do iOS.
*   **FR-02:** O sistema deve sincronizar periodicamente com a API Organizze (v2) para validar gastos manuais ou futuras parcelas.
*   **FR-03:** O sistema deve ler notificações da Apple Wallet via automação de "Atalhos" do iOS.
*   **FR-04:** **Conciliação Automática:** O sistema deve identificar e "mesclar" gastos capturados via Webhook com os que aparecerem posteriormente na API do Organizze (evitando duplicidade), usando valor, data e similaridade de descrição.

### 4.2. Inteligência de Gastos
*   **FR-05:** Calcular o **Burn-Rate Velocity** (Média de gastos diários vs. Dias restantes).
*   **FR-06:** Projetar o saldo final de mês considerando gastos fixos já lançados no Organizze.
*   **FR-07:** Gerar o **Gráfico Burn-down Textual** para envio via Telegram.

### 4.3. Persistência e Configuração
*   **FR-08:** Armazenar todas as transações em um banco de dados **PostgreSQL**.
*   **FR-09:** O sistema deve ler os limites de categoria diretamente de uma tabela de configuração no PostgreSQL.

## 5. Requisitos Não-Funcionais (NFRs)
*   **NFR-01 (Disponibilidade):** O servidor Python deve estar disponível 24/7 (rodando em Docker/Railway [ASSUNÇÃO]).
*   **NFR-02 (Criptografia em Trânsito):** Toda comunicação (Webhook, APIs) deve obrigatoriamente utilizar HTTPS/TLS 1.2+ para proteger os dados contra interceptação.
*   **NFR-03 (Autenticação do Webhook):** O endpoint de recepção de gastos deve exigir um Token de Autenticação (API Key) no Header, configurado via Atalhos do iOS.
*   **NFR-04 (Conexões Seguras):** O banco de dados PostgreSQL deve utilizar conexões SSL obrigatórias para proteger os dados em trânsito.
*   **NFR-05 (Proteção de Segredos):** Uso estrito de variáveis de ambiente para tokens (Organizze, Postgres, CallMeBot). Credenciais NUNCA devem aparecer em logs da aplicação.
*   **NFR-06 (Privacidade):** O sistema deve anonimizar ou omitir valores sensíveis em logs de depuração (debug logs).
*   **NFR-07 (Backup e Recuperação):** O banco de dados deve possuir rotina de backup automático para evitar perda de dados históricos.

## 6. Riscos e Dependências
*   **API Organizze:** Limites de rate-limit ou instabilidade.
*   **iOS Shortcuts:** Mudanças no sistema operacional que possam quebrar a leitura de notificações da Carteira.
*   **CallMeBot:** Dependência de serviço de terceiro gratuito para o Telegram.

## 7. Próximos Passos (Fases)
*   **Fase 1:** Setup do Postgres e sincronização básica com Organizze.
*   **Fase 2:** Implementação do Webhook e Integração Apple Wallet.
*   **Fase 3:** Lógica de inteligência (Burn-rate) e Notificações Telegram.

## 8. Regras de Negócio e Extração de Dados (Descobertas em Implementação)
*   **Filtro Exclusivo de Cartões:** O sistema deve sincronizar SOMENTE lançamentos vindos das faturas dos cartões de crédito monitorados (ex: Itaú Azul e Santander AA). Operações de débito e conta corrente devem ser ignoradas no cálculo do Burn-Rate.
*   **Estratégia Orientada a Faturas (Invoices):** As parcelas de cartão e transações movidas manualmente dentro do Organizze preservam sua "data de compra" original. Para garantir o enquadramento perfeito, o sistema DEVE extrair as despesas diretamente das **Faturas de Cartão de Crédito**, usando a `invoice_date` (data de vencimento da fatura) como base para os cálculos, não a data de compra.
*   **Ciclo do Dia 10:** O ciclo financeiro fecha e inicia no dia 10. Consultas de orçamento se baseiam no mês de faturamento que esse dia 10 representa.
*   **Valores Absolutos:** A API retorna despesas como valores negativos, mas toda a inteligência e projeção lida com valores absolutos.
*   **Filtros de Exclusão:** Transações com `ignorar` no campo *notes* e descrições automáticas de débito de fatura (`deb._autom._de_fatura`) devem ser removidas da soma de orçamentos.
*   **Limites de Categoria:** Existe um fallback interno (lista de limites em BRL para categorias como Alimentação, Casa, Viagem, etc.) caso o sistema principal de limites falhe ou não esteja disponível.
