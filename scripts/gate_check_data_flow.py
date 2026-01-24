#!/usr/bin/env python3
"""
Data flow gate checks for backend integration.

Usage:
    python3 scripts/gate_check_data_flow.py <phase>

Phases:
    0 or baseline     - Baseline checks
    1 or db           - Database migrations & backend alignment
    2 or evidence     - Article-eater → knowledge-graph pipeline
    3 or tagger       - Image-tagger → graphical-model pipeline
    4 or bidirectional- Knowledge-graph ↔ graphical-model flow
    5 or final        - Final verification
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

import importlib.util
from pathlib import Path


def _load_gate_check():
    base_dir = Path(__file__).resolve().parent.parent
    gate_path = base_dir / "scripts" / "gate_check.py"
    spec = importlib.util.spec_from_file_location("gate_check", gate_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load gate_check from {gate_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_gate_module = _load_gate_check()
GateCheck = _gate_module.GateCheck
BASE_DIR = _gate_module.BASE_DIR


def _http_json(
    method: str,
    url: str,
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 5,
) -> Dict[str, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        body = response.read().decode("utf-8")
        if "application/json" not in content_type:
            raise ValueError("Response was not JSON")
        return json.loads(body)


def _check_json_endpoint(
    gate: GateCheck,
    name: str,
    method: str,
    url: str,
    payload: Optional[Dict[str, Any]] = None,
) -> bool:
    try:
        _http_json(method, url, payload=payload)
        return gate.check(name, True)
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as exc:
        return gate.check(name, False, str(exc))


def check_phase_0() -> bool:
    print("\n" + "=" * 50)
    print("DATA FLOW PHASE 0: BASELINE")
    print("=" * 50)
    print()

    gate = GateCheck("data-flow-0")
    gate.file_exists("DATA_FLOW_INTEGRATION_PLAN.md", "Data flow plan")
    gate.file_exists("AGENT_INSTRUCTIONS.md", "Agent instructions")
    gate.file_exists("VERIFICATION_PLAN.md", "Verification plan")
    gate.file_exists("graphical-model/CLAUDE.md", "graphical-model CLAUDE")
    gate.file_exists(
        "image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/CLAUDE.md",
        "image-tagger CLAUDE",
    )
    gate.file_exists("article-eater/Article_Eater_v20_7_43_repo/CLAUDE.md", "article-eater CLAUDE")
    gate.file_exists("knowledge-graph-ui/CLAUDE.md", "knowledge-graph CLAUDE")

    return gate.summary()


def check_phase_1() -> bool:
    print("\n" + "=" * 50)
    print("DATA FLOW PHASE 1: DB ALIGNMENT")
    print("=" * 50)
    print()

    gate = GateCheck("data-flow-1")
    gate.file_exists("integration/docker-compose.unified.yml", "Unified docker-compose")
    gate.port_responding(5432, "PostgreSQL")
    gate.port_responding(6379, "Redis")
    gate.command_succeeds(
        [
            "docker",
            "exec",
            "integration-postgres",
            "psql",
            "-U",
            "postgres",
            "-d",
            "image_analyzer",
            "-c",
            "\\dn",
        ],
        "Schemas available",
    )

    return gate.summary()


def check_phase_2() -> bool:
    print("\n" + "=" * 50)
    print("DATA FLOW PHASE 2: EVIDENCE → GRAPH")
    print("=" * 50)
    print()

    gate = GateCheck("data-flow-2")
    base_url = os.getenv("UNIFIED_API_BASE_URL", "http://localhost:8080").rstrip("/")

    _check_json_endpoint(
        gate,
        "Article-eater export",
        "POST",
        f"{base_url}/api/article/integration/export-to-graph",
    )
    _check_json_endpoint(
        gate,
        "Knowledge-graph update",
        "POST",
        f"{base_url}/api/graph/edges/update-from-findings",
        payload=[],
    )

    return gate.summary()


def check_phase_3() -> bool:
    print("\n" + "=" * 50)
    print("DATA FLOW PHASE 3: TAGGER → GRAPHICAL")
    print("=" * 50)
    print()

    gate = GateCheck("data-flow-3")
    base_url = os.getenv("UNIFIED_API_BASE_URL", "http://localhost:8080").rstrip("/")

    _check_json_endpoint(
        gate,
        "Tagger BN export",
        "GET",
        f"{base_url}/api/tagger/v1/export/bn-training-data",
    )
    _check_json_endpoint(
        gate,
        "Graphical import",
        "POST",
        f"{base_url}/api/graphical/integration/import-training-data",
        payload={"images": [], "trigger_retrain": False},
    )

    return gate.summary()


def check_phase_4() -> bool:
    print("\n" + "=" * 50)
    print("DATA FLOW PHASE 4: BIDIRECTIONAL GRAPH")
    print("=" * 50)
    print()

    gate = GateCheck("data-flow-4")
    base_url = os.getenv("UNIFIED_API_BASE_URL", "http://localhost:8080").rstrip("/")

    _check_json_endpoint(
        gate,
        "Knowledge-graph export",
        "GET",
        f"{base_url}/api/graph/export-for-bayesian",
    )
    _check_json_endpoint(
        gate,
        "Graphical publish posteriors",
        "POST",
        f"{base_url}/api/graphical/integration/publish-posteriors",
        payload={"model_version": "latest"},
    )
    _check_json_endpoint(
        gate,
        "Knowledge-graph update posteriors",
        "POST",
        f"{base_url}/api/graph/edges/update-from-posteriors",
        payload=[],
    )

    return gate.summary()


def check_phase_5() -> bool:
    print("\n" + "=" * 50)
    print("DATA FLOW PHASE 5: FINAL")
    print("=" * 50)
    print()

    gate = GateCheck("data-flow-5")
    gate.file_exists("integration/tests/test_data_flow.py", "Data flow test suite")
    gate.command_succeeds(["bash", "scripts/run_data_flow_tests.sh"], "Data flow tests")

    return gate.summary()


def main() -> int:
    phases = {
        "0": check_phase_0,
        "baseline": check_phase_0,
        "1": check_phase_1,
        "db": check_phase_1,
        "2": check_phase_2,
        "evidence": check_phase_2,
        "3": check_phase_3,
        "tagger": check_phase_3,
        "4": check_phase_4,
        "bidirectional": check_phase_4,
        "5": check_phase_5,
        "final": check_phase_5,
    }

    if len(sys.argv) < 2:
        print("Usage: python3 scripts/gate_check_data_flow.py <phase>")
        return 1

    phase = sys.argv[1]
    if phase not in phases:
        print(f"Unknown phase: {phase}")
        return 1

    return 0 if phases[phase]() else 1


if __name__ == "__main__":
    sys.exit(main())
