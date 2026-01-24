#!/usr/bin/env python3
"""
baseline_check.py - Verify module baseline state before integration

This script checks the current state of all modules to establish a baseline
before any integration work begins. It verifies:
1. Directory structure exists
2. Key files are present
3. Dependencies are defined
4. Docker configurations exist (where applicable)

Run this BEFORE making any integration changes.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Base directory (parent of scripts/)
BASE_DIR = Path(__file__).parent.parent

# Module configurations
MODULES = {
    "graphical-model": {
        "path": "graphical-model",
        "description": "Bayesian causal inference engine",
        "checks": {
            "api_entry": "api/main.py",
            "requirements": "requirements.txt",
            "docker": "docker-compose.yml",
            "database": "database/01_core_tables.sql",
            "claude_md": "CLAUDE.md"
        }
    },
    "image-tagger": {
        "path": "image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full",
        "description": "Image annotation system",
        "checks": {
            "api_entry": "backend/main.py",
            "requirements": "requirements-install.txt",
            "docker": "deploy/docker-compose.yml",
            "claude_md": "CLAUDE.md"
        }
    },
    "article-eater": {
        "path": "article-eater/Article_Eater_v20_7_43_repo",
        "description": "Evidence extraction from papers",
        "checks": {
            "api_entry": "app/main.py",
            "requirements": "requirements.txt",
            "claude_md": "CLAUDE.md"
        }
    },
    "knowledge-graph-ui": {
        "path": "knowledge-graph-ui/GraphExplorer_Static_v3",
        "description": "Graph visualization interface",
        "checks": {
            "api_entry": "backend/app/main.py",
            "requirements": "backend/requirements.txt",
            "frontend": "static-frontend/index.html"
        }
    },
    "experiments": {
        "path": "experiments",
        "description": "Experimental/prototype code",
        "checks": {
            "claude_md": "CLAUDE.md"
        }
    }
}


def check_file_exists(base_path: Path, relative_path: str) -> dict:
    """Check if a file exists and return details."""
    full_path = base_path / relative_path
    exists = full_path.exists()

    result = {
        "exists": exists,
        "path": str(relative_path)
    }

    if exists:
        stat = full_path.stat()
        result["size"] = stat.st_size
        result["modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()

    return result


def check_module(name: str, config: dict) -> dict:
    """Check a single module's baseline state."""
    base_path = BASE_DIR / config["path"]

    result = {
        "name": name,
        "description": config["description"],
        "path": config["path"],
        "exists": base_path.exists(),
        "checks": {}
    }

    if not base_path.exists():
        result["status"] = "MISSING"
        return result

    # Check each required file
    all_critical_pass = True
    for check_name, check_path in config["checks"].items():
        check_result = check_file_exists(base_path, check_path)
        result["checks"][check_name] = check_result

        # api_entry and requirements are critical
        if check_name in ["api_entry", "requirements"] and not check_result["exists"]:
            all_critical_pass = False

    result["status"] = "OK" if all_critical_pass else "INCOMPLETE"
    return result


def print_results(results: list) -> bool:
    """Print results in a readable format and return overall status."""
    print("\n" + "=" * 70)
    print("BASELINE CHECK - Module State Verification")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Base Directory: {BASE_DIR}")
    print("=" * 70)

    all_pass = True

    for result in results:
        status_icon = {
            "OK": "\033[92m✓\033[0m",           # Green check
            "INCOMPLETE": "\033[93m⚠\033[0m",    # Yellow warning
            "MISSING": "\033[91m✗\033[0m"        # Red X
        }.get(result["status"], "?")

        print(f"\n{status_icon} {result['name']}")
        print(f"   Description: {result['description']}")
        print(f"   Path: {result['path']}")
        print(f"   Status: {result['status']}")

        if result["status"] == "MISSING":
            print(f"   \033[91mDirectory not found!\033[0m")
            all_pass = False
            continue

        print("   Files:")
        for check_name, check_result in result["checks"].items():
            file_icon = "\033[92m✓\033[0m" if check_result["exists"] else "\033[91m✗\033[0m"
            print(f"      {file_icon} {check_name}: {check_result['path']}")

            if check_result["exists"]:
                size_kb = check_result["size"] / 1024
                print(f"         Size: {size_kb:.1f} KB | Modified: {check_result['modified']}")

        if result["status"] != "OK":
            all_pass = False

    print("\n" + "=" * 70)

    # Summary
    ok_count = sum(1 for r in results if r["status"] == "OK")
    incomplete_count = sum(1 for r in results if r["status"] == "INCOMPLETE")
    missing_count = sum(1 for r in results if r["status"] == "MISSING")

    print(f"SUMMARY: {ok_count} OK | {incomplete_count} Incomplete | {missing_count} Missing")

    if all_pass:
        print("\n\033[92mBASELINE CHECK PASSED\033[0m - All critical files present")
        print("Ready to proceed with integration work.")
    else:
        print("\n\033[93mBASELINE CHECK WARNING\033[0m - Some issues found")
        print("Review the issues above before proceeding.")

    print("=" * 70 + "\n")

    return all_pass


def save_baseline_report(results: list):
    """Save baseline report as JSON for future reference."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "base_directory": str(BASE_DIR),
        "modules": results
    }

    report_path = BASE_DIR / "scripts" / "baseline_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Baseline report saved to: {report_path}")


def main():
    """Run baseline checks on all modules."""
    results = []

    for name, config in MODULES.items():
        result = check_module(name, config)
        results.append(result)

    all_pass = print_results(results)
    save_baseline_report(results)

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
