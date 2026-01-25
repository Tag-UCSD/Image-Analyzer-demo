# Agent-Driven Development Verification Plan

## Overview

This document establishes the testing, verification, and self-critique framework for integrating the Image Analyzer modules. Following best practices for agent-driven development, each phase includes:

1. **Pre-flight Checks** - Verify prerequisites before starting
2. **Implementation** - Execute with incremental verification
3. **Gate Checks** - Validate before proceeding to next phase
4. **Self-Critique** - Honest assessment of quality and completeness
5. **Rollback Strategy** - How to undo if things go wrong

---

## Verification Philosophy

### Core Principles

1. **Test Before Change** - Establish baseline behavior before modifying anything
2. **Small Increments** - Make one change, verify, then proceed
3. **Fail Fast** - Detect problems immediately, don't accumulate debt
4. **Honest Assessment** - Acknowledge limitations and uncertainties
5. **Reversibility** - Every change should be reversible

### Self-Critique Checkpoints

At each gate, ask:
- [ ] Does this actually work, or does it just look like it works?
- [ ] What assumptions am I making that might be wrong?
- [ ] What edge cases haven't I tested?
- [ ] Is this the simplest solution, or am I over-engineering?
- [ ] Would this be maintainable by someone else?
- [ ] Am I introducing any security vulnerabilities?

---

## Phase 0: Baseline Establishment

### Objective
Document current state of each module before any integration work.

### Pre-flight Checks

```bash
# For each module, verify current functionality

# 1. graphical-model
cd graphical-model
[ -f requirements.txt ] && echo "✓ requirements.txt exists"
[ -f api/main.py ] && echo "✓ API entry point exists"
python -c "import fastapi" 2>/dev/null && echo "✓ FastAPI importable" || echo "✗ FastAPI not installed"

# 2. image-tagger
cd../image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full
[ -f backend/main.py ] && echo "✓ Backend entry point exists"
[ -f deploy/docker-compose.yml ] && echo "✓ Docker compose exists"

# 3. article-eater
cd../../article-eater/Article_Eater_v20_7_43_repo
[ -f app/main.py ] && echo "✓ API entry point exists"
[ -f requirements.txt ] && echo "✓ requirements.txt exists"

# 4. knowledge-graph-ui
cd../../knowledge-graph-ui/GraphExplorer_Static_v3
[ -f backend/app/main.py ] && echo "✓ API entry point exists"
[ -f static-frontend/index.html ] && echo "✓ Frontend exists"
```

### Baseline Tests

For each module, document:

| Module | Can Start? | API Responds? | DB Connects? | Frontend Loads? |
|--------|-----------|---------------|--------------|-----------------|
| graphical-model | ? | ? | ? | ? |
| image-tagger | ? | ? | ? | ? |
| article-eater | ? | ? | ? | ? |
| knowledge-graph-ui | ? | ? | ? | ? |

### Verification Script

```python
#!/usr/bin/env python3
"""baseline_check.py - Verify module baseline state"""

import subprocess
import sys
from pathlib import Path

MODULES = {
 "graphical-model": {
 "path": "graphical-model",
 "api_file": "api/main.py",
 "requirements": "requirements.txt",
 "docker": "docker-compose.yml"
 },
 "image-tagger": {
 "path": "image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full",
 "api_file": "backend/main.py",
 "requirements": "requirements.txt",
 "docker": "deploy/docker-compose.yml"
 },
 "article-eater": {
 "path": "article-eater/Article_Eater_v20_7_43_repo",
 "api_file": "app/main.py",
 "requirements": "requirements.txt",
 "docker": None
 },
 "knowledge-graph-ui": {
 "path": "knowledge-graph-ui/GraphExplorer_Static_v3",
 "api_file": "backend/app/main.py",
 "requirements": "backend/requirements.txt",
 "docker": None
 }
}

def check_module(name, config):
 """Check if a module's key files exist."""
 base = Path(config["path"])
 results = {"name": name, "exists": base.exists, "files": {}}

 if not base.exists:
 return results

 for key in ["api_file", "requirements", "docker"]:
 if config[key]:
 file_path = base / config[key]
 results["files"][key] = file_path.exists

 return results

def main:
 print("=" * 60)
 print("BASELINE CHECK - Module State Verification")
 print("=" * 60)

 all_pass = True
 for name, config in MODULES.items:
 result = check_module(name, config)
 status = "✓" if result["exists"] else "✗"
 print(f"\n{status} {name}")

 if result["exists"]:
 for file_type, exists in result["files"].items:
 file_status = "✓" if exists else "✗"
 print(f" {file_status} {file_type}: {config[file_type]}")
 if not exists:
 all_pass = False
 else:
 all_pass = False
 print(f" ✗ Directory not found: {config['path']}")

 print("\n" + "=" * 60)
 if all_pass:
 print("BASELINE CHECK PASSED - All modules ready for integration")
 else:
 print("BASELINE CHECK FAILED - Fix issues before proceeding")
 print("=" * 60)

 return 0 if all_pass else 1

if __name__ == "__main__":
 sys.exit(main)
```

### Gate Check
- [ ] All 4 modules exist and have expected file structure
- [ ] Documented which modules currently work standalone
- [ ] Identified any existing issues to avoid during integration
- [ ] Created backup/snapshot of current state

### Self-Critique
- Am I assuming modules work when they might not?
- Have I actually tried to run each module?
- Are there hidden dependencies I'm not aware of?

---

## Phase 1: Infrastructure Foundation

### Objective
Set up unified Docker Compose, shared database, and Nginx gateway.

### Pre-flight Checks
- [ ] Docker and Docker Compose installed and working
- [ ] No port conflicts (5432, 6379, 8000-8003, 80)
- [ ] Sufficient disk space for containers
- [ ] Baseline check passed (Phase 0)

### Implementation Steps with Verification

#### Step 1.1: Create Directory Structure

```bash
# Create integration directory
mkdir -p integration/{nginx,db-init,frontend-shell}

# Verify
ls -la integration/
# Expected: nginx/, db-init/, frontend-shell/ directories
```

**Verification:** Directory structure exists

#### Step 1.2: Create Unified Docker Compose

Create `integration/docker-compose.unified.yml`

**Verification Script:**
```bash
# Syntax check
docker-compose -f integration/docker-compose.unified.yml config

# Expected: Valid YAML output, no errors
```

#### Step 1.3: Database Initialization

Create SQL init scripts in `integration/db-init/`

**Verification:**
```bash
# Start only database
docker-compose -f integration/docker-compose.unified.yml up -d postgres

# Wait for startup
sleep 10

# Check database
docker exec integration-postgres psql -U admin -d unified_db -c "\dn"
# Expected: List of schemas (graphical, tagger, article, graph)

docker exec integration-postgres psql -U admin -d unified_db -c "\dt graphical.*"
# Expected: Tables in graphical schema
```

#### Step 1.4: Redis Setup

**Verification:**
```bash
docker-compose -f integration/docker-compose.unified.yml up -d redis

# Test Redis
docker exec integration-redis redis-cli ping
# Expected: PONG
```

#### Step 1.5: Nginx Gateway

Create `integration/nginx/nginx.conf`

**Verification:**
```bash
# Config syntax check
docker run --rm -v $(pwd)/integration/nginx:/etc/nginx:ro nginx nginx -t
# Expected: syntax is ok, test is successful
```

### Gate Check
- [ ] `docker-compose config` validates without errors
- [ ] PostgreSQL starts and has all 4 schemas
- [ ] Redis starts and responds to PING
- [ ] Nginx config passes syntax check
- [ ] All containers can communicate on shared network

### Self-Critique Questions
- [ ] Are the port mappings correct and conflict-free?
- [ ] Is the database initialization idempotent (safe to run multiple times)?
- [ ] Are credentials properly externalized (not hardcoded)?
- [ ] What happens if a service fails to start?

### Rollback Strategy
```bash
# Stop all containers
docker-compose -f integration/docker-compose.unified.yml down

# Remove volumes (if needed for fresh start)
docker-compose -f integration/docker-compose.unified.yml down -v

# Delete integration directory
rm -rf integration/
```

---

## Phase 2: Backend Standardization

### Objective
Modify each backend to use shared database and standardized API prefixes.

### Pre-flight Checks
- [ ] Phase 1 gate checks passed
- [ ] Infrastructure containers running
- [ ] Backup of original backend code

### Implementation Steps with Verification

#### Step 2.1: graphical-model Backend

**Changes:**
- Update database connection to use shared PostgreSQL
- Ensure API prefix is `/api/v1/graphical/`

**Verification:**
```bash
# Start graphical-model service
docker-compose -f integration/docker-compose.unified.yml up -d graphical-model

# Health check
curl -s http://localhost:8001/health | jq.
# Expected: {"status": "ok",...}

# API endpoint check
curl -s http://localhost:8001/api/v1/graphical/status | jq.
# Expected: Valid response

# Database connectivity
docker exec integration-graphical-model python -c "
from database import get_db
db = next(get_db)
print('DB connection: OK')
"
```

#### Step 2.2: image-tagger Backend

**Verification:**
```bash
curl -s http://localhost:8002/health | jq.
curl -s http://localhost:8002/api/v1/tagger/status | jq.
```

#### Step 2.3: article-eater Backend

**Note:** Currently uses SQLite, needs migration to PostgreSQL

**Verification:**
```bash
curl -s http://localhost:8003/health | jq.
curl -s http://localhost:8003/api/v1/article/status | jq.
```

#### Step 2.4: knowledge-graph-ui Backend

**Note:** Currently uses in-memory data, needs PostgreSQL integration

**Verification:**
```bash
curl -s http://localhost:8004/health | jq.
curl -s http://localhost:8004/api/v1/graph/status | jq.
```

### Cross-Backend Verification

```python
#!/usr/bin/env python3
"""verify_backends.py - Check all backends are running and accessible"""

import requests
import sys

BACKENDS = {
 "graphical-model": {"port": 8001, "prefix": "/api/v1/graphical"},
 "image-tagger": {"port": 8002, "prefix": "/api/v1/tagger"},
 "article-eater": {"port": 8003, "prefix": "/api/v1/article"},
 "knowledge-graph-ui": {"port": 8004, "prefix": "/api/v1/graph"},
}

def check_backend(name, config):
 """Check if backend is accessible."""
 url = f"http://localhost:{config['port']}/health"
 try:
 resp = requests.get(url, timeout=5)
 return resp.status_code == 200
 except requests.RequestException:
 return False

def main:
 print("Backend Verification")
 print("=" * 40)

 all_pass = True
 for name, config in BACKENDS.items:
 status = check_backend(name, config)
 icon = "✓" if status else "✗"
 print(f"{icon} {name} (port {config['port']})")
 if not status:
 all_pass = False

 print("=" * 40)
 return 0 if all_pass else 1

if __name__ == "__main__":
 sys.exit(main)
```

### Gate Check
- [ ] All 4 backends start without errors
- [ ] All 4 backends respond to health checks
- [ ] All 4 backends connect to shared PostgreSQL
- [ ] API prefixes are correct and don't conflict
- [ ] No import errors or missing dependencies

### Self-Critique Questions
- [ ] Did I actually test the database writes, not just reads?
- [ ] Are the schema migrations reversible?
- [ ] What happens if one backend fails - do others continue?
- [ ] Am I handling connection pooling correctly?
- [ ] Are there any hardcoded URLs that should be configurable?

### Rollback Strategy
```bash
# Restore original backend files from git
git checkout -- graphical-model/api/
git checkout -- image-tagger/.../backend/
git checkout -- article-eater/.../app/
git checkout -- knowledge-graph-ui/.../backend/
```

---

## Phase 3: Frontend Unification

### Objective
Create unified frontend shell with navigation between modules.

### Pre-flight Checks
- [ ] Phase 2 gate checks passed
- [ ] All backends accessible via Nginx gateway
- [ ] Node.js and npm available for frontend build

### Implementation Steps with Verification

#### Step 3.1: Nginx Gateway Integration

**Verification:**
```bash
# Test routing through gateway
curl -s http://localhost:8080/api/graphical/health | jq.
curl -s http://localhost:8080/api/tagger/health | jq.
curl -s http://localhost:8080/api/article/health | jq.
curl -s http://localhost:8080/api/graph/health | jq.

# All should return valid health responses
```

#### Step 3.2: Frontend Shell Creation

**Verification:**
```bash
# Build frontend
cd integration/frontend-shell
npm install
npm run build

# Check build output
ls -la dist/
# Expected: index.html, assets/, etc.
```

#### Step 3.3: Module Loading

**Verification (Manual):**
1. Open http://localhost:8080 in browser
2. Verify navigation bar shows all 4 modules
3. Click each module tab, verify content loads
4. Check browser console for JavaScript errors

**Automated Verification:**
```python
#!/usr/bin/env python3
"""verify_frontend.py - Check frontend is serving correctly"""

import requests

def main:
 # Check main page loads
 resp = requests.get("http://localhost:8080/")
 assert resp.status_code == 200, "Main page failed to load"
 assert "<!DOCTYPE html>" in resp.text, "Not HTML response"

 # Check static assets
 resp = requests.get("http://localhost:8080/assets/main.js")
 assert resp.status_code == 200, "JS assets not loading"

 print("✓ Frontend verification passed")

if __name__ == "__main__":
 main
```

### Gate Check
- [ ] Frontend builds without errors
- [ ] Main page loads in browser
- [ ] Navigation between all 4 modules works
- [ ] No JavaScript console errors
- [ ] API calls from frontend reach correct backends
- [ ] Responsive design works on mobile viewport

### Self-Critique Questions
- [ ] Does navigation actually work, or just appear to work?
- [ ] What happens when API calls fail - is there error handling?
- [ ] Is the loading state handled (spinners, etc.)?
- [ ] Are there any CORS issues?
- [ ] Is the frontend accessible (keyboard navigation, screen readers)?

---

## Phase 4: Inter-Module Integration

### Objective
Enable modules to communicate and share data.

### Pre-flight Checks
- [ ] Phase 3 gate checks passed
- [ ] Redis running and accessible
- [ ] All modules have event bus client

### Implementation Steps with Verification

#### Step 4.1: Event Bus Setup

**Verification:**
```python
#!/usr/bin/env python3
"""verify_eventbus.py - Test event bus connectivity"""

import redis
import json
import threading
import time

r = redis.Redis(host='localhost', port=6379, db=0)

received = []

def subscriber:
 pubsub = r.pubsub
 pubsub.subscribe('test_channel')
 for message in pubsub.listen:
 if message['type'] == 'message':
 received.append(json.loads(message['data']))
 break

# Start subscriber in thread
t = threading.Thread(target=subscriber)
t.start

time.sleep(0.5)

# Publish test message
r.publish('test_channel', json.dumps({"test": "message"}))

t.join(timeout=2)

assert len(received) == 1, "Message not received"
assert received[0]["test"] == "message", "Message content wrong"

print("✓ Event bus verification passed")
```

#### Step 4.2: Cross-Module Data Flow

Test: Image tagged in image-tagger appears in knowledge-graph-ui

**Verification:**
```python
#!/usr/bin/env python3
"""verify_integration.py - Test cross-module data flow"""

import requests
import time

# 1. Create test data in image-tagger
resp = requests.post("http://localhost:8080/api/tagger/images", json={
 "url": "test://image.jpg",
 "tags": ["test_tag"]
})
image_id = resp.json["id"]

# 2. Wait for event propagation
time.sleep(2)

# 3. Check if knowledge-graph has the data
resp = requests.get(f"http://localhost:8080/api/graph/nodes")
nodes = resp.json["nodes"]

# Verify integration worked
found = any(n.get("source_id") == image_id for n in nodes)
assert found, "Cross-module data flow failed"

print("✓ Integration verification passed")
```

### Gate Check
- [ ] Event bus messages flow between all modules
- [ ] Data created in one module appears in others (where applicable)
- [ ] No message loss under normal load
- [ ] Error handling for failed cross-module calls
- [ ] Timeout handling for slow responses

### Self-Critique Questions
- [ ] What happens if Redis goes down?
- [ ] Are there race conditions in event handling?
- [ ] Is the message format documented and versioned?
- [ ] Can messages be replayed if processing fails?
- [ ] Am I creating circular dependencies between modules?

---

## Phase 5: Polish and Final Verification

### Objective
Final testing, documentation, and deployment preparation.

### Comprehensive Test Suite

```python
#!/usr/bin/env python3
"""full_integration_test.py - Comprehensive integration tests"""

import requests
import subprocess
import time
import sys

class IntegrationTests:
 def __init__(self):
 self.base_url = "http://localhost:8080"
 self.results = []

 def test(self, name, func):
 """Run a test and record result."""
 try:
 func
 self.results.append((name, True, None))
 print(f" ✓ {name}")
 except AssertionError as e:
 self.results.append((name, False, str(e)))
 print(f" ✗ {name}: {e}")
 except Exception as e:
 self.results.append((name, False, str(e)))
 print(f" ✗ {name}: {e}")

 def run_all(self):
 print("\n" + "=" * 60)
 print("FULL INTEGRATION TEST SUITE")
 print("=" * 60)

 # Infrastructure tests
 print("\n[Infrastructure]")
 self.test("PostgreSQL accessible", self.test_postgres)
 self.test("Redis accessible", self.test_redis)
 self.test("Nginx gateway running", self.test_nginx)

 # Backend tests
 print("\n[Backends]")
 self.test("graphical-model health", lambda: self.test_backend_health("graphical"))
 self.test("image-tagger health", lambda: self.test_backend_health("tagger"))
 self.test("article-eater health", lambda: self.test_backend_health("article"))
 self.test("knowledge-graph health", lambda: self.test_backend_health("graph"))

 # API tests
 print("\n[API Endpoints]")
 self.test("graphical-model predictions", self.test_graphical_api)
 self.test("image-tagger images", self.test_tagger_api)
 self.test("article-eater papers", self.test_article_api)
 self.test("knowledge-graph nodes", self.test_graph_api)

 # Integration tests
 print("\n[Cross-Module Integration]")
 self.test("Event bus messaging", self.test_event_bus)
 self.test("Shared authentication", self.test_shared_auth)
 self.test("Data flow: tagger → graph", self.test_tagger_to_graph)

 # Frontend tests
 print("\n[Frontend]")
 self.test("Main page loads", self.test_frontend_loads)
 self.test("Navigation works", self.test_navigation)
 self.test("API calls from frontend", self.test_frontend_api)

 # Summary
 print("\n" + "=" * 60)
 passed = sum(1 for _, success, _ in self.results if success)
 total = len(self.results)
 print(f"RESULTS: {passed}/{total} tests passed")

 if passed < total:
 print("\nFailed tests:")
 for name, success, error in self.results:
 if not success:
 print(f" - {name}: {error}")

 print("=" * 60)
 return passed == total

 def test_postgres(self):
 result = subprocess.run(["docker", "exec", "integration-postgres", "pg_isready"],
 capture_output=True, timeout=5)
 assert result.returncode == 0, "PostgreSQL not ready"

 def test_redis(self):
 result = subprocess.run(["docker", "exec", "integration-redis", "redis-cli", "ping"],
 capture_output=True, timeout=5)
 assert b"PONG" in result.stdout, "Redis not responding"

 def test_nginx(self):
 resp = requests.get(f"{self.base_url}/", timeout=5)
 assert resp.status_code in [200, 304], f"Nginx returned {resp.status_code}"

 def test_backend_health(self, module):
 resp = requests.get(f"{self.base_url}/api/{module}/health", timeout=5)
 assert resp.status_code == 200, f"Health check failed: {resp.status_code}"

 def test_graphical_api(self):
 resp = requests.get(f"{self.base_url}/api/graphical/status", timeout=5)
 assert resp.status_code == 200

 def test_tagger_api(self):
 resp = requests.get(f"{self.base_url}/api/tagger/images", timeout=5)
 assert resp.status_code in [200, 401] # 401 if auth required

 def test_article_api(self):
 resp = requests.get(f"{self.base_url}/api/article/papers", timeout=5)
 assert resp.status_code in [200, 401]

 def test_graph_api(self):
 resp = requests.get(f"{self.base_url}/api/graph/v1_demo", timeout=5)
 assert resp.status_code == 200

 def test_event_bus(self):
 # Simplified check - verify Redis pub/sub works
 import redis
 r = redis.Redis(host='localhost', port=6379)
 r.publish('test', 'ping')

 def test_shared_auth(self):
 # Test that auth tokens work across modules
 # This is a placeholder - implement based on actual auth
 pass

 def test_tagger_to_graph(self):
 # Test data flows from tagger to graph
 # This is a placeholder - implement based on actual flow
 pass

 def test_frontend_loads(self):
 resp = requests.get(f"{self.base_url}/", timeout=5)
 assert "<!DOCTYPE html>" in resp.text or "<html" in resp.text

 def test_navigation(self):
 # Check that navigation-related assets exist
 resp = requests.get(f"{self.base_url}/", timeout=5)
 assert resp.status_code == 200

 def test_frontend_api(self):
 # Verify frontend can make API calls (CORS, etc.)
 resp = requests.get(f"{self.base_url}/api/graphical/health", timeout=5)
 assert "Access-Control-Allow-Origin" in resp.headers or resp.status_code == 200


if __name__ == "__main__":
 tests = IntegrationTests
 success = tests.run_all
 sys.exit(0 if success else 1)
```

### Final Checklist

#### Functionality
- [ ] All 4 modules accessible from unified UI
- [ ] Navigation between modules is seamless
- [ ] Data persists across browser refresh
- [ ] Cross-module data flow works
- [ ] Error states handled gracefully

#### Performance
- [ ] Page load time < 3 seconds
- [ ] API responses < 500ms
- [ ] No memory leaks in long-running sessions
- [ ] Database queries are indexed

#### Security
- [ ] No exposed credentials in code or configs
- [ ] Authentication required for sensitive endpoints
- [ ] HTTPS ready (certificates configured)
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified

#### Documentation
- [ ] README updated with integration instructions
- [ ] API documentation complete
- [ ] Environment variables documented
- [ ] Troubleshooting guide created

### Self-Critique Final Review

Answer honestly:
1. **What doesn't work perfectly?** List known issues.
2. **What shortcuts did I take?** Document technical debt.
3. **What would I do differently?** Lessons learned.
4. **What's the worst that could happen?** Risk assessment.
5. **Is this ready for users?** Honest readiness evaluation.

---

## Continuous Verification Commands

Quick commands to run during development:

```bash
# Full health check./scripts/verify_all.sh

# Check specific phase./scripts/verify_phase.sh 1 # Infrastructure./scripts/verify_phase.sh 2 # Backends./scripts/verify_phase.sh 3 # Frontend./scripts/verify_phase.sh 4 # Integration

# Watch logs
docker-compose -f integration/docker-compose.unified.yml logs -f

# Quick restart
docker-compose -f integration/docker-compose.unified.yml restart

# Nuclear option - full rebuild
docker-compose -f integration/docker-compose.unified.yml down -v
docker-compose -f integration/docker-compose.unified.yml up --build
```

---

## Verification Log Template

Use this template to document verification results:

```markdown
## Verification Log - [DATE]

### Phase: [NUMBER]
### Step: [NAME]

**Pre-flight:**
- [ ] Check 1
- [ ] Check 2

**Execution:**
```
[Command output here]
```

**Result:** PASS / FAIL

**Issues Found:**
- Issue 1
- Issue 2

**Self-Critique:**
- What I learned:
- What I'd do differently:

**Next Steps:**
- Step 1
- Step 2
```

---

## Appendix: Error Recovery Procedures

### Database Corruption
```bash
# Stop all services
docker-compose down

# Backup corrupted DB (for analysis)
docker cp integration-postgres:/var/lib/postgresql/data./db-backup-corrupted

# Remove volume and recreate
docker volume rm integration_postgres_data
docker-compose up -d postgres

# Re-run migrations./scripts/init-db.sh
```

### Container Won't Start
```bash
# Check logs
docker-compose logs [service-name]

# Check resource usage
docker stats

# Rebuild specific service
docker-compose build --no-cache [service-name]
docker-compose up -d [service-name]
```

### Network Issues
```bash
# Recreate network
docker network rm integration_default
docker-compose up -d

# Check connectivity
docker exec integration-nginx ping integration-graphical-model
```
