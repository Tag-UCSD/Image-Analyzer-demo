#!/usr/bin/env python3
"""
self_critique.py - Self-critique framework for agent-driven development

This script provides structured self-assessment checkpoints to ensure
quality, completeness, and honest evaluation of work.

Usage:
    python scripts/self_critique.py [phase]

Phases: baseline, infrastructure, backends, frontend, integration, final
"""

import sys
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

# Self-critique questions organized by phase
CRITIQUE_QUESTIONS = {
    "baseline": {
        "title": "Phase 0: Baseline Establishment",
        "questions": [
            {
                "id": "B1",
                "question": "Have I actually verified each module works standalone?",
                "check": "Did you run each module, not just check files exist?",
                "risk": "Assuming modules work when they don't"
            },
            {
                "id": "B2",
                "question": "Are there hidden dependencies not captured in requirements.txt?",
                "check": "System packages, environment variables, external services?",
                "risk": "Integration will fail due to missing dependencies"
            },
            {
                "id": "B3",
                "question": "Do I understand each module's database schema?",
                "check": "Can you describe tables, relationships, constraints?",
                "risk": "Schema conflicts during consolidation"
            },
            {
                "id": "B4",
                "question": "Are there any existing tests I should preserve?",
                "check": "Test suites, fixtures, CI/CD configurations?",
                "risk": "Breaking existing test coverage"
            },
            {
                "id": "B5",
                "question": "Do I have a rollback plan for each module?",
                "check": "Git state, database backups, configuration backups?",
                "risk": "Unable to recover from failed integration"
            }
        ]
    },
    "infrastructure": {
        "title": "Phase 1: Infrastructure Foundation",
        "questions": [
            {
                "id": "I1",
                "question": "Is my Docker Compose configuration correct?",
                "check": "Syntax validated? Service dependencies correct? Volumes mapped?",
                "risk": "Containers fail to start or communicate"
            },
            {
                "id": "I2",
                "question": "Are there port conflicts with existing services?",
                "check": "Checked localhost ports 5432, 6379, 8000-8004, 80?",
                "risk": "Services fail to bind to ports"
            },
            {
                "id": "I3",
                "question": "Is database initialization idempotent?",
                "check": "Safe to run multiple times? Uses IF NOT EXISTS?",
                "risk": "Data corruption on restart"
            },
            {
                "id": "I4",
                "question": "Are credentials properly externalized?",
                "check": "Using environment variables? No secrets in code?",
                "risk": "Security vulnerabilities, deployment issues"
            },
            {
                "id": "I5",
                "question": "What happens if a service fails to start?",
                "check": "Health checks? Restart policies? Failure isolation?",
                "risk": "Cascading failures, unclear error states"
            },
            {
                "id": "I6",
                "question": "Can I actually connect to each service?",
                "check": "Tested PostgreSQL, Redis, Nginx connections manually?",
                "risk": "Assuming network works when it doesn't"
            }
        ]
    },
    "backends": {
        "title": "Phase 2: Backend Standardization",
        "questions": [
            {
                "id": "K1",
                "question": "Are all backends using the shared database correctly?",
                "check": "Connection strings? Schema prefixes? Connection pooling?",
                "risk": "Database connection failures in production"
            },
            {
                "id": "K2",
                "question": "Did I test database writes, not just reads?",
                "check": "Insert, update, delete operations verified?",
                "risk": "Read-only testing misses write permission issues"
            },
            {
                "id": "K3",
                "question": "Are the schema migrations reversible?",
                "check": "Can you roll back each migration safely?",
                "risk": "Unable to recover from failed migrations"
            },
            {
                "id": "K4",
                "question": "Are there hardcoded URLs that should be configurable?",
                "check": "Localhost references? Hardcoded ports? Service names?",
                "risk": "Deployment failures in different environments"
            },
            {
                "id": "K5",
                "question": "What happens if one backend fails - do others continue?",
                "check": "Failure isolation? Graceful degradation?",
                "risk": "Single point of failure takes down entire system"
            },
            {
                "id": "K6",
                "question": "Are API prefixes consistent and non-conflicting?",
                "check": "All use /api/{module}/ pattern? No route collisions?",
                "risk": "Wrong backend receives requests"
            }
        ]
    },
    "frontend": {
        "title": "Phase 3: Frontend Unification",
        "questions": [
            {
                "id": "F1",
                "question": "Does navigation actually work between modules?",
                "check": "Clicked all nav links? State preserved? Deep links work?",
                "risk": "Navigation appears to work but doesn't"
            },
            {
                "id": "F2",
                "question": "What happens when API calls fail?",
                "check": "Error handling? User feedback? Retry logic?",
                "risk": "Silent failures confuse users"
            },
            {
                "id": "F3",
                "question": "Are there any CORS issues?",
                "check": "Cross-origin requests work? Credentials handled?",
                "risk": "API calls blocked in browser"
            },
            {
                "id": "F4",
                "question": "Is loading state handled appropriately?",
                "check": "Spinners? Skeleton screens? No layout shift?",
                "risk": "Poor user experience during loads"
            },
            {
                "id": "F5",
                "question": "Is the frontend accessible?",
                "check": "Keyboard navigation? Screen reader support? Color contrast?",
                "risk": "Excluding users with disabilities"
            },
            {
                "id": "F6",
                "question": "Did I check browser console for errors?",
                "check": "JavaScript errors? Network errors? Warnings?",
                "risk": "Hidden errors causing subtle bugs"
            }
        ]
    },
    "integration": {
        "title": "Phase 4: Inter-Module Integration",
        "questions": [
            {
                "id": "G1",
                "question": "What happens if Redis goes down?",
                "check": "Fallback behavior? Error handling? Reconnection?",
                "risk": "Event bus failure breaks cross-module features"
            },
            {
                "id": "G2",
                "question": "Are there race conditions in event handling?",
                "check": "Message ordering? Duplicate handling? Timing issues?",
                "risk": "Intermittent failures hard to debug"
            },
            {
                "id": "G3",
                "question": "Is the message format documented and versioned?",
                "check": "Schema defined? Version field? Forward compatibility?",
                "risk": "Breaking changes during updates"
            },
            {
                "id": "G4",
                "question": "Can messages be replayed if processing fails?",
                "check": "Dead letter queue? Retry mechanism? Idempotent handlers?",
                "risk": "Lost messages during failures"
            },
            {
                "id": "G5",
                "question": "Am I creating circular dependencies?",
                "check": "Module A calls B calls A? Deadlock potential?",
                "risk": "System hangs or stack overflows"
            },
            {
                "id": "G6",
                "question": "Is authentication truly shared?",
                "check": "Same token works across all modules? Token refresh?",
                "risk": "Users must re-authenticate between modules"
            }
        ]
    },
    "final": {
        "title": "Phase 5: Final Verification",
        "questions": [
            {
                "id": "Z1",
                "question": "What doesn't work perfectly?",
                "check": "List ALL known issues, even minor ones.",
                "risk": "Undocumented issues surprise users"
            },
            {
                "id": "Z2",
                "question": "What shortcuts did I take?",
                "check": "Technical debt incurred? TODO items remaining?",
                "risk": "Shortcuts become long-term problems"
            },
            {
                "id": "Z3",
                "question": "What would I do differently next time?",
                "check": "Lessons learned? Better approaches identified?",
                "risk": "Repeating the same mistakes"
            },
            {
                "id": "Z4",
                "question": "What's the worst that could happen?",
                "check": "Data loss? Security breach? Downtime scenarios?",
                "risk": "Unprepared for failure modes"
            },
            {
                "id": "Z5",
                "question": "Is this actually ready for users?",
                "check": "Honest assessment. Would YOU use this?",
                "risk": "Shipping broken software"
            },
            {
                "id": "Z6",
                "question": "Is the documentation accurate?",
                "check": "README matches reality? API docs current? Setup works?",
                "risk": "Users can't get started"
            }
        ]
    }
}


def run_critique(phase: str) -> dict:
    """Run self-critique for a specific phase."""
    if phase not in CRITIQUE_QUESTIONS:
        print(f"Unknown phase: {phase}")
        print(f"Available phases: {', '.join(CRITIQUE_QUESTIONS.keys())}")
        sys.exit(1)

    critique = CRITIQUE_QUESTIONS[phase]
    results = {
        "phase": phase,
        "title": critique["title"],
        "timestamp": datetime.now().isoformat(),
        "responses": []
    }

    print("\n" + "=" * 70)
    print(f"SELF-CRITIQUE: {critique['title']}")
    print("=" * 70)
    print("\nAnswer each question honestly. Press Enter to skip.\n")

    for q in critique["questions"]:
        print(f"\n[{q['id']}] {q['question']}")
        print(f"    Check: {q['check']}")
        print(f"    Risk if ignored: {q['risk']}")
        print()

        response = input("    Your answer (or Enter to skip): ").strip()
        status = "answered" if response else "skipped"

        results["responses"].append({
            "id": q["id"],
            "question": q["question"],
            "response": response,
            "status": status
        })

    # Summary
    answered = sum(1 for r in results["responses"] if r["status"] == "answered")
    skipped = sum(1 for r in results["responses"] if r["status"] == "skipped")

    print("\n" + "=" * 70)
    print(f"CRITIQUE COMPLETE: {answered} answered, {skipped} skipped")

    if skipped > 0:
        print("\n⚠️  WARNING: Skipped questions represent unexamined risks!")
        print("    Consider revisiting skipped items before proceeding.")

    print("=" * 70)

    # Save results
    results_dir = BASE_DIR / "scripts" / "critique_logs"
    results_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = results_dir / f"critique_{phase}_{timestamp}.json"

    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {results_file}")

    return results


def list_phases():
    """Print all available phases."""
    print("\nAvailable self-critique phases:")
    print("-" * 40)
    for phase, info in CRITIQUE_QUESTIONS.items():
        count = len(info["questions"])
        print(f"  {phase:15} - {info['title']} ({count} questions)")
    print()


def run_all_phases():
    """Run critique for all phases (non-interactive summary)."""
    print("\n" + "=" * 70)
    print("SELF-CRITIQUE SUMMARY - All Phases")
    print("=" * 70)

    for phase, info in CRITIQUE_QUESTIONS.items():
        print(f"\n{info['title']}")
        print("-" * 50)
        for q in info["questions"]:
            print(f"  [{q['id']}] {q['question']}")
    print()


def main():
    if len(sys.argv) < 2:
        print("Self-Critique Framework for Agent-Driven Development")
        print("\nUsage:")
        print("  python scripts/self_critique.py <phase>    - Run critique for phase")
        print("  python scripts/self_critique.py list       - List all phases")
        print("  python scripts/self_critique.py all        - Show all questions")
        list_phases()
        return 0

    arg = sys.argv[1].lower()

    if arg == "list":
        list_phases()
    elif arg == "all":
        run_all_phases()
    else:
        run_critique(arg)

    return 0


if __name__ == "__main__":
    sys.exit(main())
