FROM python:3.14-slim AS base-uv

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM base-uv AS django

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    netcat-openbsd \
    git \
    && rm -rf /var/lib/apt/lists/*

FROM django AS final

COPY ./django-hatchway-example/pyproject.toml /app/
RUN uv lock && uv sync --frozen --no-dev

COPY ./django-hatchway-example/ .

# Make wait_for_db.sh executable
RUN chmod +x wait_for_db.sh
