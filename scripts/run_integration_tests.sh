#!/bin/bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$BASE_DIR/.venv"
REQ_FILE="$BASE_DIR/integration/requirements.txt"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

if [ -f "$REQ_FILE" ]; then
  python -m pip install -q -r "$REQ_FILE"
fi

python -m unittest \
  integration.tests.test_auth \
  integration.tests.test_events \
  integration.tests.test_api_client \
  integration.tests.test_integration
