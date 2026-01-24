#!/usr/bin/env python3
"""
validate_contracts.py - Validate data against contract schemas

Usage:
    python scripts/validate_contracts.py <schema_name> <json_file>
    python scripts/validate_contracts.py --check-schemas

Examples:
    python scripts/validate_contracts.py evidence_export sample_export.json
    python scripts/validate_contracts.py training_data_export export.json
    python scripts/validate_contracts.py --check-schemas
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema package required. Install with: pip install jsonschema")
    sys.exit(1)


BASE_DIR = Path(__file__).resolve().parent.parent
CONTRACTS_DIR = BASE_DIR / "contracts"


def load_schema(name: str) -> Dict[str, Any]:
    """Load a JSON schema by name."""
    # Try with and without .schema.json suffix
    candidates = [
        CONTRACTS_DIR / f"{name}.schema.json",
        CONTRACTS_DIR / f"{name}",
    ]
    for path in candidates:
        if path.exists():
            with open(path) as f:
                return json.load(f)
    raise FileNotFoundError(f"Schema not found: {name}")


def validate_data(data: Any, schema_name: str) -> List[str]:
    """Validate data against a schema. Returns list of error messages."""
    schema = load_schema(schema_name)
    validator = jsonschema.Draft7Validator(schema)
    errors = []
    for error in validator.iter_errors(data):
        path = " -> ".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"{path}: {error.message}")
    return errors


def check_all_schemas() -> bool:
    """Validate that all schema files are valid JSON Schema."""
    print("Checking all contract schemas...")
    print()

    all_valid = True
    for schema_file in sorted(CONTRACTS_DIR.glob("*.schema.json")):
        print(f"  {schema_file.name}...", end=" ")
        try:
            with open(schema_file) as f:
                schema = json.load(f)
            jsonschema.Draft7Validator.check_schema(schema)
            print("\033[92mVALID\033[0m")
        except json.JSONDecodeError as e:
            print(f"\033[91mINVALID JSON\033[0m: {e}")
            all_valid = False
        except jsonschema.SchemaError as e:
            print(f"\033[91mINVALID SCHEMA\033[0m: {e.message}")
            all_valid = False

    print()
    if all_valid:
        print("\033[92mAll schemas are valid.\033[0m")
    else:
        print("\033[91mSome schemas have errors.\033[0m")

    return all_valid


def validate_file(schema_name: str, json_file: str) -> bool:
    """Validate a JSON file against a schema."""
    # Load the data
    json_path = Path(json_file)
    if not json_path.exists():
        print(f"Error: File not found: {json_file}")
        return False

    try:
        with open(json_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_file}: {e}")
        return False

    # Validate
    print(f"Validating {json_file} against {schema_name}...")
    print()

    errors = validate_data(data, schema_name)

    if not errors:
        print("\033[92mVALIDATION PASSED\033[0m")
        return True
    else:
        print(f"\033[91mVALIDATION FAILED\033[0m ({len(errors)} errors):")
        print()
        for error in errors[:20]:  # Limit to first 20 errors
            print(f"  - {error}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")
        return False


def list_schemas() -> None:
    """List available schemas."""
    print("Available schemas:")
    print()
    for schema_file in sorted(CONTRACTS_DIR.glob("*.schema.json")):
        name = schema_file.stem.replace(".schema", "")
        with open(schema_file) as f:
            schema = json.load(f)
        title = schema.get("title", "No title")
        print(f"  {name}")
        print(f"    {title}")
        print()


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        print()
        list_schemas()
        return 0

    if sys.argv[1] == "--check-schemas":
        return 0 if check_all_schemas() else 1

    if sys.argv[1] == "--list":
        list_schemas()
        return 0

    if len(sys.argv) < 3:
        print("Error: Missing arguments")
        print()
        print("Usage: python scripts/validate_contracts.py <schema_name> <json_file>")
        return 1

    schema_name = sys.argv[1]
    json_file = sys.argv[2]

    return 0 if validate_file(schema_name, json_file) else 1


if __name__ == "__main__":
    sys.exit(main())
