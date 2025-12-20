#!/bin/bash
#
# verify_all.sh - Run all verification checks
#
# Usage:
#   ./scripts/verify_all.sh           # Run all checks
#   ./scripts/verify_all.sh quick     # Quick checks only
#   ./scripts/verify_all.sh phase N   # Check specific phase (0-5)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
PASSED=0
FAILED=0
WARNINGS=0

pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++)) || true
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++)) || true
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++)) || true
}

header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
}

# Phase 0: Baseline Checks
check_baseline() {
    header "Phase 0: Baseline Checks"

    # Run Python baseline check
    if python3 "$SCRIPT_DIR/baseline_check.py" > /dev/null 2>&1; then
        pass "Baseline check passed"
    else
        fail "Baseline check failed - run: python3 scripts/baseline_check.py"
    fi

    # Check for CLAUDE.md files
    for project in graphical-model image-tagger article-eater knowledge-graph-ui experiments; do
        if [ -f "$BASE_DIR/$project/CLAUDE.md" ] || [ -f "$BASE_DIR/$project"/*"/CLAUDE.md" ]; then
            pass "CLAUDE.md exists for $project"
        else
            warn "CLAUDE.md missing for $project"
        fi
    done

    # Check integration plan
    if [ -f "$BASE_DIR/INTEGRATION_PLAN.md" ]; then
        pass "Integration plan exists"
    else
        warn "Integration plan not found"
    fi

    # Check verification plan
    if [ -f "$BASE_DIR/VERIFICATION_PLAN.md" ]; then
        pass "Verification plan exists"
    else
        warn "Verification plan not found"
    fi
}

# Phase 1: Infrastructure Checks
check_infrastructure() {
    header "Phase 1: Infrastructure Checks"

    # Check Docker
    if command -v docker &> /dev/null; then
        pass "Docker installed"
    else
        fail "Docker not installed"
        return
    fi

    # Check Docker Compose
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        pass "Docker Compose available"
    else
        fail "Docker Compose not available"
    fi

    # Check integration directory
    if [ -d "$BASE_DIR/integration" ]; then
        pass "Integration directory exists"

        # Check docker-compose.unified.yml
        if [ -f "$BASE_DIR/integration/docker-compose.unified.yml" ]; then
            pass "Unified docker-compose exists"

            # Validate syntax
            if docker-compose -f "$BASE_DIR/integration/docker-compose.unified.yml" config > /dev/null 2>&1; then
                pass "Docker Compose syntax valid"
            else
                fail "Docker Compose syntax invalid"
            fi
        else
            warn "Unified docker-compose not created yet"
        fi

        # Check nginx config
        if [ -f "$BASE_DIR/integration/nginx/nginx.conf" ]; then
            pass "Nginx config exists"
        else
            warn "Nginx config not created yet"
        fi

        # Check db-init scripts
        if [ -d "$BASE_DIR/integration/db-init" ] && [ "$(ls -A "$BASE_DIR/integration/db-init" 2>/dev/null)" ]; then
            pass "Database init scripts exist"
        else
            warn "Database init scripts not created yet"
        fi
    else
        warn "Integration directory not created yet"
    fi

    # Check if containers are running (if docker-compose exists)
    if [ -f "$BASE_DIR/integration/docker-compose.unified.yml" ]; then
        if docker-compose -f "$BASE_DIR/integration/docker-compose.unified.yml" ps 2>/dev/null | grep -q "Up"; then
            pass "Integration containers running"
        else
            warn "Integration containers not running"
        fi
    fi
}

# Phase 2: Backend Checks
check_backends() {
    header "Phase 2: Backend Checks"

    # Check if we can reach backends (assumes they're running)
    backends=("graphical:8001" "tagger:8002" "article:8003" "graph:8004")

    for backend in "${backends[@]}"; do
        name="${backend%:*}"
        port="${backend#*:}"

        if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
            pass "$name backend responding on port $port"
        else
            warn "$name backend not responding on port $port"
        fi
    done

    # Check gateway routing (if nginx is running)
    if curl -s "http://localhost:8080/api/graphical/health" > /dev/null 2>&1; then
        pass "Gateway routing to graphical-model"
    else
        warn "Gateway routing not working (nginx may not be running)"
    fi
}

# Phase 3: Frontend Checks
check_frontend() {
    header "Phase 3: Frontend Checks"

    # Check if frontend shell exists
    if [ -d "$BASE_DIR/integration/frontend-shell" ]; then
        pass "Frontend shell directory exists"

        # Check for package.json
        if [ -f "$BASE_DIR/integration/frontend-shell/package.json" ]; then
            pass "package.json exists"
        else
            warn "package.json not created yet"
        fi

        # Check for build output
        if [ -d "$BASE_DIR/integration/frontend-shell/dist" ]; then
            pass "Frontend build output exists"
        else
            warn "Frontend not built yet"
        fi
    else
        warn "Frontend shell not created yet"
    fi

    # Check if frontend is being served
    if curl -s "http://localhost:8080/" | grep -q "html" 2>/dev/null; then
        pass "Frontend being served"
    else
        warn "Frontend not being served (nginx may not be running)"
    fi
}

# Phase 4: Integration Checks
check_integration() {
    header "Phase 4: Integration Checks"

    # Check Redis
    if docker exec integration-redis redis-cli ping 2>/dev/null | grep -q "PONG"; then
        pass "Redis responding"
    else
        warn "Redis not responding (may not be running)"
    fi

    # Check PostgreSQL
    if docker exec integration-postgres pg_isready 2>/dev/null; then
        pass "PostgreSQL ready"
    else
        warn "PostgreSQL not ready (may not be running)"
    fi

    # Check schemas exist
    if docker exec integration-postgres psql -U postgres -d image_analyzer -c "\dn" 2>/dev/null | grep -q "graphical"; then
        pass "Database schemas created"
    else
        warn "Database schemas not created yet"
    fi
}

# Quick checks only
check_quick() {
    header "Quick Verification"

    # Files exist
    [ -f "$BASE_DIR/INTEGRATION_PLAN.md" ] && pass "Integration plan" || warn "No integration plan"
    [ -f "$BASE_DIR/VERIFICATION_PLAN.md" ] && pass "Verification plan" || warn "No verification plan"
    [ -f "$BASE_DIR/scripts/baseline_check.py" ] && pass "Baseline check script" || warn "No baseline script"

    # Docker available
    command -v docker &> /dev/null && pass "Docker available" || fail "Docker not available"
}

# Summary
print_summary() {
    echo ""
    echo "========================================"
    echo "VERIFICATION SUMMARY"
    echo "========================================"
    echo -e "Passed:   ${GREEN}$PASSED${NC}"
    echo -e "Failed:   ${RED}$FAILED${NC}"
    echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
    echo "========================================"

    if [ $FAILED -gt 0 ]; then
        echo -e "${RED}VERIFICATION FAILED${NC} - Fix failures before proceeding"
        exit 1
    elif [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}VERIFICATION PASSED WITH WARNINGS${NC}"
        exit 0
    else
        echo -e "${GREEN}ALL CHECKS PASSED${NC}"
        exit 0
    fi
}

# Main
main() {
    cd "$BASE_DIR"

    case "${1:-all}" in
        quick)
            check_quick
            ;;
        phase)
            case "$2" in
                0|baseline) check_baseline ;;
                1|infrastructure) check_infrastructure ;;
                2|backends) check_backends ;;
                3|frontend) check_frontend ;;
                4|integration) check_integration ;;
                *) echo "Unknown phase: $2. Use 0-4 or name."; exit 1 ;;
            esac
            ;;
        all)
            check_baseline
            check_infrastructure
            check_backends
            check_frontend
            check_integration
            ;;
        *)
            echo "Usage: $0 [quick|all|phase N]"
            exit 1
            ;;
    esac

    print_summary
}

main "$@"
