FROM python:3.14-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

WORKDIR /app

FROM base AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,source=./django-rapid-example/pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=./django-rapid-example/uv.lock,target=uv.lock \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

FROM base AS final

RUN apt-get update && apt-get install -y \
    postgresql-client \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY ./django-rapid-example/ .
