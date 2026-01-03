FROM python:3.14-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

WORKDIR /app

FROM base AS builder

# Install system dependencies needed for building
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies into a virtualenv
# Using a cache mount for uv speed up subsequent builds
RUN --mount=type=bind,source=./django-example/pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=./django-example/uv.lock,target=uv.lock \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

FROM base AS final

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-openbsd \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtualenv from the builder
COPY --from=builder /app/.venv /app/.venv

# Add the venv to the path
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY ./django-example/ /app/

# Make wait_for_db.sh executable
RUN chmod +x wait_for_db.sh
