# Data Flow Integration Agent Instructions

> **Purpose:** Direct an LLM coding agent to implement backend data flow integration across Image Analyzer modules using DATA_FLOW_INTEGRATION_PLAN.md as the source of truth.

---

## Mission

You are implementing backend data flow integration across four research modules. Your work must be:

1. **Plan-Driven** - Follow DATA_FLOW_INTEGRATION_PLAN.md phases and steps exactly.
2. **Auditable** - Produce clear logs and audit artifacts at each phase.
3. **Minimal-Invasive** - Modify module internals only as required for integration; archive any removed code.
4. **High-Quality** - Type hints on all Python functions, docstrings for public functions, and user-friendly error handling.

---

## Critical Documents (Read Before Coding)

- `DATA_FLOW_INTEGRATION_PLAN.md` (primary source of tasks and phases)
- `VERIFICATION_PLAN.md` (testing protocol for this push)
- `AGENT_INSTRUCTIONS.md` (this file)
- Each module's `CLAUDE.md`

---

## Phase Execution Protocol

### Before Each Phase

1. Read the phase section in `DATA_FLOW_INTEGRATION_PLAN.md`.
2. Run the gate check:
   ```bash
   python3 scripts/gate_check.py <phase_number>
   ```
3. Create a log at `integration/logs/data_flow_phase_N_log.md`.
4. List planned changes in the log before implementation.

### During Each Phase

1. Make incremental commits (one logical change per commit).
2. Update the phase log with files modified and rationale.
3. Run the required verification for each step before proceeding.
4. Preserve existing behaviors unless explicitly required to change.

### After Each Phase

1. Run required verification and gate check.
2. Complete the phase log with summary and known issues.
3. Create an audit report at `integration/audits/data_flow_phase_N_audit.md`.
4. Tag the checkpoint:
   ```bash
   git add -A
   git commit -m "Phase N data flow complete: <summary>"
   git tag data-flow-phase-N-checkpoint
   ```
5. STOP and wait for explicit human approval before the next phase.

---

## Data Flow Phases (from DATA_FLOW_INTEGRATION_PLAN.md)

Use the plan verbatim. The high-level phases are:

1. **Phase 1: Database Migrations & Backend Alignment**
2. **Phase 2: Article-Eater → Knowledge-Graph Pipeline**
3. **Phase 3: Image-Tagger → Graphical-Model Pipeline**
4. **Phase 4: Knowledge-Graph ↔ Graphical-Model Bidirectional Flow**
5. **Phase 5: Frontend Integration & Testing**

---

## Code Quality Standards

### Python
- Type hints required for all functions.
- Docstrings required for public functions.
- Validate inputs early and return user-friendly error messages.
- Avoid placeholder code (`TODO`, `pass`, `...`).

### HTTP/API
- Keep new endpoints versioned and documented.
- Handle timeouts and failed cross-module calls gracefully.
- Keep payload schemas consistent with the plan.

### Databases
- Use schema-prefixed table names.
- Add migrations with reversible steps where possible.
- Do not drop data; archive or backfill if changes are required.

---

## Constraints and Boundaries

### Do NOT
- Skip phases or gate checks.
- Modify module internals beyond integration needs.
- Remove code without archiving it.
- Introduce new dependencies without justification.
- Proceed without explicit human approval after each phase.

### Always
- Read the module `CLAUDE.md` before editing that module.
- Document decisions and rationale.
- Add tests for new functionality.
- Keep changes as small and reversible as possible.

---

## Quick Commands

```bash
# Gate checks
python3 scripts/gate_check.py N

# Integration tests
scripts/run_integration_tests.sh

# Full verification
./scripts/verify_all.sh all
```

---

## Success Criteria

The integration is complete when:

1. Data flows between modules per the plan (Article-Eater ↔ Knowledge-Graph, Image-Tagger → Graphical-Model, Graphical-Model → Knowledge-Graph).
2. Shared database schemas are used consistently.
3. Event bus messages are published and consumed correctly.
4. New endpoints pass integration tests.
5. Documentation and audit artifacts are complete and approved.
