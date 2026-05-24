import json
import sys
from pathlib import Path

from jsonschema import validate, ValidationError


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    root = Path(__file__).resolve().parent.parent
    schema_path = root / "schemas" / "evaluation-result.schema.json"

    if not schema_path.exists():
        print(f"Schema not found: {schema_path}")
        sys.exit(1)

    schema = load_json(schema_path)

    result_files = sorted(root.glob("examples/**/evaluation-result.json"))

    if not result_files:
        print("No evaluation-result.json files found under examples/.")
        sys.exit(0)

    passed = 0
    failed = 0

    for result_path in result_files:
        rel = result_path.relative_to(root)
        try:
            data = load_json(result_path)
            validate(instance=data, schema=schema)
            print(f"PASS  {rel}")
            passed += 1
        except ValidationError as e:
            print(f"FAIL  {rel}")
            print(f"      {e.message}")
            failed += 1
        except json.JSONDecodeError as e:
            print(f"FAIL  {rel}")
            print(f"      Invalid JSON: {e}")
            failed += 1

    print()
    print(f"Summary: {passed} passed, {failed} failed, {len(result_files)} total")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
