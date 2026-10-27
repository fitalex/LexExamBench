# Agents and contributor rules

- The public repository is `fitalex/LexExamBench`; `main` is stable. Subsequent substantive work takes place on a separate branch and Draft PR. Never force push or auto-merge.
- **No copyrighted question text, options, answer text, explanations, exam PDFs, private Holdout contents, secrets, real case files, or license correspondence** may enter public code, commits, PRs, fixtures, logs, or CI.
- Published source URLs and independently written metadata are not evidence of redistribution or third-party-model processing authorization. Keep the rights dimensions separate and explicit.
- 2017-and-earlier judicial exams and 2018+ legal qualification exams use distinct `exam_system` values; do not invent official post-2018 past papers or references.
- Historical official answer keys, historical governing law and current-law applicability are separate review events. No simulated legal expert signatures.
- Engineering tests use original synthetic metadata; do not contact paid AI/model APIs, scrape official sites, or download third-party question banks as part of CI.
- For every PR run `python scripts/validate_index.py` and `python -m unittest discover -s tests -v`; attach real exit codes and CI evidence. Default validation rejects an empty index. `--allow-empty` is an explicit structure-only diagnostic and **does not satisfy the 30-question pilot**.
- Source work is governed by [LexRouter Issue #16](https://github.com/fitalex/LexRouter/issues/16). Follow its Gate 1 rights, provenance and expert-review requirements. Do not change LexRouter itself.
