#!/bin/sh
set -e

echo "⏳ Running database migrations..."
uv run --no-sync alembic upgrade head
echo "✅ Migrations complete."

exec uv run --no-sync gunicorn main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind "0.0.0.0:${WEB_SERVER_PORT:-8000}" \
  --workers "${GUNICORN_WORKERS:-2}" \
