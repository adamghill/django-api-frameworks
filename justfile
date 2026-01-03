#!/usr/bin/env just

# Load environment variables from .env if it exists
set dotenv-load

# List commands
_default:
  just --list --unsorted --justfile {{ justfile() }} --list-heading $'Available commands:\n'

# Build Docker containers
build  *ARGS='':
  docker-compose build {{ ARGS }}

# Build Docker containers without cache
build-no-cache *ARGS='':
  docker-compose build --no-cache {{ ARGS }}

# Start all Docker containers in detached mode
up *ARGS='':
  just build {{ ARGS }}
  docker-compose up -d {{ ARGS }}

# Start Django container
django:
  docker-compose up -d django

# Start Django DRF container
djangorestframework:
  docker-compose up -d djangorestframework

# Start Django Ninja container
django-ninja:
  docker-compose up -d django-ninja

# Start FastAPI container
fastapi:
  docker-compose up -d fastapi

# Start Django Rapid container
django-rapid:
  docker-compose up -d django-rapid

# Start Django Bolt container
django-bolt:
  docker-compose up -d django-bolt

# Start Django REST Framework 2 container
djrest2:
  docker-compose up -d djrest2

# Start Django Shinobi container
django-shinobi:
  docker-compose up -d django-shinobi

# Stop and remove Docker containers
down:
  docker-compose down

# Clean up Docker resources
clean:
  docker stop $(docker ps -aq) || true
  docker rm $(docker ps -aq) || true
  docker volume rm $(docker volume ls -q) || true
  docker rmi $(docker images -q) || true
  docker network rm $(docker network ls -q) || true
  docker system prune -a --volumes || true

# Run Django migrations
migrate:
  # Only need to run this in one container since they all share the same database
  docker exec -it django uv run python manage.py migrate

# Populate Django database
populate:
  # Only need to run this in one container since they all share the same database
  just migrate
  docker exec -it django uv run python manage.py populate

# Run pytest tests
test *ARGS='':
  docker exec -it django uv run pytest -q
  docker exec -it django-bolt uv run pytest -q
  docker exec -it django-ninja uv run pytest -q
  docker exec -it django-rapid uv run pytest -q
  docker exec -it django-shinobi uv run pytest -q
  docker exec -it djangorestframework uv run pytest -q
  docker exec -it djrest2 uv run pytest -q
  docker exec -it fastapi uv run pytest -q
  just validate {{ ARGS }}

validate *ARGS='':
  cd load-testing && uv run pytest -q {{ ARGS }}

# Run benchmarks
benchmark:
  cd load-testing && uv run pytest --benchmark-only --benchmark-compare --benchmark-columns 'min,max,mean,stddev,median'

wrk:
  cd load-testing && uv run pytest -k test_wrk_endpoints -s

test-all:
  just test
  just benchmark

# Open PostgreSQL shell
psql:
  docker exec -it db psql -U postgres -d django-api-frameworks

shell:
  docker exec -it django uv run python manage.py shell
