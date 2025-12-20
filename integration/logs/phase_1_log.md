# Phase 1 Log

## Planned Changes
- Create unified Docker Compose at `integration/docker-compose.unified.yml`.
- Add Nginx gateway config at `integration/nginx/nginx.conf`.
- Add database init SQL in `integration/db-init/` for schemas and tables.
- Add `.env.example` and `integration/README.md` for setup guidance.

## Notes
- Gate check 1 initially failed due to missing integration directories/files, Docker daemon not running, and ports 5432/80 in use.
- Docker Desktop started, local PostgreSQL stopped to free port 5432. Port 80 now appears free.

## Changes Made
- Created `integration/`, `integration/logs/`, `integration/nginx/`, `integration/db-init/` directories.

## Files Created
- `integration/docker-compose.unified.yml`
- `integration/nginx/nginx.conf`
- `integration/db-init/00_create_schemas.sql`
- `integration/db-init/01_graphical_tables.sql`
- `integration/db-init/02_tagger_tables.sql`
- `integration/db-init/03_article_tables.sql`
- `integration/db-init/04_graph_tables.sql`
- `integration/db-init/05_shared_tables.sql`
- `integration/.env.example`
- `integration/README.md`

## Issues
- Phase 1 gate check fails on port 80 availability because binding to port 80 requires elevated permissions on macOS.

## Updates
- Changed Nginx host port mapping to 8080 and updated gate checks/verification docs accordingly.

## Updates (Verification Fixes)
- Updated service Dockerfile references and commands in `integration/docker-compose.unified.yml` to run on ports 8001-8004.
- Added Dockerfile for knowledge-graph backend at `knowledge-graph-ui/GraphExplorer_Static_v3/backend/Dockerfile`.

## Verification Fixes (Post-Checkpoint)
- Added `email-validator` dependency and `KeyManager` wrapper for Article Eater startup.
- Added environment overrides for graphical-model model and upload paths.
- Added graphical-model healthcheck override for port 8001.
- Added knowledge-graph backend Dockerfile.
- Updated Nginx upstream hostnames and routing to strip module prefixes.
