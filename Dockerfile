FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instalar uv, cron e limpar cache do apt
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates cron \
    && curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
RUN uv pip install --system --no-cache .

COPY . .

# Tornar o script de entrypoint executável
RUN chmod +x /app/entrypoint.sh

# Configurar o crontab
# 0 10 = 7:00 BRT
# 0 0 = 21:00 BRT
# 15 13 = 10:15 BRT (Run teste imediato/agendado pelo usuario)
RUN echo "0 10 * * * root cd /app && /usr/local/bin/python -m src.scripts.run_cron >> /var/log/cron.log 2>&1" > /etc/cron.d/organizze-cron \
    && echo "0 0 * * * root cd /app && /usr/local/bin/python -m src.scripts.run_cron >> /var/log/cron.log 2>&1" >> /etc/cron.d/organizze-cron \
    && echo "15 13 * * * root cd /app && /usr/local/bin/python -m src.scripts.run_cron >> /var/log/cron.log 2>&1" >> /etc/cron.d/organizze-cron \
    && echo "" >> /etc/cron.d/organizze-cron \
    && chmod 0644 /etc/cron.d/organizze-cron

# Definir o entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Expose port
EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
