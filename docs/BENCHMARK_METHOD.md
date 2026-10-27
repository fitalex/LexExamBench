# Benchmark contract and Gate 1 method

This is a legal knowledge/reasoning exam index, not a measurement of the complete
legal practice capabilities of LexRouter Skills. Historical judicial exams through
2017 and national legal qualification exams from 2018 have distinct systems.
Exam scores are neither real exam certification nor proof of professional ability.

Contract v0.2 uses strict question and source JSON schemas. Every future item has
stable source-based ID, original year/paper/number, type/subject, original source
and answer locator, retrieval date, provenance revision, five separate rights
claims and evidence, historical law context, pending current-law and expert
reviews, and unassigned public/Holdout candidacy. Duplicate original positions
are rejected even if assigned different IDs. Cross-year/republished duplicate
content needs human comparison in a controlled licensed space; metadata checks
cannot detect semantic duplicates. Do not put actual body hashes/snapshots here.

Business mapping currently accepts only `no-direct-mapping`: the six LexRouter
business-category identifiers have not been authoritatively established in this
audit. A future reviewed vocabulary change may add those optional mappings;
never infer six categories from exam subjects. No LexRouter files were changed.

Rights vocabulary: `verified / pending / denied / not-applicable`. All five
body-use dimensions are currently pending. Gate 1 rejects verified or
not-applicable body-use claims, even with HTTPS evidence, because there is no
independently reviewed grant ledger. The schema can represent those states for a
future version, but a URL alone cannot make them valid. `denied` requires a
specific recorded basis. Source access is not a grant. Synthetic fixtures are
human-original metadata only, carry no real answer, and do not count as exams.

## Sampling and future evaluation (not implemented)

Target 24 objective plus 6 subjective items, prioritizing verified 2017 official
sources and extending to other verified years only if needed. Stratify by year,
subject and question type; report convenience-sample bias and all gaps. Current
sample: zero, so no coverage or performance claim is possible. Track overlap
with public training data and common corpora; public historical questions and
JEC-QA have substantial potential contamination. Publication date alone does not
prove exclusion from model training. Holdout membership itself stays private.

Future single-choice scoring uses exact option identity. Multiple/indefinite
choices require exact set equality without order sensitivity or partial credit.
Case/essay evaluation needs independently reviewed rubric dimensions, anchors,
weights, dual expert marking and adjudication. Rubrics and legal correctness are
pending; no model, scorer, answer ingestion or evaluation engine is implemented.
Compare scores within compatible types and denominators; do not imply objective
accuracy and subjective rubric points are interchangeable. Preserve historical
keys; flag legal reforms and current-law conflicts for expert calibration.

## Public/Holdout and consumption

This repository contains public metadata only, no real Holdout items, answers,
complete snapshots, membership manifest, or private storage pointer. Any future
Holdout must be placed in controlled external private storage with separate ACLs,
review and audit; Git ignore rules alone are not isolation. No actual split is
assigned. Structural checks and manual diff review cannot establish the absence
of secrets embedded in arbitrary prose; content review remains necessary.

Future independent consumers must pin repository release plus full commit SHA,
schema version and SHA256 of the exact UTF-8 index bytes, verifying before use.
A release manifest should list source-audit revision, grant-ledger revision and
expert-review revision. Mutable HEAD is not a valid consumption contract. No
release or licensed runnable dataset is created by this PR.

## Gate 2 inputs and stop boundary

- Licensed usable questions: **none**; body processing `BLOCKED_BY_RIGHTS`.
- Verified index input: **0/30**; original MOJ access/locators still needed.
- Expert queue: historical key/then-applicable law/current-law changes all pending
  (`LEGAL_REVIEW_PENDING`); no expert approval asserted.
- Pinning contract above is a draft, not a LexRouter integration change.

Gate 1 acceptance remains incomplete. Stop at Draft PR for ChatGPT engineering
review. Gate 2, model calls, scores, rankings, merges and roadmap changes require
a separate approved task.
