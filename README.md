# LexExamBench

An independent, versioned **Chinese legal-exam benchmark data project**. LexExamBench indexes historical Chinese National Judicial Examination materials and later National Unified Legal Professional Qualification Examination sources, with traceable provenance, rights, and legal-date review status.

**This public repository does not contain examination question text or answer text.** Public access to a source is not permission to copy, redistribute or submit its content to a third-party model.

## Getting started (Python 3.11+)

```sh
python -m pip install -r requirements.txt
python scripts/validate_index.py
python -m unittest discover -s tests -v
```

The starter index intentionally contains **0 verified question records**. A successful validator run proves only that the metadata structure is valid; it does not establish a populated dataset or legal accuracy.

## Layout

- `data/questions/index.json`: public **metadata-only** question index; initially empty.
- `data/sources/index.json`: source records; initially empty.
- `schemas/question-index.schema.json`: public index contract.
- `scripts/validate_index.py`: offline schema and rights-boundary validation.
- `tests/`: synthetic-only engineering tests.
- `LICENSE_POLICY.md`: code/content licensing separation and unknown-rights guardrails.

## Boundaries

- Pre-2018 National Judicial Examination and the 2018-onward legal qualification examination are not interchangeable source types.
- Historical official answer keys do **not** automatically establish current-law correctness.
- Public and private Holdout material must be kept in separate storage. Nothing confidential belongs in this repository or public CI.
- No legal proficiency scores, real provider calls, or LexRouter Skill rankings are produced by this bootstrap.
- Any future licensed dataset must explicitly document rights to retain, publish, and process question **and** answer material.

## Integration

[LexRouter](https://github.com/fitalex/LexRouter) is a separate project. Future integrations must pin a **release / commit and dataset hash**, rather than reading a mutable dataset HEAD.

Tracking: [LexRouter LR-P2-01](https://github.com/fitalex/LexRouter/issues/16).

## Status

LEB-01 minimal bootstrap for Codex Cloud environment setup. The 30-question **index-only source-audit pilot remains pending** and should be implemented in a separate Draft PR.
