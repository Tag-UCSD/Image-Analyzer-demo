#!/bin/bash
set -euo pipefail

python3 -m unittest integration.tests.test_data_flow
