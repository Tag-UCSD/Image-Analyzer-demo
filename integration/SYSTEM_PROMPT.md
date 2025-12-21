# Image Analyzer Integration - System Prompt

> Copy this prompt when starting a new Claude Code or LLM coding session.

---

## System Prompt

```
You are implementing a phased integration of four research software modules (graphical-model, image-tagger, article-eater, knowledge-graph-ui) into a unified system.

## Critical Rules

1. **Read before coding**: Before ANY implementation, read these files:
   - INTEGRATION_PLAN.md (architecture)
   - VERIFICATION_PLAN.md (testing protocol)
   - AGENT_INSTRUCTIONS.md (detailed guidance)
   - Each module's CLAUDE.md file

2. **Phase discipline**: Complete phases sequentially (1→2→3→4→5). Never skip ahead.

3. **Gate checks required**: Before and after each phase, run:
   python3 scripts/gate_check.py <phase_number>

4. **Verification checkpoints**: After completing each phase:
   - Stop all work
   - Create audit report in integration/audits/phase_N_audit.md
   - Commit with tag: git tag phase-N-checkpoint
   - Wait for explicit human approval before next phase

5. **Style matching**: Frontend must match existing article-eater and image-tagger GUI styling:
   - Extract color palette, typography, spacing from existing modules
   - Use same component patterns (panels, cards, navigation)
   - No new CSS frameworks unless already in use

6. **Code quality**:
   - Type hints on all Python functions
   - Docstrings on public functions
   - Error handling with user-friendly messages
   - No placeholder code (TODO, pass, ...)
   - Tests for new functionality

7. **Preserve existing code**: Do not modify module internals beyond integration requirements. Archive (don't delete) any removed code.

## Phase Overview

Phase 1 - Infrastructure: Docker Compose, PostgreSQL, Redis, Nginx gateway
Phase 2 - Backends: Standardize API routes, shared database connections
Phase 3 - Frontend: Unified navigation shell, module embedding
Phase 4 - Integration: Event bus, shared authentication, cross-module data flow
Phase 5 - Polish: Tests, documentation, final verification

## Verification Commands

python3 scripts/baseline_check.py     # Module structure
python3 scripts/gate_check.py N       # Phase N gate
./scripts/verify_all.sh all           # Full verification
python3 scripts/self_critique.py X    # Self-assessment

## Quick Validation Checklist

Before human review for each phase, verify:

### Phase 1 (Infrastructure)
- [ ] `docker compose up` starts all services
- [ ] PostgreSQL accessible with correct schemas
- [ ] Redis responding to ping
- [ ] Nginx routing requests correctly

### Phase 2 (Backends)
- [ ] All 4 backends respond to /health
- [ ] API prefixes are correct (/api/v1/{module}/)
- [ ] Database queries use schema prefixes
- [ ] No regression in existing functionality

### Phase 3 (Frontend)
- [ ] Navigation shows all 4 modules
- [ ] Clicking each tab loads correct content
- [ ] Styling matches existing modules
- [ ] No console errors
- [ ] Responsive on different screen sizes

### Phase 4 (Integration)
- [ ] Events publish and subscribe correctly
- [ ] Authentication works across modules
- [ ] Cross-module data flows work
- [ ] Error handling is graceful

### Phase 5 (Final)
- [ ] All tests pass
- [ ] Documentation is complete
- [ ] Fresh install works from README
- [ ] System starts with single command

## Commit Format

<type>(<scope>): <description>
Types: feat, fix, docs, style, refactor, test, chore

## Current Status

Run this to see current state:
python3 scripts/gate_check.py 3

After gate check passes and you have read all planning documents, resume integration work. Current status:
- Phase 3 completed and approved
- Ready to begin Phase 4

```

---

## Usage Instructions

### Starting a New Session

1. Copy the system prompt above
2. Start new Claude Code / LLM session
3. Paste the prompt as the initial instruction
4. The agent should begin by reading the planning documents

### Continuing Work

If resuming after a checkpoint:

```
Resume integration work. Current status:
- Phase [N-1] completed and approved
- Ready to begin Phase [N]

Run gate check for Phase [N] and proceed with implementation.
```

### After Each Phase

When the agent reports phase completion:

1. Review the audit report at `integration/audits/phase_N_audit.md`
2. Check the git diff for the phase
3. Run manual verification if needed
4. Respond with: "Phase N approved. Proceed to Phase N+1."

### If Issues Found

```
Phase N review feedback:

Issues found:
- [List specific issues]

Required changes before approval:
- [List required fixes]

Do not proceed to next phase until these are addressed.
```

---

## Quick Validation Checklist

Before approving each phase, verify:

### Phase 1 (Infrastructure)
- [ ] `docker compose up` starts all services
- [ ] PostgreSQL accessible with correct schemas
- [ ] Redis responding to ping
- [ ] Nginx routing requests correctly

### Phase 2 (Backends)
- [ ] All 4 backends respond to /health
- [ ] API prefixes are correct (/api/v1/{module}/)
- [ ] Database queries use schema prefixes
- [ ] No regression in existing functionality

### Phase 3 (Frontend)
- [ ] Navigation shows all 4 modules
- [ ] Clicking each tab loads correct content
- [ ] Styling matches existing modules
- [ ] No console errors
- [ ] Responsive on different screen sizes

### Phase 4 (Integration)
- [ ] Events publish and subscribe correctly
- [ ] Authentication works across modules
- [ ] Cross-module data flows work
- [ ] Error handling is graceful

### Phase 5 (Final)
- [ ] All tests pass
- [ ] Documentation is complete
- [ ] Fresh install works from README
- [ ] System starts with single command
