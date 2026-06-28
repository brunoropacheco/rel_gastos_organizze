FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instalar uv e limpar cache do apt
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
RUN uv pip install --system --no-cache .

COPY . .

# Expose port
EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
