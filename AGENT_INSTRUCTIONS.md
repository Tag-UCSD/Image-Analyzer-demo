# Integration Agent Instructions

> **Purpose:** Direct an LLM coding agent to implement the Image Analyzer integration following established plans with human oversight, consistent styling, and high code quality.

---

## Mission

You are implementing a unified integration of four research software modules into a single cohesive system. Your work must be:

1. **Phased** - Follow the 5-phase plan exactly, completing each phase before moving to the next
2. **Auditable** - Produce clear artifacts that humans can review between phases
3. **Consistent** - Match the existing visual style of the article-eater and image-tagger GUIs
4. **High-Quality** - Write production-ready code that follows best practices

---

## Critical Documents

Before any implementation, read and internalize these documents:

```
INTEGRATION_PLAN.md      - Architecture and implementation details
VERIFICATION_PLAN.md     - Testing and verification procedures
scripts/gate_check.py    - Automated verification gates
```

Each module has a `CLAUDE.md` file describing its structure:
- `graphical-model/CLAUDE.md`
- `image-tagger/.../CLAUDE.md`
- `article-eater/.../CLAUDE.md`
- `knowledge-graph-ui/CLAUDE.md`

---

## Phase Execution Protocol

### Before Each Phase

1. **Read the plan section** for the current phase in `INTEGRATION_PLAN.md`
2. **Run the gate check** to verify prerequisites:
   ```bash
   python3 scripts/gate_check.py <phase_number>
   ```
3. **Create a phase log** at `integration/logs/phase_N_log.md`
4. **List planned changes** in the log before making them

### During Each Phase

1. **Make incremental commits** - One logical change per commit
2. **Document as you go** - Update the phase log with:
   - Files created/modified
   - Decisions made and rationale
   - Issues encountered and resolutions
3. **Test continuously** - Verify each change works before proceeding
4. **Follow the style guide** - See "Code Quality Standards" below

### After Each Phase

1. **Run verification** - Execute all relevant tests
2. **Complete the phase log** - Add summary and any known issues
3. **Create audit checkpoint** - Tag the commit:
   ```bash
   git add -A
   git commit -m "Phase N complete: <description>"
   git tag phase-N-complete
   ```
4. **Generate audit report** - Create `integration/audits/phase_N_audit.md`:
   ```markdown
   # Phase N Audit Report

   ## Changes Made
   - [List all files created/modified]

   ## Verification Results
   - [Gate check output]
   - [Test results]

   ## Known Issues
   - [Any issues for human review]

   ## Ready for Phase N+1: Yes/No
   ```
5. **STOP and await human approval** before proceeding to next phase

---

## Phase-by-Phase Implementation

### Phase 1: Infrastructure Foundation

**Goal:** Set up Docker Compose, shared PostgreSQL, Redis, and Nginx gateway.

**Create these files:**
```
integration/
├── docker-compose.unified.yml
├── nginx/
│   └── nginx.conf
├── db-init/
│   ├── 00_create_schemas.sql
│   ├── 01_graphical_tables.sql
│   ├── 02_tagger_tables.sql
│   ├── 03_article_tables.sql
│   ├── 04_graph_tables.sql
│   └── 05_shared_tables.sql
├── .env.example
└── README.md
```

**Verification:**
```bash
docker compose -f integration/docker-compose.unified.yml config
docker compose -f integration/docker-compose.unified.yml up -d
python3 scripts/gate_check.py 1
```

**Audit Artifact:** Screenshot or log of all containers running, database schemas created.

---

### Phase 2: Backend Standardization

**Goal:** Modify each backend to use shared database and standardized API routes.

**Changes per backend:**
1. Update database connection strings to use shared PostgreSQL
2. Add schema prefix to all table references
3. Standardize API prefix: `/api/v1/{module}/`
4. Add `/health` endpoint returning `{"status": "ok", "module": "..."}`
5. Ensure CORS allows requests from the unified frontend

**Do NOT:**
- Rewrite existing logic
- Change internal APIs between components
- Remove existing functionality

**Verification:**
```bash
curl http://localhost:8001/health  # graphical-model
curl http://localhost:8002/health  # image-tagger
curl http://localhost:8003/health  # article-eater
curl http://localhost:8004/health  # knowledge-graph-ui
python3 scripts/gate_check.py 2
```

**Audit Artifact:** API response examples, database connection verification.

---

### Phase 3: Frontend Unification

**Goal:** Create unified frontend shell with navigation between modules.

**Create:**
```
integration/frontend-shell/
├── package.json
├── vite.config.js
├── index.html
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── components/
│   │   ├── Navigation.jsx
│   │   ├── ModuleFrame.jsx
│   │   └── LoadingSpinner.jsx
│   ├── modules/
│   │   ├── GraphicalModel.jsx
│   │   ├── ImageTagger.jsx
│   │   ├── ArticleEater.jsx
│   │   └── KnowledgeGraph.jsx
│   └── styles/
│       ├── main.css
│       ├── navigation.css
│       └── variables.css
└── public/
```

**Style Requirements:** See "GUI Styling Standards" section below.

**Verification:**
```bash
cd integration/frontend-shell
npm install
npm run build
python3 scripts/gate_check.py 3
```

**Audit Artifact:** Screenshots of navigation, each module view, responsive layout.

---

### Phase 4: Inter-Module Integration

**Goal:** Enable modules to communicate via shared event bus and authentication.

**Create:**
```
integration/shared/
├── auth/
│   ├── __init__.py
│   ├── jwt_handler.py
│   └── middleware.py
├── events/
│   ├── __init__.py
│   ├── publisher.py
│   ├── subscriber.py
│   └── schemas.py
└── api_client/
    ├── __init__.py
    └── unified_client.py
```

**Event Schema:**
```python
{
    "event_type": "image.tagged" | "paper.processed" | "graph.updated" | ...,
    "source_module": "tagger" | "article" | "graphical" | "graph",
    "timestamp": "ISO-8601",
    "payload": { ... },
    "correlation_id": "uuid"
}
```

**Verification:**
```bash
# Test event flow
python3 integration/tests/test_events.py
python3 scripts/gate_check.py 4
```

**Audit Artifact:** Event flow diagram, authentication test results.

---

### Phase 5: Polish and Final Verification

**Goal:** Complete documentation, run full test suite, prepare for handoff.

**Create/Update:**
```
integration/
├── README.md              # Complete setup guide
├── TROUBLESHOOTING.md     # Common issues and fixes
├── tests/
│   ├── test_integration.py
│   ├── test_auth.py
│   ├── test_events.py
│   └── test_api_routes.py
└── docs/
    ├── ARCHITECTURE.md
    ├── API_REFERENCE.md
    └── DEPLOYMENT.md
```

**Final Verification:**
```bash
python3 scripts/gate_check.py 5
./scripts/verify_all.sh all
pytest integration/tests/ -v
```

**Audit Artifact:** Full test report, documentation review checklist.

---

## GUI Styling Standards

### Reference Implementations

Study these existing GUIs for styling patterns:

1. **Article Eater Control Room** (`article-eater/.../scripts/ae_streamlit_control_room.py`)
   - Panel-based layout
   - Clean typography
   - Status indicators
   - Card-based content display

2. **Image Tagger Workbench** (`image-tagger/.../frontend/apps/workbench/`)
   - Toolbar navigation
   - Side panel details
   - Image grid layouts
   - Action buttons

### Design Tokens

Extract and use consistent values:

```css
:root {
  /* Colors - derive from existing modules */
  --color-primary: #...;        /* From article-eater */
  --color-secondary: #...;
  --color-background: #...;
  --color-surface: #...;
  --color-text: #...;
  --color-text-muted: #...;
  --color-border: #...;
  --color-success: #...;
  --color-warning: #...;
  --color-error: #...;

  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-size-base: 14px;
  --font-size-sm: 12px;
  --font-size-lg: 16px;
  --font-size-xl: 20px;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 600;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* Borders */
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  --border-width: 1px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}
```

### Component Patterns

**Navigation Bar:**
```jsx
// Horizontal tabs, clean separation, active state indicator
<nav className="unified-nav">
  <div className="nav-brand">Image Analyzer</div>
  <div className="nav-tabs">
    <button className={activeModule === 'graphical' ? 'active' : ''}>
      Causal Model
    </button>
    <!-- ... -->
  </div>
  <div className="nav-user">
    <!-- User menu -->
  </div>
</nav>
```

**Panel Layout:**
```jsx
// Consistent panel structure across modules
<div className="panel">
  <div className="panel-header">
    <h2 className="panel-title">Title</h2>
    <div className="panel-actions"><!-- buttons --></div>
  </div>
  <div className="panel-content">
    <!-- content -->
  </div>
  <div className="panel-footer">
    <!-- optional footer -->
  </div>
</div>
```

**Cards:**
```jsx
// Used for items in lists, search results, etc.
<div className="card">
  <div className="card-header"><!-- optional --></div>
  <div className="card-body"><!-- main content --></div>
  <div className="card-footer"><!-- actions --></div>
</div>
```

### Styling Rules

1. **Do not introduce new design patterns** - Use existing patterns from article-eater and image-tagger
2. **Match visual weight** - Buttons, spacing, typography should feel consistent
3. **Preserve module identity** - Each module can have subtle color accents but share common chrome
4. **Responsive design** - Must work on 1024px+ widths; graceful degradation below
5. **No heavy frameworks** - Use vanilla CSS or CSS modules; avoid Bootstrap/Tailwind unless already in use
6. **Accessibility** - Proper contrast, focus states, semantic HTML

---

## Code Quality Standards

### General Principles

1. **Readability over cleverness** - Code should be immediately understandable
2. **Explicit over implicit** - Name things clearly, avoid magic values
3. **Small functions** - Each function does one thing well
4. **Fail fast** - Validate inputs early, use descriptive error messages
5. **No dead code** - Remove unused imports, functions, variables

### Python Standards

```python
# File structure
"""
Module docstring explaining purpose.
"""

from __future__ import annotations

import stdlib_modules
import third_party_modules
from local import modules

# Constants at top
DEFAULT_TIMEOUT = 30

# Type hints required
def process_data(input_data: dict[str, Any]) -> ProcessResult:
    """
    Brief description.

    Args:
        input_data: Description of parameter.

    Returns:
        Description of return value.

    Raises:
        ValueError: When input is invalid.
    """
    if not input_data:
        raise ValueError("input_data cannot be empty")

    # Implementation
    return result
```

### JavaScript/React Standards

```jsx
// File structure
import React, { useState, useEffect } from 'react';

// Named exports preferred
export function ComponentName({ prop1, prop2 }) {
  // Hooks at top
  const [state, setState] = useState(null);

  // Effects after state
  useEffect(() => {
    // effect logic
  }, [dependency]);

  // Handlers
  const handleClick = () => {
    // handler logic
  };

  // Early returns for loading/error states
  if (!data) {
    return <LoadingSpinner />;
  }

  // Main render
  return (
    <div className="component-name">
      {/* JSX */}
    </div>
  );
}
```

### SQL Standards

```sql
-- Use explicit schema prefixes
SELECT
    g.node_id,
    g.node_name,
    g.created_at
FROM graphical.nodes g
WHERE g.status = 'active'
ORDER BY g.created_at DESC;

-- Migrations must be reversible
-- UP
CREATE TABLE IF NOT EXISTS graphical.nodes (...);

-- DOWN
DROP TABLE IF EXISTS graphical.nodes;
```

### Docker Standards

```yaml
# docker-compose.unified.yml
services:
  service-name:
    build:
      context: ./path
      dockerfile: Dockerfile
    container_name: integration-service-name  # Consistent naming
    environment:
      - ENV_VAR=${ENV_VAR:-default}  # Use defaults
    healthcheck:  # Always include
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - integration-network
```

### Commit Standards

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(frontend): add navigation component for module switching
fix(backend): correct database schema prefix for tagger module
docs(integration): update README with setup instructions
test(events): add integration tests for event bus
```

---

## Error Handling

### Backend Errors

```python
from fastapi import HTTPException
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
    code: str | None = None

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.DEBUG else None,
            code="INTERNAL_ERROR"
        ).dict()
    )
```

### Frontend Errors

```jsx
// Wrap async operations
async function fetchData() {
  try {
    const response = await api.get('/endpoint');
    return response.data;
  } catch (error) {
    if (error.response?.status === 401) {
      // Handle auth error
      redirectToLogin();
    } else if (error.response?.status === 404) {
      // Handle not found
      return null;
    } else {
      // Show user-friendly error
      showNotification({
        type: 'error',
        message: 'Failed to load data. Please try again.',
      });
      throw error;  // Re-throw for error boundary
    }
  }
}
```

---

## Testing Requirements

### Unit Tests

- Every new function with logic needs a test
- Test happy path and error cases
- Mock external dependencies

### Integration Tests

```python
# integration/tests/test_integration.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_cross_module_flow():
    """Test data flows from image-tagger to knowledge-graph."""
    async with AsyncClient(base_url="http://localhost") as client:
        # Create image in tagger
        response = await client.post("/api/tagger/images", json={...})
        assert response.status_code == 201
        image_id = response.json()["id"]

        # Wait for event propagation
        await asyncio.sleep(2)

        # Verify in knowledge graph
        response = await client.get(f"/api/graph/nodes?source={image_id}")
        assert response.status_code == 200
        assert len(response.json()["nodes"]) > 0
```

### E2E Tests

- Navigation between all modules works
- Data persists across page refreshes
- Authentication flows correctly

---

## Human Checkpoint Protocol

After completing each phase:

1. **Stop all implementation work**

2. **Generate audit package:**
   ```bash
   # Create audit directory
   mkdir -p integration/audits/phase_N

   # Copy relevant files
   cp integration/logs/phase_N_log.md integration/audits/phase_N/

   # Run verification
   python3 scripts/gate_check.py N > integration/audits/phase_N/gate_check.txt

   # Capture container status
   docker compose ps > integration/audits/phase_N/containers.txt

   # Generate file tree
   tree integration/ > integration/audits/phase_N/file_tree.txt
   ```

3. **Create summary for human review:**
   ```markdown
   # Phase N Complete - Ready for Review

   ## Summary
   [2-3 sentence summary of what was accomplished]

   ## Files Changed
   [List with brief descriptions]

   ## Verification Status
   - Gate check: PASSED/FAILED
   - Tests: X passed, Y failed
   - Manual verification: [what was checked]

   ## Screenshots
   [If applicable, especially for frontend]

   ## Known Issues
   [Any issues requiring human decision]

   ## Questions for Reviewer
   [Any clarifications needed]

   ## Next Phase Preview
   [What Phase N+1 will accomplish]
   ```

4. **Commit and tag:**
   ```bash
   git add -A
   git commit -m "Phase N complete: [summary]"
   git tag phase-N-checkpoint
   ```

5. **Wait for human approval before proceeding**

---

## Constraints and Boundaries

### Do NOT:

- Delete existing code without archiving it first
- Modify module internals beyond what's needed for integration
- Introduce new dependencies without justification
- Skip verification steps
- Proceed to next phase without human approval
- Make changes that break existing module functionality
- Ignore errors or warnings in verification
- Use placeholder implementations (`# TODO`, `pass`, `...`)

### Always:

- Read relevant CLAUDE.md files before modifying a module
- Run tests after every significant change
- Document decisions and rationale
- Follow existing patterns in the codebase
- Ask for clarification if requirements are ambiguous
- Create backups/archives before major changes
- Use type hints and docstrings
- Handle errors gracefully

---

## Quick Reference Commands

```bash
# Verification
python3 scripts/baseline_check.py          # Check module structure
python3 scripts/gate_check.py N            # Check phase N prerequisites
./scripts/verify_all.sh quick              # Quick health check
./scripts/verify_all.sh all                # Full verification

# Docker
docker compose -f integration/docker-compose.unified.yml up -d
docker compose -f integration/docker-compose.unified.yml logs -f
docker compose -f integration/docker-compose.unified.yml down

# Testing
pytest integration/tests/ -v               # Run all tests
pytest integration/tests/test_X.py -v      # Run specific test

# Database
docker exec -it integration-postgres psql -U admin -d unified_db

# Self-critique
python3 scripts/self_critique.py baseline  # Run self-assessment
```

---

## Success Criteria

The integration is complete when:

1. [ ] All 4 modules accessible from unified navigation
2. [ ] Consistent visual styling across all views
3. [ ] Shared authentication working
4. [ ] Cross-module events propagating correctly
5. [ ] All gate checks pass
6. [ ] All tests pass
7. [ ] Documentation complete and accurate
8. [ ] Human reviewer has approved each phase
9. [ ] System can be started with single `docker compose up` command
10. [ ] README provides clear setup instructions for new users
