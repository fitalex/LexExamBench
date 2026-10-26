"""Original synthetic metadata only; no exam questions or answers."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_index import validate_document  # noqa: E402


def synthetic_record():
    right = {"status": "pending", "evidence_url": None}
    return {
        "id": "synthetic-2017-001",
        "exam_system": "national-judicial-exam",
        "year": 2017,
        "paper": "synthetic-paper",
        "question_number": "synthetic-1",
        "question_type": "single-choice",
        "subject": "synthetic-placeholder",
        "source_url": "https://example.org/synthetic-source",
        "answer_source_url": None,
        "provenance_grade": "synthetic",
        "rights": {k: copy.deepcopy(right) for k in
                   ("question_copy", "answer_copy", "storage", "redistribution", "external_model")},
        "law_time_status": "unknown",
        "expert_review": "pending",
        "split": "unassigned",
    }


class IndexValidationTests(unittest.TestCase):
    def test_empty_index_is_valid_but_not_a_dataset(self):
        self.assertEqual([], validate_document({"schema_version": "0.1.0", "questions": []}))

    def test_synthetic_metadata_is_valid(self):
        self.assertEqual([], validate_document({"schema_version": "0.1.0", "questions": [synthetic_record()]}))

    def test_duplicate_id_rejected(self):
        x = synthetic_record()
        self.assertTrue(validate_document({"schema_version": "0.1.0", "questions": [x, x]}))

    def test_unlicensed_body_field_rejected(self):
        x = synthetic_record()
        x["question_text"] = "REDACTED"
        self.assertTrue(validate_document({"schema_version": "0.1.0", "questions": [x]}))

    def test_rights_verified_without_evidence_rejected(self):
        x = synthetic_record()
        x["rights"]["external_model"]["status"] = "verified"
        self.assertTrue(validate_document({"schema_version": "0.1.0", "questions": [x]}))

    def test_examination_system_year_mismatch_rejected(self):
        x = synthetic_record()
        x["year"] = 2022
        self.assertTrue(validate_document({"schema_version": "0.1.0", "questions": [x]}))

    def test_secret_holdout_split_rejected(self):
        x = synthetic_record()
        x["split"] = "holdout"
        self.assertTrue(validate_document({"schema_version": "0.1.0", "questions": [x]}))

    def test_legal_professional_approval_must_not_be_faked(self):
        x = synthetic_record()
        x["expert_review"] = "approved"
        self.assertTrue(validate_document({"schema_version": "0.1.0", "questions": [x]}))


if __name__ == "__main__":
    unittest.main()
