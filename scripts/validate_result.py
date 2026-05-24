import json
from pathlib import Path

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_basic_fields(data: dict) -> bool:
    required = ["case_id", "passed", "score", "criteria_results"]
    return all(field in data for field in required)

if __name__ == "__main__":
    sample_path = Path("examples/llm-answer-quality/evaluation-result.json")
    if not sample_path.exists():
        print("Sample evaluation result not found.")
        exit(1)

    result = load_json(str(sample_path))
    if validate_basic_fields(result):
        print("Basic evaluation result validation passed.")
    else:
        print("Basic evaluation result validation failed.")
