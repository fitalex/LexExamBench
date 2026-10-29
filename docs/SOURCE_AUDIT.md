# Gate 1 source audit — 2026-10-27

Status: **incomplete source verification; 0/30 question locators**. Task:
https://github.com/fitalex/LexRouter/issues/16 . This report distinguishes task
assertions from observations. No question bank, exam PDF, question text or answer
text was retained. Source records live in `data/sources/index.json` (the existing
repository path is preserved rather than introducing a second registry).

## Observed access evidence

| Registry ID | Exact original entry | Observed result | What remains unverified |
| --- | --- | --- | --- |
| moj-2017-paper1 | https://www.moj.gov.cn/pub/sfbgw/jgsz/jgszzsdw/zsdwgjsfkszx/gjsfkskskt/201805/t20180510_172369.html | urllib HTTPS request: HTTP 302 redirect loop | title, publication date, copyright notice, individual numbers, subjects/types |
| moj-2017-answer1 | https://www.moj.gov.cn/jgsz/jgszzsdw/zsdwgjsfkszx/gjsfkskskt/201709/t20170921_172374.html | HTTP 302 redirect loop | answer-key identity, scope, notice, correspondence with paper |
| moj-2026-notice | https://www.moj.gov.cn/jgsz/jgszzsdw/zsdwgjsfkszx/gjsfkszxdt/202606/t20260611_536377.html | HTTP 302 redirect loop | exact nonpublication rule and scope |
| jec-qa | https://github.com/thunlp/jec-qa | README HTTP 200; root LICENSE HTTP 404; root directory listing has no license file | underlying sources, per-item locators, dataset/compilation/answer/model grants |
| recalled-candidate | https://github.com/fitalex/LexRouter/issues/16 | source class required by task; no specific provider selected | publisher, year, subjects, provenance, permission; not a question source |

Additional official requests using `/pub/sfbgw/` for the answer and 2026 notice,
and the official `gjsfkskskt/` directory, also returned redirect loops. These are
access failures, not evidence that the documents do not exist. No anti-bot bypass
was attempted. No per-question source was successfully observed.

JEC-QA metadata revision: `8706c64ff62637e61cd8a729815f585a6df3b3f1`.
README describes an academic legal-domain QA dataset, points to
http://jecqa.thunlp.org/ and requests citation. The homepage and dataset were not
retrieved. Root metadata and README alone establish neither a dataset license
nor rights to underlying exams, compilations, answer data or external processing.
Absence of a root LICENSE is a limited observation, not proof no permission exists.

The task reports restrictive reprint notices for the 2017 paper/key and
nonpublication of 2026 questions/answers. **Those claims were not independently
reconfirmed in this run**. Do not describe recollections as official questions.

## Authorization matrix

All statuses concern original source bodies, not our independently written audit.
`pending` means no authorization established; `denied` would require evidence of
an applicable prohibition/refusal, so access failure alone is not marked denied.

| Source class | Individual indexing | Extract question | Extract answer | Internal body storage | Public redistribution | Third-party model |
| --- | --- | --- | --- | --- | --- | --- |
| MOJ 2017 paper / key | pending: locator not observed | pending | pending | pending | pending | pending |
| MOJ 2026 notice / exams | pending: no question locator | pending | pending | pending | pending | pending |
| JEC-QA | pending: no item inspected | pending | pending | pending | pending | pending |
| Recalled / training material | pending: provider unselected | pending | pending | pending | pending | pending |

Access and citation requests confer no copying rights. Indexing feasibility and
body-use rights are separate. Body collection and model processing remain
**BLOCKED_BY_RIGHTS**. No actual usable licensed question list exists yet.

## Pilot accounting and next evidence

| Target | Verified | Gap |
| --- | ---: | ---: |
| Objective (single/multiple/indefinite) | 0 | 24 |
| Subjective / case / essay | 0 | 6 |
| Total unique original positions | 0 | 30 |

No invented numbers, subject labels, keys or synthetic records enter the real
index. A source URL is insufficient to count a question. Recheck original paper
and key access, then record original paper and number, question type, subject,
exact URL, retrieval date and revision before counting. Subjective items require
a separately verified paper; no inferred paper-IV URL was fabricated.

Historical governing-law and current-law comparison: **LEGAL_REVIEW_PENDING**.
An expert must verify the original key and applicable exam-date law, then assess
changes as of 2026 separately. Codex has neither changed historical answers nor
signed any professional review.
