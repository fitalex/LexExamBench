"""Offline validation for the public, metadata-only LexExamBench index."""
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "data" / "questions" / "index.json"
SCHEMA = ROOT / "schemas" / "question-index.schema.json"
SENSITIVE_KEYS = {
    "question_text", "question_body", "answer_text", "answer",
    "answers", "options", "explanation", "solution", "content", "prompt",
}


def validate_document(document):
    """Return errors without contacting any remote source."""
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = [
        f"/{'/'.join(str(p) for p in err.absolute_path)}: {err.message}"
        for err in Draft202012Validator(schema).iter_errors(document)
    ]
    if not isinstance(document, dict):
        return errors
    questions = document.get("questions")
    if not isinstance(questions, list):
        return errors
    seen_ids = set()
    seen_source_positions = set()
    for n, entry in enumerate(questions):
        path = f"/questions/{n}"
        if not isinstance(entry, dict):
            continue
        if SENSITIVE_KEYS.intersection(entry):
            errors.append(f"{path}: question/answer body fields are forbidden in public index")
        identifier = entry.get("id")
        if isinstance(identifier, str):
            if identifier in seen_ids:
                errors.append(f"{path}: duplicate id {identifier}")
            seen_ids.add(identifier)
        position = (entry.get("exam_system"), entry.get("year"), entry.get("paper"), entry.get("question_number"))
        if all(v is not None for v in position):
            if position in seen_source_positions:
                errors.append(f"{path}: duplicate original exam position")
            seen_source_positions.add(position)
        year = entry.get("year")
        exam = entry.get("exam_system")
        if type(year) is int:
            if exam == "national-judicial-exam" and year >= 2018:
                errors.append(f"{path}: 2018+ cannot be tagged national-judicial-exam")
            if exam == "national-legal-qualification-exam" and year < 2018:
                errors.append(f"{path}: pre-2018 cannot be tagged national-legal-qualification-exam")
            if exam == "national-legal-qualification-exam" and entry.get("provenance_grade") == "official-exam":
                errors.append(f"{path}: post-2018 published real-exam question requires new provenance review")
        if entry.get("expert_review") == "approved":
            errors.append(f"{path}: expert approval cannot be asserted in bootstrap index")
        if entry.get("law_time_status") in ("historical-reviewed", "current-reviewed"):
            errors.append(f"{path}: legal time review cannot be asserted in bootstrap index")
        rights = entry.get("rights")
        if isinstance(rights, dict):
            for dimension, claim in rights.items():
                if isinstance(claim, dict) and claim.get("status") == "verified":
                    ev = claim.get("evidence_url")
                    if not isinstance(ev, str) or not ev.startswith("https://"):
                        errors.append(f"{path}/rights/{dimension}: verified requires HTTPS evidence URL")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate metadata-only public question index")
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_INDEX)
    args = parser.parse_args(argv)
    try:
        document = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"INDEX_ERROR: {exc}", file=sys.stderr)
        return 1
    errors = validate_document(document)
    for error in errors:
        print(f"INDEX_INVALID: {error}", file=sys.stderr)
    if errors:
        return 1
    count = len(document["questions"])
    print(f"INDEX_VALID: {count} metadata record(s); legal/rights review not established.")
    if count == 0:
        print("INDEX_EMPTY: no actual exam question indexes have been collected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
