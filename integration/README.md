# Integration Infrastructure

This directory contains the Phase 1 infrastructure for the unified Image Analyzer system.

## Contents

- `docker-compose.unified.yml` - Unified orchestration for database, cache, gateway, and services
- `nginx/nginx.conf` - Nginx gateway configuration
- `db-init/` - PostgreSQL initialization SQL
- `.env.example` - Environment variable template

## Quick Start

1. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

2. Validate the compose file:
   ```bash
   docker compose -f docker-compose.unified.yml config
   ```

3. Start infrastructure services:
   ```bash
   docker compose -f docker-compose.unified.yml up -d postgres redis
   ```

4. Run the Phase 1 gate check:
   ```bash
   python3 ../scripts/gate_check.py 1
   ```
