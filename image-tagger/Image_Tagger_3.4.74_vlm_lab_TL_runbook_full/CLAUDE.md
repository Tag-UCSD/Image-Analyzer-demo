# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Image Tagger v3.4.74** - Enterprise-grade image tagging and annotation system for architectural image research. Production-ready micro-frontend architecture for analyzing how different spaces are perceived.

**Version:** 3.4.74 (VLM Lab Technical Lead Runbook)

**Architecture:** Monorepo with 4 React micro-frontends, unified FastAPI backend, PostgreSQL database, and Docker orchestration.

**Purpose:** Research tool for tagging architectural images and analyzing perception through visual and semantic attributes with VLM (Vision-Language Model) integration.

## Commands

### Quick Start

```bash
# Full Docker deployment (recommended)
cd deploy
docker-compose up --build

# Access the GUIs:
# - Research Explorer: http://localhost:8080/explorer
# - Tagger Workbench: http://localhost:8080/workbench
# - Supervisor Monitor: http://localhost:8080/monitor
# - Admin Cockpit: http://localhost:8080/admin
```

### Installation and Setup

```bash
# Automated installation with seeding and smoke tests
./install.sh

# This will:
# 1. Build containers (API, DB, frontend)
# 2. Run seeding scripts (tool configs, attributes)
# 3. Run smoke tests (API and science pipeline)
```

### AutoInstaller (Alternative)

```bash
# Use shared AutoInstaller + AI Copilot kit
bash infra/turnkey_installer_v1.3/installer/install.sh

# AI copilot for installation diagnostics
python ai/installer_copilot.py --logfile logs/install.log --out logs/ai_plan.json --dry-run 1 --provider none
```

### Testing

```bash
# Install test dependencies (if not using Docker)
pip install pytest httpx

# Run all tests
pytest tests/test_v3_api.py -v

# Specific test suites
pytest tests/test_v3_api.py           # API and RBAC
pytest tests/test_guardian.py         # Governance
pytest tests/test_bn_export_smoke.py  # BN export
pytest tests/test_workbench_smoke.py  # Tagger Workbench
pytest tests/test_explorer_smoke.py   # Explorer

# Slow tests (full science pipeline)
pytest -m slow
```

### Governance and Guardian

```bash
# Verify governance compliance (check for drift)
python scripts/guardian.py verify

# Update baseline after intentional changes
python scripts/guardian.py freeze
```

### Science Pipeline

```bash
# Run science pipeline smoke test
pytest tests/test_science_pipeline_smoke.py
```

### Database Operations

```bash
# Seed database with core configuration
python backend/scripts/seed_tool_configs.py
python backend/scripts/seed_attributes.py
```

## Architecture

### Frontend (Monorepo - 4 React Apps)

Located in `frontend/apps/`:

1. **Workbench** (`frontend/apps/workbench/`) - Tagger interface for annotating images
2. **Monitor** (`frontend/apps/monitor/`) - Supervisor monitoring dashboard
3. **Admin** (`frontend/apps/admin/`) - Admin cockpit for system management
4. **Explorer** (`frontend/apps/explorer/`) - Research explorer for browsing and searching images

**Tech Stack:**
- React (micro-frontend architecture)
- Shared components in `frontend/shared/`
- Nginx gateway for routing
- Docker for deployment

### Backend (Unified FastAPI Service)

Located in `backend/`:

**Structure:**
- `backend/main.py` - FastAPI application entry point
- `backend/routers/` - API route handlers
- `backend/scripts/` - Database seeding and utilities
- `backend/database/` - Database models and migrations

**Database:** PostgreSQL

**Key Features:**
- Role-based access control (RBAC)
- Image upload and management
- Science pipeline integration
- VLM (Vision-Language Model) support
- Tag validation and IRR (Inter-Rater Reliability)

### Science Pipeline

Located in `backend/science/` (or similar):

**Purpose:** Deterministic, heuristic-based analysis pipeline for architectural images

**Components:**
- Visual attribute extraction (edge detection, complexity analysis)
- Composite indices and bins
- Science debug layers (Canny edge detection overlays)

**Note:** VLM integration hooks exist but are stubbed by default to keep costs predictable.

### Infrastructure (`deploy/`)

**Docker Compose Setup:**
- API service (FastAPI)
- Database service (PostgreSQL)
- Frontend service (Nginx + static files)

**Configuration:**
- Environment variables
- Volume mounts for persistence
- Reverse proxy structure

## Project Constitution

This project follows strict governance rules (see `PROJECT_CONSTITUTION.md`):

### Key Principles

1. **Versioning:** v3.M.N - each release shippable as ZIP or concatenated TXT
2. **No-deletion rule:** Files from prior releases go to `archive/`, never deleted
3. **Governance:** `v3_governance.yml` + `scripts/guardian.py` enforce drift protection
4. **Code quality:** No syntax errors, no `...` placeholders in active code
5. **Science honesty:** Heuristic methods must be readable, reproducible, modifiable
6. **Documentation:** Student-facing docs must stay aligned with reality

### Guardian System

The Guardian (`scripts/guardian.py`) protects critical code from unintended drift:
- Science modules
- API routers
- Deploy scripts
- Governance config

**Always run `python scripts/guardian.py verify` before proposing changes.**

## Student Usage

### Two Tracks

This system supports two student usage patterns:

**Track A - Full App (persistent, Docker-based):**
- Students access a running instance via URL
- Or run Docker locally if comfortable
- Use Tagger Workbench to tag images
- View results in Monitor/Explorer

**Track B - Colab Science Notebook (ephemeral):**
- Students use `notebooks/VLM_Health_Lab.ipynb` in Google Colab
- Self-contained experiment with synthetic images
- Runs science pipeline + VLM variance audit
- Nothing persists after runtime restart

**See:** `STUDENT_START_HERE.md` and `docs/ops/Student_Quickstart_v3.4.73.md`

## Important Patterns

### Archive Pattern (No Deletion)

When refactoring or replacing code:

```bash
# WRONG - deleting old code
rm backend/old_science.py

# RIGHT - archiving old code
mkdir -p archive/v3_2_38_old_science
mv backend/old_science.py archive/v3_2_38_old_science/
```

### Governance Workflow

Before making changes to protected areas:

```bash
# 1. Check current state
python scripts/guardian.py verify

# 2. Make your changes to protected files
# ...

# 3. Verify again (will show drift)
python scripts/guardian.py verify

# 4. After review, freeze new baseline
python scripts/guardian.py freeze
```

### Science Module Development

All science modules should be:
- **Deterministic** - same input always produces same output
- **Readable** - students can read and understand the code
- **Reproducible** - results can be reproduced
- **Modifiable** - thresholds can be changed to see predictable effects

```python
# GOOD - clear, deterministic, modifiable
def calculate_visual_complexity(image, edge_threshold=100):
    """Calculate visual complexity using Canny edge detection.

    Args:
        image: Input image (numpy array)
        edge_threshold: Threshold for edge detection (default 100)

    Returns:
        float: Complexity score between 0 and 1
    """
    edges = cv2.Canny(image, edge_threshold, edge_threshold * 2)
    edge_density = np.sum(edges > 0) / edges.size
    return min(edge_density * 5, 1.0)  # Scale to 0-1

# BAD - opaque, calls external API, non-deterministic
def calculate_visual_complexity(image):
    return vlm_model.predict(image)  # What does this do? Can't modify.
```

### Empty Dashboard Handling

If dashboards show no data:
1. Run seeding scripts (`seed_tool_configs.py`, `seed_attributes.py`)
2. Process images through science pipeline
3. Collect validation data for IRR/Tag Inspector

UX should explicitly say "No data yet" rather than showing empty tables silently.

## Key Files and Locations

**Entry Points:**
- `STUDENT_START_HERE.md` - Student entry point
- `README_v3.md` - High-level overview and quickstart
- `PROJECT_CONSTITUTION.md` - Governance rules

**Documentation:**
- `docs/science_overview.md` - Science pipeline details
- `docs/devops_quickstart.md` - Setup and operations
- `docs/governance_guide.md` - Governance and Guardian
- `docs/AI_COLLAB_WORKFLOW.md` - Multi-agent AI collaboration rules
- `docs/ops/Technical_Lead_Runbook_v3.4.74.md` - Technical lead guide
- `docs/ops/Student_Quickstart_v3.4.73.md` - Student quickstart
- `docs/SCIENCE_DEBUG_LAYERS.md` - Edge map and overlay debug views
- `docs/PRODUCTION_DEPLOYMENT.md` - Production deployment guide

**Configuration:**
- `v3_governance.yml` - Governance configuration
- `deploy/docker-compose.yml` - Docker orchestration
- `contracts/` - API contracts and schemas

**Scripts:**
- `install.sh` - Automated installation
- `scripts/guardian.py` - Governance enforcement
- `scripts/smoke_api.py` - API smoke tests
- `scripts/smoke_science.py` - Science pipeline smoke tests
- `backend/scripts/seed_tool_configs.py` - Seed tool configurations
- `backend/scripts/seed_attributes.py` - Seed image attributes

**AI Integration:**
- `ai/installer_copilot.py` - AI copilot for installation diagnostics
- `ai/triage_schema.json` - Triage schema for AI
- `ai/copilot_policy.json` - Copilot policy

## Known Limitations

1. **Science modules are heuristic** - Not ML-based, intentionally deterministic for teaching
2. **VLM hooks are stubbed** - To keep costs predictable in classroom settings
3. **Composite indices are simple** - Starting point for BN modeling, not final scientific truth
4. **CI workflow is a template** - May need adaptation for specific infrastructure

## Development Workflow

### Adding New Features

1. **Read the constitution** - `PROJECT_CONSTITUTION.md`
2. **Check governance** - Run `scripts/guardian.py verify`
3. **Make changes** - Follow existing patterns
4. **Update docs** - Keep student-facing docs aligned
5. **Update tests** - Add/update tests for new features
6. **Archive old code** - Move replaced code to `archive/`
7. **Freeze baseline** - Run `scripts/guardian.py freeze` after review

### Release Process

Each release must be shippable as:
1. ZIP of full directory tree
2. Concatenated TXT file with `deconcat.py` header for reconstruction

Use `deconcat.py` to concatenate and `deconcat_v3_3.py` to reconstruct.

### AI Collaboration

Follow `docs/AI_COLLAB_WORKFLOW.md` for multi-agent AI collaboration rules specific to this project.

## Production Deployment

See `docs/PRODUCTION_DEPLOYMENT.md` for:
- Environment variables
- Volume configuration
- HTTPS / reverse proxy setup
- Security checklist

## Version History

Current: **v3.4.74** (VLM Lab Technical Lead Runbook)

See `CHANGELOG_*.md` files for version-specific changes:
- `CHANGELOG_v3.4.74_*.md` - Recent changes
- Archive older changelogs in `archive/`

## Support Resources

**For Students:**
- Start: `STUDENT_START_HERE.md`
- Quick guide: `docs/ops/Student_Quickstart_v3.4.73.md`

**For Technical Leads:**
- Runbook: `docs/ops/Technical_Lead_Runbook_v3.4.74.md`
- DevOps: `docs/devops_quickstart.md`

**For Developers:**
- Constitution: `PROJECT_CONSTITUTION.md`
- Governance: `docs/governance_guide.md`
- AI workflow: `docs/AI_COLLAB_WORKFLOW.md`
