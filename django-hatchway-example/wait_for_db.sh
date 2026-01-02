#!/bin/bash
set -e

# Wait for PostgreSQL to be available
echo "Waiting for PostgreSQL..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL is up - executing command"

# Execute the command passed to this script
exec "$@"
