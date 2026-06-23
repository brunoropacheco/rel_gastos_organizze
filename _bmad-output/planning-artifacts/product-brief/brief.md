---
title: Relatório de Inteligência de Gastos Organizze
status: draft
created: 2026-06-13
updated: 2026-06-13
---

# Product Brief: Co-Piloto Financeiro Organizze

## 1. Visão Geral e Objetivo
Transformar a gestão financeira passiva (apenas registro) em uma experiência ativa e preditiva. O sistema deve fornecer uma "visão diária da realidade", eliminando pontos cegos através de notificações em tempo real e projeções baseadas em comportamento, utilizando a infraestrutura do Organizze e Google Sheets.

## 2. O Problema (A "Dor")
A dificuldade de manter a consciência situacional dos gastos ao longo do mês. O usuário muitas vezes só percebe que excedeu o orçamento quando o estrago já foi feito, devido à falta de feedback imediato e projeções realistas de gastos recorrentes/invisíveis.

## 3. Público-Alvo
Uso pessoal (Bruno), focado em automação de baixo esforço e alta relevância.

## 4. Funcionalidades Principais (Conceitos do Brainstorming)

### 4.1. Estação Meteorológica Financeira (Previsão)
*   **Burn-Rate Velocity:** Monitoramento da velocidade de gasto em relação ao tempo restante do mês/fatura.
*   **Projetor de Consequências:** Mostrar o impacto de um gasto hoje no aporte final planejado para o mês.
*   **Indicador de Pressão:** Alerta quando múltiplas categorias sobem simultaneamente acima da média histórica.

### 4.2. Notificações e Interação (O Mensageiro)
*   **WhatsApp via CallMeBot:** Notificações matinais com o "teto do dia" e alertas de desvio.
*   **Shadow Hook (Atalhos iOS):** [ASSUNÇÃO] Uso de webhooks disparados por automações de celular para captura instantânea de gastos.
*   **Gráfico Burn-down Textual:** Visualização simplificada no WhatsApp `[Ideal: ===] [Real: ===]`.

### 4.3. Inteligência e Persistência
*   **Arquétipo de Rotina:** Criação de um "budget fantasma" para gastos de rotina (café, transporte) que ocorrem em dias específicos.
*   **Persistência Segura:** Armazenamento local/em nuvem (Google Sheets) para permitir comparativos históricos mesmo com instabilidades na API do Organizze.

## 5. Requisitos Técnicos e Infraestrutura
*   **Plataforma:** Script Python rodando 24/7 em servidor [ASSUNÇÃO] (ex: Raspberry Pi, VPS, Railway).
*   **Integrações:** API Organizze (v2), API Google Sheets (v4), CallMeBot API.
*   **Segurança:** Credenciais via variáveis de ambiente (`os.environ`).

## 6. Critérios de Sucesso
*   Recebimento de resumo diário antes das 9h da manhã.
*   Zero "pontos cegos" (nenhum gasto grande sem que o impacto no aporte seja notificado).
*   Latência de captura de gastos via Shadow Hook inferior a 5 segundos [ASSUNÇÃO].

---

## 7. O que está fora do escopo (Non-Goals)
*   Interface gráfica complexa (o foco é texto/WhatsApp).
*   Substituição total do app Organizze (o sistema é um complemento de inteligência).
