#!/bin/sh

# Salva todas as variáveis de ambiente atuais em /etc/environment
# para que o processo do cron (que roda isolado) possa acessá-las.
env >> /etc/environment

# Inicia o serviço do cron no background
service cron start

# Redireciona os logs do cron para o stdout/stderr do container para melhor visibilidade
touch /var/log/cron.log
tail -f /var/log/cron.log &

# Executa o CMD original do Dockerfile ou o comando que o Railway passar
exec "$@"
