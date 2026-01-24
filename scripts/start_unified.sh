#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/integration/docker-compose.unified.yml"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker is not installed or not on PATH." >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker daemon is not running." >&2
  exit 1
fi

# Free port 8080 if a known conflicting container is running.
if docker ps --format '{{.Names}} {{.Ports}}' | rg -q 'deploy-frontend-1.*0\.0\.0\.0:8080'; then
  echo "Stopping conflicting container deploy-frontend-1 on port 8080..."
  docker stop deploy-frontend-1 >/dev/null
fi

# Start base services.
docker compose -f "$COMPOSE_FILE" up -d

# Ensure nginx is running; recreate if needed.
if ! docker compose -f "$COMPOSE_FILE" ps --status running | rg -q '^integration-nginx'; then
  echo "Recreating nginx container..."
  docker compose -f "$COMPOSE_FILE" rm -f nginx >/dev/null || true
  docker compose -f "$COMPOSE_FILE" up -d nginx
fi

# Final check.
if ! curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/ | rg -q '^200$'; then
  echo "WARNING: Gateway not responding on http://localhost:8080/." >&2
  exit 2
fi

echo "Unified stack is up at http://localhost:8080/"
