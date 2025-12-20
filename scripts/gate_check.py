#!/usr/bin/env python3
"""
gate_check.py - Phase gate verification for integration project

This script verifies that all prerequisites are met before proceeding
to the next phase. It implements the verification gates defined in
VERIFICATION_PLAN.md.

Usage:
    python scripts/gate_check.py <phase>

Phases:
    0 or baseline     - Check baseline (before any changes)
    1 or infra        - Check infrastructure setup
    2 or backends     - Check backend standardization
    3 or frontend     - Check frontend unification
    4 or integration  - Check inter-module integration
    5 or final        - Final verification
"""

import sys
import subprocess
import json
import socket
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

BASE_DIR = Path(__file__).parent.parent


class GateCheck:
    """Phase gate verification."""

    def __init__(self, phase: str):
        self.phase = phase
        self.results: List[Tuple[str, bool, str]] = []
        self.timestamp = datetime.now().isoformat()

    def check(self, name: str, condition: bool, details: str = "") -> bool:
        """Record a check result."""
        self.results.append((name, condition, details))
        icon = "\033[92m✓\033[0m" if condition else "\033[91m✗\033[0m"
        print(f"  {icon} {name}")
        if details and not condition:
            print(f"      → {details}")
        return condition

    def file_exists(self, path: str, name: str = None) -> bool:
        """Check if a file exists."""
        full_path = BASE_DIR / path
        exists = full_path.exists()
        return self.check(
            name or f"File exists: {path}",
            exists,
            f"Missing: {full_path}" if not exists else ""
        )

    def dir_exists(self, path: str, name: str = None) -> bool:
        """Check if a directory exists."""
        full_path = BASE_DIR / path
        exists = full_path.is_dir()
        return self.check(
            name or f"Directory exists: {path}",
            exists,
            f"Missing: {full_path}" if not exists else ""
        )

    def port_available(self, port: int) -> bool:
        """Check if a port is available (not in use)."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            sock.close()
            return self.check(f"Port {port} available", True)
        except OSError:
            return self.check(f"Port {port} available", False, f"Port {port} already in use")

    def port_responding(self, port: int, name: str = None) -> bool:
        """Check if something is responding on a port."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            sock.connect(('localhost', port))
            sock.close()
            return self.check(name or f"Port {port} responding", True)
        except (socket.timeout, ConnectionRefusedError, OSError):
            return self.check(name or f"Port {port} responding", False, "Connection refused")

    def command_succeeds(self, cmd: List[str], name: str = None) -> bool:
        """Check if a command succeeds."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=30,
                cwd=str(BASE_DIR)
            )
            success = result.returncode == 0
            return self.check(
                name or f"Command: {' '.join(cmd[:2])}...",
                success,
                result.stderr.decode()[:100] if not success else ""
            )
        except subprocess.TimeoutExpired:
            return self.check(name or f"Command: {' '.join(cmd[:2])}...", False, "Timeout")
        except FileNotFoundError:
            return self.check(name or f"Command: {' '.join(cmd[:2])}...", False, "Command not found")

    def docker_available(self) -> bool:
        """Check if Docker is available."""
        return self.command_succeeds(["docker", "version"], "Docker available")

    def summary(self) -> bool:
        """Print summary and return overall pass/fail."""
        passed = sum(1 for _, ok, _ in self.results if ok)
        failed = sum(1 for _, ok, _ in self.results if not ok)

        print()
        print("=" * 50)
        print(f"GATE CHECK: Phase {self.phase}")
        print(f"Results: {passed} passed, {failed} failed")
        print("=" * 50)

        all_pass = failed == 0

        if all_pass:
            print("\n\033[92mGATE PASSED\033[0m - Ready to proceed to next phase")
        else:
            print("\n\033[91mGATE FAILED\033[0m - Address failures before proceeding")

        # Save results
        self._save_results()

        return all_pass

    def _save_results(self):
        """Save gate check results to file."""
        results_dir = BASE_DIR / "scripts" / "gate_logs"
        results_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"gate_{self.phase}_{timestamp}.json"

        data = {
            "phase": self.phase,
            "timestamp": self.timestamp,
            "checks": [
                {"name": name, "passed": ok, "details": details}
                for name, ok, details in self.results
            ],
            "passed": sum(1 for _, ok, _ in self.results if ok),
            "failed": sum(1 for _, ok, _ in self.results if not ok)
        }

        with open(results_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\nResults saved to: {results_file}")


def check_phase_0():
    """Phase 0: Baseline check - before any integration changes."""
    print("\n" + "=" * 50)
    print("PHASE 0: BASELINE VERIFICATION")
    print("=" * 50)
    print()

    gate = GateCheck("0-baseline")

    # Core documents
    gate.file_exists("INTEGRATION_PLAN.md", "Integration plan document")
    gate.file_exists("VERIFICATION_PLAN.md", "Verification plan document")
    gate.file_exists("CLAUDE.md", "Root CLAUDE.md")

    # Scripts
    gate.file_exists("scripts/baseline_check.py", "Baseline check script")
    gate.file_exists("scripts/verify_all.sh", "Verification script")
    gate.file_exists("scripts/self_critique.py", "Self-critique script")

    # Module presence
    print("\n[Module Structure]")
    gate.dir_exists("graphical-model", "graphical-model exists")
    gate.file_exists("graphical-model/api/main.py", "graphical-model API")

    gate.dir_exists("image-tagger", "image-tagger exists")

    gate.dir_exists("article-eater", "article-eater exists")

    gate.dir_exists("knowledge-graph-ui", "knowledge-graph-ui exists")

    # Run baseline check script
    print("\n[Baseline Script]")
    gate.command_succeeds(
        ["python3", "scripts/baseline_check.py"],
        "Baseline check script passes"
    )

    return gate.summary()


def check_phase_1():
    """Phase 1: Infrastructure - Docker, database, gateway."""
    print("\n" + "=" * 50)
    print("PHASE 1: INFRASTRUCTURE VERIFICATION")
    print("=" * 50)
    print()

    gate = GateCheck("1-infrastructure")

    # Prerequisites
    print("[Prerequisites]")
    gate.docker_available()
    gate.command_succeeds(["docker", "compose", "version"], "Docker Compose v2 available")

    # Integration directory
    print("\n[Integration Directory]")
    gate.dir_exists("integration", "Integration directory")
    gate.dir_exists("integration/nginx", "Nginx config directory")
    gate.dir_exists("integration/db-init", "Database init directory")

    # Docker Compose
    print("\n[Docker Compose]")
    if (BASE_DIR / "integration/docker-compose.unified.yml").exists():
        gate.file_exists("integration/docker-compose.unified.yml", "Unified docker-compose")
        gate.command_succeeds(
            ["docker", "compose", "-f", "integration/docker-compose.unified.yml", "config"],
            "Docker Compose syntax valid"
        )
    else:
        gate.check("Unified docker-compose", False, "Not created yet")

    # Nginx config
    print("\n[Nginx]")
    gate.file_exists("integration/nginx/nginx.conf", "Nginx configuration")

    # Database init
    print("\n[Database]")
    gate.file_exists("integration/db-init/00_create_schemas.sql", "Schema creation SQL")

    # Port availability (if services not running)
    print("\n[Port Availability]")
    for port in [5432, 6379, 8080, 8001, 8002, 8003, 8004]:
        gate.port_available(port)

    return gate.summary()


def check_phase_2():
    """Phase 2: Backend standardization."""
    print("\n" + "=" * 50)
    print("PHASE 2: BACKEND VERIFICATION")
    print("=" * 50)
    print()

    gate = GateCheck("2-backends")

    # Backend services responding
    print("[Backend Health Checks]")
    backends = [
        (8001, "graphical-model"),
        (8002, "image-tagger"),
        (8003, "article-eater"),
        (8004, "knowledge-graph-ui")
    ]

    for port, name in backends:
        gate.port_responding(port, f"{name} backend (:{port})")

    # Gateway routing
    print("\n[Gateway Routing]")
    gate.port_responding(8080, "Nginx gateway (:8080)")

    # Database connectivity
    print("\n[Database]")
    gate.port_responding(5432, "PostgreSQL (:5432)")
    gate.port_responding(6379, "Redis (:6379)")

    return gate.summary()


def check_phase_3():
    """Phase 3: Frontend unification."""
    print("\n" + "=" * 50)
    print("PHASE 3: FRONTEND VERIFICATION")
    print("=" * 50)
    print()

    gate = GateCheck("3-frontend")

    # Frontend shell
    print("[Frontend Shell]")
    gate.dir_exists("integration/frontend-shell", "Frontend shell directory")
    gate.file_exists("integration/frontend-shell/package.json", "package.json")
    gate.file_exists("integration/frontend-shell/src/App.jsx", "Main App component")

    # Build output
    print("\n[Build Output]")
    gate.dir_exists("integration/frontend-shell/dist", "Build output directory")
    gate.file_exists("integration/frontend-shell/dist/index.html", "Built index.html")

    # Frontend serving
    print("\n[Frontend Serving]")
    gate.port_responding(8080, "Frontend via Nginx (:8080)")

    return gate.summary()


def check_phase_4():
    """Phase 4: Inter-module integration."""
    print("\n" + "=" * 50)
    print("PHASE 4: INTEGRATION VERIFICATION")
    print("=" * 50)
    print()

    gate = GateCheck("4-integration")

    # Event bus
    print("[Event Bus]")
    gate.port_responding(6379, "Redis for event bus")

    # All services
    print("\n[All Services Running]")
    gate.port_responding(5432, "PostgreSQL")
    gate.port_responding(6379, "Redis")
    gate.port_responding(8080, "Nginx gateway")
    gate.port_responding(8001, "graphical-model")
    gate.port_responding(8002, "image-tagger")
    gate.port_responding(8003, "article-eater")
    gate.port_responding(8004, "knowledge-graph-ui")

    # Shared auth
    print("\n[Shared Authentication]")
    gate.file_exists("integration/shared/auth.py", "Shared auth module")

    return gate.summary()


def check_phase_5():
    """Phase 5: Final verification."""
    print("\n" + "=" * 50)
    print("PHASE 5: FINAL VERIFICATION")
    print("=" * 50)
    print()

    gate = GateCheck("5-final")

    # All components
    print("[Full System Check]")

    # Documentation
    gate.file_exists("INTEGRATION_PLAN.md", "Integration plan")
    gate.file_exists("VERIFICATION_PLAN.md", "Verification plan")
    gate.file_exists("integration/README.md", "Integration README")

    # Infrastructure
    print("\n[Infrastructure]")
    gate.file_exists("integration/docker-compose.unified.yml", "Docker Compose")
    gate.file_exists("integration/nginx/nginx.conf", "Nginx config")

    # All services responding
    print("\n[Services]")
    for port in [5432, 6379, 8080, 8001, 8002, 8003, 8004]:
        gate.port_responding(port)

    # Tests
    print("\n[Tests]")
    gate.file_exists("integration/tests/test_integration.py", "Integration tests")

    return gate.summary()


def main():
    phases = {
        "0": check_phase_0, "baseline": check_phase_0,
        "1": check_phase_1, "infra": check_phase_1, "infrastructure": check_phase_1,
        "2": check_phase_2, "backends": check_phase_2,
        "3": check_phase_3, "frontend": check_phase_3,
        "4": check_phase_4, "integration": check_phase_4,
        "5": check_phase_5, "final": check_phase_5,
    }

    if len(sys.argv) < 2:
        print("Gate Check - Phase Verification")
        print()
        print("Usage: python scripts/gate_check.py <phase>")
        print()
        print("Phases:")
        print("  0, baseline      - Check baseline (before changes)")
        print("  1, infra         - Check infrastructure setup")
        print("  2, backends      - Check backend standardization")
        print("  3, frontend      - Check frontend unification")
        print("  4, integration   - Check inter-module integration")
        print("  5, final         - Final verification")
        print()
        return 1

    phase = sys.argv[1].lower()

    if phase not in phases:
        print(f"Unknown phase: {phase}")
        print(f"Valid phases: 0-5, baseline, infra, backends, frontend, integration, final")
        return 1

    success = phases[phase]()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
