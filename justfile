# List available commands
_default:
    @just --list

# Start the Temporal dev server
server:
    temporal server start-dev

# Start the worker
worker:
    uv run python3 worker.py

# Start both the Temporal server and worker together
dev:
    #!/usr/bin/env bash
    set -e
    temporal server start-dev &
    SERVER_PID=$!
    trap "kill $SERVER_PID 2>/dev/null" EXIT
    uv run python3 worker.py

# Run the workflow
run:
    uv run python3 -m starters.hello

# Run the weather workflow
weather:
    uv run python3 -m starters.weather

# Initialize database with migrations
db-init:
    uv run alembic upgrade head

# Create a new database migration
db-migrate MESSAGE="":
    uv run alembic revision --autogenerate -m "{{MESSAGE}}"

# View recent weather records
db-view:
    #!/usr/bin/env bash
    source .env
    psql "$DATABASE_URL" -c "SELECT id, location, weather_status, temperature, humidity, description, timestamp FROM weather ORDER BY timestamp DESC LIMIT 10;"
