FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

RUN chmod +x entrypoint.sh

ARG WEB_SERVER_PORT=8080
EXPOSE ${WEB_SERVER_PORT}

CMD ["./entrypoint.sh"]
