FROM python:3.14-slim AS base-uv

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY ./django-bolt-example/pyproject.toml /app/
RUN uv lock && uv sync --frozen --no-dev

# Copy application code
COPY ./django-bolt-example/ .

# Run the application
CMD ["uv", "run", "python", "manage.py", "runbolt", "--host", "0.0.0.0", "--port", "8000"]
