# Audit Reporting Protocol

A full-spectrum audit ends in one coherent, persistent audit artifact. Chat summaries and inline review comments are secondary surfaces.

This file owns report structure, coverage accounting, audit-ledger lifecycle, re-review behavior, and persistence. Finding priority/type/confidence/status/schema are owned by `finding-protocol.md`.

## Core rule

Sort active findings by **priority, then root-cause importance**, not file order, lens, discovery sequence, or ID.

The report must make a crucial distinction visible:

> **No finding found** is not the same as **not reviewed**.

## Read prior audit state first

Before a re-review, inspect the target repository's existing audit index and relevant prior reports when available.

Carry forward:

- stable finding IDs and statuses;
- unresolved/root-cause relationships;
- prior Keep-As-Is decisions;
- Open Questions that remain unresolved;
- the last reviewed revision and relevant evidence limitations.

Do not silently assign new IDs to old root causes.

## Coverage Ledger

Every audit must contain a Coverage Ledger derived from the audit plan.

Recommended fields:

```markdown
| Area / Flow | Depth | Status | Evidence / Notes |
|---|---|---|---|
| Order execution | deep | COMPLETE | traced submit → reconcile → position |
| Reporting UI | sampled | PARTIAL | sampled API boundary only |
| Legacy migration | none | NOT_COVERED | outside requested target |
| External contract X | deep | INSUFFICIENT_EVIDENCE | contract unavailable |
```

Suggested depth values:

- `deep` — end-to-end or sufficiently detailed inspection for a reliable conclusion;
- `sampled` — representative inspection, not exhaustive;
- `none` — intentionally not inspected.

Coverage status:

- `COMPLETE` — planned depth achieved with sufficient evidence;
- `PARTIAL` — some planned evidence/path remains unreviewed;
- `NOT_COVERED` — explicitly outside achieved audit coverage;
- `INSUFFICIENT_EVIDENCE` — inspected, but available evidence cannot support a responsible conclusion.

Use plain equivalents if the target repository prefers different terminology, but preserve the distinction.

A full audit means all materially relevant areas are represented in the ledger. It does not require identical depth everywhere.

## Proportional reporting

The canonical artifact scales with the target.

- A narrow PR may use a compact report with a short Coverage Ledger and concise P2/P3 findings.
- A repository-wide audit may require extensive architecture/business evidence and a broader ledger.

Do not drop evidence discipline because the report is short, and do not force a 30-line PR into a multi-thousand-word template when concise evidence is sufficient.

## Recommended report structure

```markdown
# Full-Spectrum Review Report

## 1. Audit Metadata
- Repository / target
- Reviewed revision / base / head
- Audit date
- Skill version/revision if known
- Loaded Domain Packs + versions
- Prior audit/index consulted
- Important evidence limitations

## 2. Coverage Ledger
| Area / Flow | Depth | Status | Evidence / Notes |
|---|---|---|---|

## 3. Executive Summary
- Overall assessment
- Highest-risk/root-cause themes
- Whether merge/production should be blocked when applicable
- Active findings by priority
- Most important simplification/performance opportunities

## 4. Priority Overview
| ID | Priority | Confidence | Status | Type | Area | Finding | Impact |
|---|---|---|---|---|---|---|---|

## 5. Recommended Execution Order
1. Fix the root cause that invalidates downstream work...
2. Then address...

## 6+. Findings — P0 → P1 → P2 → P3
...

## Open Questions for the Maintainer
- Material intent/contract questions that cannot responsibly be turned into findings

## Positive Findings / Keep As-Is
- Important proven invariants/design choices worth preserving

## Evidence / Verification Gaps
- Important uncertainty that cannot responsibly be assigned a finding priority

## Appendix
- Commands/tests/benchmarks/contracts/history inspected when useful
```

Skip empty detailed priority sections if doing so improves signal, but the Priority Overview or Executive Summary must make zero counts clear.

Use the canonical finding schema and prose depth rules from `finding-protocol.md` instead of redefining another schema here.

## Recommended Execution Order

Priority alone is insufficient when fixes depend on each other.

Order remediation by:

1. immediate production/real-money safety;
2. root causes that invalidate downstream fixes;
3. authoritative state/ownership corrections;
4. correctness/business/recovery defects;
5. performance/stability bottlenecks;
6. accidental-complexity and entropy reduction;
7. lower-impact cleanup.

If one architectural correction makes several findings disappear, say so explicitly. Existing downstream IDs remain in the audit ledger and may become `SUPERSEDED` after verification.

## Audit index: persistent finding ledger

When persistence is authorized and the repository has no equivalent convention, maintain:

```text
docs/reviews/INDEX.md
```

Keep it deliberately small. Recommended columns:

```markdown
| ID | Title | First Seen | Current Priority | Status | Latest Audit |
|---|---|---|---|---|---|
```

The index is not an issue tracker. Do not add assignees, dates, milestones, labels, or workflow machinery unless the repository already uses them and the user requests integration.

### ID lifecycle

- allocate each new root cause a new monotonic ID;
- never renumber because sorting/priority changes;
- never reuse an old ID for a different problem;
- update status/priority/latest-audit on re-review;
- preserve historical reports for the exact revisions they audited.

## Re-review lifecycle

A new audit should classify prior findings before inventing replacements:

- still present → same ID remains `OPEN`;
- verified corrected → `FIXED`;
- consciously retained with rationale → `ACCEPTED`;
- replaced by a better root-cause finding → `SUPERSEDED` and link the successor;
- returned after being closed → `REOPENED`.

A finding's priority may change without changing its ID.

## Positive Findings / Keep As-Is persistence

Include only important choices supported by evidence, such as authoritative-state boundaries, invariants, or recovery semantics that later agents should not casually "simplify."

On re-review, read prior Keep-As-Is entries. If new evidence justifies overturning one, say so explicitly; otherwise treat it as a design constraint worth preserving.

Do not add praise for politeness.

## Open Questions vs findings

Use `Open Questions for the Maintainer` when required business/product intent cannot be established confidently enough for a finding.

An Open Question should state:

- what decision/intent is ambiguous;
- what evidence conflicts or is missing;
- which conclusions depend on the answer.

Do not assign P0–P3 merely to force uncertainty into the finding table.

## Persistence rules

When repository writes are available and the user authorized audit persistence:

1. follow an existing audit/review convention if the target already has one;
2. otherwise use `docs/reviews/` plus `docs/reviews/INDEX.md`;
3. write only audit artifacts — never implementation changes under audit authorization;
4. include exact reviewed revision(s);
5. do not overwrite a report for a different revision;
6. update the index after the report is finalized;
7. keep platform inline comments concise and secondary to the canonical report.

Default report filenames:

```text
docs/reviews/<YYYY-MM-DD>-full-spectrum-review.md
docs/reviews/pr-<number>-<short-head>-full-spectrum-review.md
```

If writes are unavailable, return the complete report and the index delta the maintainer would need to persist.

## Completion check

Before declaring the audit complete, verify facts rather than self-certifying a checklist:

- the Coverage Ledger represents every materially relevant planned area;
- `PARTIAL`, `NOT_COVERED`, and `INSUFFICIENT_EVIDENCE` are explicit rather than hidden behind "no finding";
- applicable Domain Packs and versions are recorded;
- prior stable IDs/statuses were reconciled on re-review;
- findings passed `finding-protocol.md` and were root-cause deduplicated;
- Recommended Execution Order reflects dependencies;
- unresolved business intent is in Open Questions;
- the report and index are persisted or returned as complete reusable artifacts.