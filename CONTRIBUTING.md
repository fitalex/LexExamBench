# Contributing

Use feature branches and Draft PRs. Include provenance and rights evidence for every new metadata item. Do not contribute third-party question or answer bodies, private Holdout material, sensitive case data, API keys or simulated legal review results. Run `python scripts/validate_index.py` and `python -m unittest discover -s tests -v` before a PR.

Default validation fails until verified question locators exist. Use `--allow-empty` only for a clearly labeled engineering diagnostic. Review source and question schemas, staged diff and paths; do not echo invalid input in error reports. Real source access checks are manual and never run in CI.
