# Actual local verification — 2026-10-29 (P1 scanner repair)

Base: `4a041eae4d44d12f8c75788c42793995efca6a4c`; branch:
`codex/leb-01-bootstrap-source-audit`.

Environment: Python 3.12.14; jsonschema 4.26.0; Linux managed LexExamBench cloud runtime.
Commands below actually ran. The default validator **fails** because 0/30 is
incomplete. Engineering CI uses the explicitly labeled structure-only diagnostic
and synthetic regression tests; a green CI does **not** mean Gate 1 accepted.

P1 repair: evaluate repository-relative paths; exempt only root `.git` metadata.
Scan `work/` and cache paths regardless of ignore rules, and union disk paths with
`git ls-files --cached -z` so force-added files remain checked after local deletion.
Git-index read failure rejects validation. No schema/source/data/CI-policy changes.

New regressions use empty synthetic files in ordinary, `<tmp>/work/repo/`, and
Actions-shaped `home/runner/work/LexExamBench/LexExamBench` checkouts. They cover
holdout, PDF, unregistered JSON, clean roots, work/cache nesting, forced staging
and subsequent disk deletion, Git metadata exclusion and index-read failure.
The old scanner fails the seven applicable new tests with 28 failing subcases;
the fixed implementation passes all 40 tests. The old-code comparison loads the
previous committed validator into the new regression module; its helper is scratch
only, while all regression fixtures/tests are committed.

```text
$ python work/check_old_scanner.py
Original implementation loaded from 10dcdcc with new filesystem regressions.

----------------------------------------------------------------------
Ran 7 tests in 0.031s

FAILED (failures=28)
exit_code=1
```

```text
$ python scripts/validate_index.py
INDEX_INVALID: empty dataset: pilot incomplete
exit_code=1
```

```text
$ python scripts/validate_index.py --allow-empty
INDEX_VALID: 0 metadata records; rights/legal review not established
PILOT_INCOMPLETE: 0/30; structure-only validation
exit_code=0
```

```text
$ python -m unittest discover -s tests -v
test_clean_roots_pass (test_public_tree.PublicTreeRegressionTests.test_clean_roots_pass) ... ok
test_force_added_ignored_files_checked_even_if_removed_from_worktree (test_public_tree.PublicTreeRegressionTests.test_force_added_ignored_files_checked_even_if_removed_from_worktree) ... ok
test_git_index_read_failure_rejects (test_public_tree.PublicTreeRegressionTests.test_git_index_read_failure_rejects) ... ok
test_git_metadata_is_excluded (test_public_tree.PublicTreeRegressionTests.test_git_metadata_is_excluded) ... ok
test_holdout_under_actions_checkout (test_public_tree.PublicTreeRegressionTests.test_holdout_under_actions_checkout) ... ok
test_pdf_under_actions_checkout (test_public_tree.PublicTreeRegressionTests.test_pdf_under_actions_checkout) ... ok
test_unregistered_data_under_actions_checkout (test_public_tree.PublicTreeRegressionTests.test_unregistered_data_under_actions_checkout) ... ok
test_work_and_cache_do_not_hide_forbidden_files (test_public_tree.PublicTreeRegressionTests.test_work_and_cache_do_not_hide_forbidden_files) ... ok
test_body_rejected (test_validate_index.IndexValidationTests.test_body_rejected) ... ok
test_current_law_forged (test_validate_index.IndexValidationTests.test_current_law_forged) ... ok
test_duplicate_id (test_validate_index.IndexValidationTests.test_duplicate_id) ... ok
test_duplicate_year_paper_number (test_validate_index.IndexValidationTests.test_duplicate_year_paper_number) ... ok
test_empty_rejected (test_validate_index.IndexValidationTests.test_empty_rejected) ... ok
test_empty_sources_rejected (test_validate_index.IndexValidationTests.test_empty_sources_rejected) ... ok
test_exam_year_mismatch (test_validate_index.IndexValidationTests.test_exam_year_mismatch) ... ok
test_expert_signature_forged (test_validate_index.IndexValidationTests.test_expert_signature_forged) ... ok
test_explicit_empty_diagnostic (test_validate_index.IndexValidationTests.test_explicit_empty_diagnostic) ... ok
test_holdout_candidate (test_validate_index.IndexValidationTests.test_holdout_candidate) ... ok
test_holdout_split (test_validate_index.IndexValidationTests.test_holdout_split) ... ok
test_illegal_json_cli_redacted (test_validate_index.IndexValidationTests.test_illegal_json_cli_redacted) ... ok
test_invalid_date (test_validate_index.IndexValidationTests.test_invalid_date) ... ok
test_malformed_url_does_not_crash (test_validate_index.IndexValidationTests.test_malformed_url_does_not_crash) ... ok
test_missing_law_time (test_validate_index.IndexValidationTests.test_missing_law_time) ... ok
test_missing_registry_source (test_validate_index.IndexValidationTests.test_missing_registry_source) ... ok
test_missing_source (test_validate_index.IndexValidationTests.test_missing_source) ... ok
test_model_rights_missing_evidence (test_validate_index.IndexValidationTests.test_model_rights_missing_evidence) ... ok
test_nested_body_rejected (test_validate_index.IndexValidationTests.test_nested_body_rejected) ... ok
test_official_recalled_mislabeled (test_validate_index.IndexValidationTests.test_official_recalled_mislabeled) ... ok
test_official_url_recalled_label (test_validate_index.IndexValidationTests.test_official_url_recalled_label) ... ok
test_public_holdout_path (test_validate_index.IndexValidationTests.test_public_holdout_path) ... ok
test_public_pdf (test_validate_index.IndexValidationTests.test_public_pdf) ... ok
test_rights_forged_status (test_validate_index.IndexValidationTests.test_rights_forged_status) ... ok
test_rights_url_is_not_a_grant (test_validate_index.IndexValidationTests.test_rights_url_is_not_a_grant) ... ok
test_source_body_rejected (test_validate_index.IndexValidationTests.test_source_body_rejected) ... ok
test_source_rights_forgery (test_validate_index.IndexValidationTests.test_source_rights_forgery) ... ok
test_source_synthetic_fixture_valid (test_validate_index.IndexValidationTests.test_source_synthetic_fixture_valid) ... ok
test_synthetic_not_counted_in_production (test_validate_index.IndexValidationTests.test_synthetic_not_counted_in_production) ... ok
test_synthetic_valid (test_validate_index.IndexValidationTests.test_synthetic_valid) ... ok
test_unknown_category (test_validate_index.IndexValidationTests.test_unknown_category) ... ok
test_unregistered_public_data (test_validate_index.IndexValidationTests.test_unregistered_public_data) ... ok

----------------------------------------------------------------------
Ran 40 tests in 0.104s

OK
exit_code=0
```

## Limits and review

No real question or answer content, model calls, professional legal review,
semantic duplicate detection or licensed data usability was tested. Official
source contents and question locators could not be verified. File/schema guards
are not comprehensive secret/content detection. Manual staged diff and file-list
review is required before push. CI links and exact head SHA are supplied in the
Draft PR and final handoff to avoid self-referential commit identifiers here.

## Human decisions / outstanding evidence

1. Maintainer: approve a code license separately (none is granted by this PR).
2. Maintainer/reviewer: arrange verifiable official source access and review
   source/body rights evidence; until then pilot remains 0/30 and body/model
   processing is BLOCKED_BY_RIGHTS. Do not authorize copying by assumption.
3. Qualified legal experts: review historical keys, exam-date law and current-law
   applicability; LEGAL_REVIEW_PENDING. No expert signatures simulated.
4. ChatGPT engineering reviewer: assess this incomplete Gate 1 Draft PR and
   requested follow-up. Gate 2 remains stopped pending a separate explicit approval.
