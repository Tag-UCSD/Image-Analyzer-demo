# Data Flow Integration Verification Plan

## Overview

This verification plan governs the data-flow integration push described in `DATA_FLOW_INTEGRATION_PLAN.md`. It enforces phase gates, incremental testing, and honest self-critique.

---

## Verification Philosophy

- **Test before change**: Establish baseline behavior.
- **Small increments**: Make one change, verify, then proceed.
- **Fail fast**: Do not accumulate failing checks.
- **Reversibility**: Each change should be revertible.

---

## Phase 0: Baseline

### Objective
Confirm all modules are reachable and isolated behavior is known.

### Checks
- `python3 scripts/baseline_check.py`
- Record baseline health endpoints:
 - `http://localhost:8001/api/v1/health`
 - `http://localhost:8002/health`
 - `http://localhost:8003/health`
 - `http://localhost:8004/health`

### Gate Criteria
- All modules reachable.
- Baseline documented.

---

## Phase 1: Database Migrations & Backend Alignment

### Objective
All modules use shared PostgreSQL schemas and configuration.

### Checks
- `python3 scripts/gate_check.py 1`
- Verify schema existence in Postgres: `core`, `tagger`, `evidence`, `graphical`, `graph`.
- Sample query per module schema.

### Gate Criteria
- All modules connect to shared database.
- No schema resolution errors.

### Self-Critique
- Did I test writes, not just reads?
- Are migrations reversible?

---

## Phase 2: Article-Eater → Knowledge-Graph Pipeline

### Objective
Evidence export/import and edge updates wired with events.

### Checks
- New article-eater export endpoint returns valid payload.
- Knowledge-graph update endpoint updates or creates edges.
- Redis event emitted and consumed.

### Gate Criteria
- Evidence items are visible in knowledge-graph output.
- Event bus messages delivered.

### Self-Critique
- What happens if evidence is malformed?
- Are duplicate findings handled safely?

---

## Phase 3: Image-Tagger → Graphical-Model Pipeline

### Objective
Tagged attributes export for Bayesian training and ingestion.

### Checks
- Tagger export endpoint returns valid training data.
- Graphical-model import endpoint persists training data.
- Optional retraining trigger works.

### Gate Criteria
- Training dataset import succeeds and is queryable.

### Self-Critique
- Are attribute schemas aligned between modules?
- Are missing fields handled gracefully?

---

## Phase 4: Knowledge-Graph ↔ Graphical-Model Bidirectional Flow

### Objective
Graph structure export and posterior feedback loop.

### Checks
- Knowledge-graph export endpoint provides DAG structure.
- Graphical-model publishes posteriors to knowledge-graph endpoint.

### Gate Criteria
- Knowledge-graph reflects updated posterior values.

### Self-Critique
- Are we mixing priors and posteriors incorrectly?
- Are edge IDs stable across modules?

---

## Phase 5: Frontend Integration & Testing

### Objective
Frontend surfaces real data and full data flow is verified.

### Checks
- `scripts/run_integration_tests.sh`
- `./scripts/verify_all.sh all`
- Optional manual flow:
 - Submit paper → knowledge-graph update
 - Tag image → model update
 - Graphical-model posterior visible in knowledge-graph

### Gate Criteria
- All automated tests pass.
- Manual flow verified.

### Self-Critique
- Did I verify the data flow end-to-end?
- Are errors surfaced clearly in the UI?

---

## Rollback Strategy

```bash
# Stop services
docker compose -f integration/docker-compose.unified.yml down

# Restore previous state if needed
git checkout -- <changed files>
```

---

## Audit Template

Each phase audit should include:

- Changes made
- Verification results
- Self-critique responses
- Known issues
- Readiness for next phase
