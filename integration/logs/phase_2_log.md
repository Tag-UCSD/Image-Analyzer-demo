# Phase 2 Log

## Planned Changes
- Standardize API prefixes to `/api/v1/{module}/` while preserving existing routes.
- Add or align `/health` endpoints with module identifiers.
- Ensure each backend uses shared PostgreSQL connection via environment configuration.
- Add tests for new routes where feasible.

## Notes
- Phase 2 gate check passed before implementation.
 - Updated article-eater database usage to go through app.db connect helper (SQLite/Postgres).
 - Added Postgres context-manager support for app.db PostgresConnection.
 - Added knowledge-graph prefix middleware, health endpoint, and optional Postgres-backed graph loading.
 - Added SCHEMA_NAME environment for article-eater and knowledge-graph in unified compose.
 - Updated Nginx routing to forward standardized `/api/v1/{module}` prefixes.
- Added backend tests for new prefix health routes (graphical-model, image-tagger, article-eater, knowledge-graph).
- Image-tagger guardian verification failed due to pre-existing protected file drift (backend/api/v1_discovery.py, backend/api/v1_debug.py, frontend/shared/src/api-client.js, frontend/apps/explorer/src/App.jsx) and new root files (.DS_Store, CLAUDE.md).
