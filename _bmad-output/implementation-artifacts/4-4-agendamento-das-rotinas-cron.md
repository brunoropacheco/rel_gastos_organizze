---
baseline_commit: "latest"
---

# Story 4.4: Agendamento das Rotinas (CRON)

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a sistema,
I want ter as rotinas de sincronização do Organizze e envio do Telegram agendadas para rodar automaticamente,
So that eu receba meu relatório 2 vezes ao dia (7h da manhã e 21h) sem intervenção manual.

## Acceptance Criteria

1. **Given** os serviços de sincronização e relatório desenvolvidos (Sync e Intel)
   **When** os horários agendados chegarem (07:00 e 21:00)
   **Then** o agendador (ex: Railway CronJobs ou script agendador interno) deve acionar a rotina
   **And** deve sincronizar os dados pendentes do Organizze
   **And** processar a inteligência e disparar a mensagem via CallMeBot via Telegram.

## Tasks / Subtasks

- [ ] Task 1: Avaliar a melhor estratégia para o agendamento no contexto da nossa arquitetura (ex: usar Cron nativo do Railway para chamar uma rota POST oculta na API, ou criar um script Python avulso acionado via comando do Docker, ou usar biblioteca interna como APScheduler/Celery). Como estamos num único contêiner no Railway rodando Uvicorn, o ideal pode ser expor um endpoint restrito ou usar o recurso de Cron Job do Railway se disponível (ou agendador em background no FastAPI).
- [ ] Task 2: Configurar o agendamento Cron para a sincronização e os envios programados. Os horários definidos pelo usuário são 07:00 e 21:00 (fuso horário local - importante checar o timezone do servidor do Railway).
- [ ] Task 3: Criar um mecanismo na rotina para orquestrar a execução sequencial: 1º Rodar o Sync (para baixar novos dados do Organizze), 2º Rodar o Intel/Notify (para gerar o gráfico com os dados mais recentes).
- [ ] Task 4: Realizar um teste manual do script/endpoint de agendamento para validar que a cadeia de execução roda do início ao fim sem bloquear a thread principal da API.

## Dev Notes

### Technical Requirements
- **Horários Alvo:** 07:00 AM e 21:00 (9 PM). Lembre-se de tratar adequadamente a conversão de Timezone (UTC vs BRT). 7h BRT = 10h UTC. 21h BRT = 00h UTC.
- **Orquestração:** O envio do telegram depende do Sync ter rodado antes. É fundamental garantir a ordem.
- **Implementação Sugerida:** Como o Railway suporta Cron Jobs de forma flexível executando um comando via CLI, uma opção limpa é criar um arquivo `src/scripts/run_cron.py` que importa os `services` e os roda via `asyncio`, sendo configurado no painel do Railway como um Cron Job que roda nos horários desejados.

### Architecture Compliance
- O `SyncService` e o `IntelService/NotifyService` foram desenhados como funções de serviço. Podem ser injetadas facilmente num script Python ou numa rota FastAPI.

### Developer Context & Guidelines
- Essa história requer desenvolvimento de código no backend.
- Lembre-se de proteger a lógica para não falhar silenciosamente. Adicione logs descrevendo `Iniciando rotina CRON de 7h/21h...`

## Previous Story Intelligence
- Na História 4.2 a API foi provisionada com sucesso e as variáveis de ambiente necessárias (DATABASE_URL, TOKEN_ORGANIZZE, CALLMEBOT_USER) já estão no Railway.
- O código atual já possui todas as lógicas essenciais em `sync_service.py` e `notify_service.py`.

## Dev Agent Record

### Agent Model Used
(To be filled during dev-story)

### Completion Notes List
- (To be filled during dev-story)
