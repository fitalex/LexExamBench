# Security and content incidents

Do not include secrets, real cases, question/answer bodies, license correspondence,
or private Holdout material in issues, PRs, artifacts or logs. Report suspected
exposure privately to the repository maintainer using an established private
channel. No public reporting address is configured; do not invent one.

On suspected exposure: stop the affected push, isolate the local material, record
only affected paths/commit identifiers privately, and ask the maintainer to arrange
credential rotation or coordinated history/cache cleanup. Do not publish the
material again as evidence or independently rewrite shared history.

The validator is a structural guard, not a content classifier or legal clearance.
Review the complete staged diff and filenames before every push. CI is offline
apart from dependency setup; no paid API or model requests are allowed.
