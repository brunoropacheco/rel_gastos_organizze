---
baseline_commit: "latest"
---

# Story 4.3: Configuração do Atalho no iOS (Apple Wallet)

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a usuário final,
I want configurar um Atalho (Shortcut) no iOS para capturar as notificações da Apple Wallet,
So that o atalho envie os dados automaticamente para a API em produção (Webhook).

## Acceptance Criteria

1. **Given** o endpoint em produção e o API Key
   **When** o celular receber uma notificação de compra da Apple Wallet
   **Then** o atalho deve extrair o valor, loja e data
   **And** fazer um POST HTTP autenticado para a API do Railway.

## Tasks / Subtasks

- [ ] Task 1: Obter a URL pública do Railway para a rota de webhook (ex: `https://<dominio>.railway.app/api/webhooks/transactions`).
- [ ] Task 2: Criar uma Automação Pessoal no app "Atalhos" do iOS acionada por notificações de "Transação" ou mensagem do "Apple Wallet".
- [ ] Task 3: Configurar blocos de extração no Atalho (Regex ou Texto) para extrair Valor (centavos), Descrição (estabelecimento) e Data.
- [ ] Task 4: Adicionar o bloco "Obter Conteúdo do URL" (HTTP POST) passando o header `X-API-Key` (configurado com a mesma chave do Railway) e o Payload JSON.
- [ ] Task 5: Realizar uma compra ou envio de teste via atalho e confirmar se a transação aparece no banco de dados e no log da API.

## Dev Notes

### Technical Requirements
- **Integração:** App "Atalhos" (Shortcuts) nativo do iOS.
- **Endpoint Target:** Rota `/api/webhooks/transactions` (Método: POST).
- **Header Autenticação:** `X-API-Key: <Sua-Chave-Secreta>`.
- **Payload Schema:**
  ```json
  {
    "description": "Texto Extraído",
    "amount_cents": 15000, 
    "date": "2026-06-28T00:00:00Z"
  }
  ```
*(Observação: `amount_cents` precisa ser passado como um número inteiro)*

### Architecture Compliance
- Este épico exige que a API já esteja pública (Story 4.2 concluída).
- O webhook processa a criação e passa pela lógica de deduplicação antes de gravar no banco de dados.

### Developer Context & Guidelines
- Essa história é completamente "No-Code" do ponto de vista do repositório de backend, porém vital para o sucesso do projeto. 
- O "Dev Agent" atuará primariamente como um consultor e guia para ajudar o usuário a montar os blocos corretos no app Atalhos do iPhone.
- Pode ser muito útil fornecer ao usuário instruções de como converter valores monetários (ex: R$ 15,30) em centavos (1530) usando Matemática dentro do app Atalhos.

## Previous Story Intelligence
- Na História 4.2 a API foi provisionada com sucesso no Railway e a rota do webhook está documentada e funcionando via HTTPS. A chave de API do webhook (`WEBHOOK_API_KEY`) já deve estar injetada nas variáveis de ambiente.

## Dev Agent Record

### Agent Model Used
(To be filled during dev-story)

### Completion Notes List
- (To be filled during dev-story)
