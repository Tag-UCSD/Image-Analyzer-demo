#!/bin/bash
#
# setup_harness.sh - Set up the AI development harness
#
# This script prepares the environment for running the integration
# harness, including Python dependencies, directory structure, and
# initial validation.
#
# Usage:
#   ./scripts/setup_harness.sh          # Full setup
#   ./scripts/setup_harness.sh --check  # Check setup only
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$BASE_DIR/.venv"
REQ_FILE="$BASE_DIR/integration/requirements.txt"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
}

# Check if we're just doing a check
CHECK_ONLY=false
if [[ "$1" == "--check" ]]; then
    CHECK_ONLY=true
fi

header "AI Development Harness Setup"

# Step 1: Check Python
info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    success "Python installed: $PYTHON_VERSION"
else
    error "Python 3 not found. Please install Python 3.8+."
    exit 1
fi

# Step 2: Check/Create virtual environment
info "Checking virtual environment..."
if [ -d "$VENV_DIR" ]; then
    success "Virtual environment exists: $VENV_DIR"
else
    if [ "$CHECK_ONLY" = true ]; then
        warn "Virtual environment not found: $VENV_DIR"
    else
        info "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
        success "Created virtual environment: $VENV_DIR"
    fi
fi

# Step 3: Activate virtual environment
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    success "Activated virtual environment"
fi

# Step 4: Install dependencies
info "Checking dependencies..."
if [ -f "$REQ_FILE" ]; then
    if [ "$CHECK_ONLY" = true ]; then
        if python -c "import redis; import jsonschema" 2>/dev/null; then
            success "Dependencies installed"
        else
            warn "Some dependencies missing. Run without --check to install."
        fi
    else
        info "Installing dependencies from $REQ_FILE..."
        python -m pip install -q --upgrade pip
        python -m pip install -q -r "$REQ_FILE"
        success "Dependencies installed"
    fi
else
    warn "Requirements file not found: $REQ_FILE"
fi

# Step 5: Check Docker
info "Checking Docker..."
if command -v docker &> /dev/null; then
    if docker info &> /dev/null; then
        success "Docker is running"
    else
        warn "Docker installed but not running"
    fi
else
    warn "Docker not installed (optional for development)"
fi

# Step 6: Check Docker Compose
info "Checking Docker Compose..."
if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version --short)
    success "Docker Compose v2: $COMPOSE_VERSION"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    success "Docker Compose v1: $COMPOSE_VERSION"
else
    warn "Docker Compose not found (optional for development)"
fi

# Step 7: Create required directories
info "Checking directory structure..."
REQUIRED_DIRS=(
    "scripts/gate_logs"
    "scripts/critique_logs"
    "integration/logs"
    "integration/audits"
    "contracts"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    full_path="$BASE_DIR/$dir"
    if [ -d "$full_path" ]; then
        success "Directory exists: $dir"
    else
        if [ "$CHECK_ONLY" = true ]; then
            warn "Directory missing: $dir"
        else
            mkdir -p "$full_path"
            success "Created directory: $dir"
        fi
    fi
done

# Step 8: Check required files
info "Checking required files..."
REQUIRED_FILES=(
    "AGENT_INSTRUCTIONS.md"
    "DATA_FLOW_INTEGRATION_PLAN.md"
    "VERIFICATION_PLAN.md"
    "scripts/baseline_check.py"
    "scripts/gate_check.py"
    "scripts/self_critique.py"
    "scripts/verify_all.sh"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$BASE_DIR/$file" ]; then
        success "File exists: $file"
    else
        warn "File missing: $file"
        ((MISSING_FILES++)) || true
    fi
done

# Step 9: Check contract schemas
info "Checking contract schemas..."
SCHEMA_COUNT=$(find "$BASE_DIR/contracts" -name "*.schema.json" 2>/dev/null | wc -l | tr -d ' ')
if [ "$SCHEMA_COUNT" -gt 0 ]; then
    success "Found $SCHEMA_COUNT contract schema(s)"
    if python -c "import jsonschema" 2>/dev/null; then
        if python "$SCRIPT_DIR/validate_contracts.py" --check-schemas &> /dev/null; then
            success "All schemas are valid JSON Schema"
        else
            warn "Some schemas have validation errors"
        fi
    fi
else
    warn "No contract schemas found in contracts/"
fi

# Step 10: Make scripts executable
if [ "$CHECK_ONLY" = false ]; then
    info "Making scripts executable..."
    chmod +x "$SCRIPT_DIR"/*.sh "$SCRIPT_DIR"/*.py 2>/dev/null || true
    success "Scripts are executable"
fi

# Step 11: Run baseline check
info "Running baseline check..."
if python3 "$SCRIPT_DIR/baseline_check.py" &> /dev/null; then
    success "Baseline check passed"
else
    warn "Baseline check has warnings (see: python3 scripts/baseline_check.py)"
fi

# Summary
header "Setup Summary"

if [ "$CHECK_ONLY" = true ]; then
    echo "Mode: Check only (no changes made)"
else
    echo "Mode: Full setup"
fi

echo ""
echo "Virtual environment: $VENV_DIR"
echo ""
echo "To activate the environment:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To run the baseline check:"
echo "  python3 scripts/baseline_check.py"
echo ""
echo "To run gate checks:"
echo "  python3 scripts/gate_check.py 0"
echo ""
echo "To validate contract schemas:"
echo "  python3 scripts/validate_contracts.py --check-schemas"
echo ""

if [ $MISSING_FILES -gt 0 ]; then
    warn "$MISSING_FILES required file(s) missing"
    exit 1
else
    success "Harness setup complete!"
fi
