# Audit Reporting Protocol

A full-spectrum audit ends in one coherent, persistent audit artifact. Chat summaries, worker packets, and inline review comments are secondary surfaces.

This file owns report structure, coverage accounting, audit-ledger lifecycle, re-review behavior, and persistence. Finding priority/type/confidence/status/schema are owned by `finding-protocol.md`. Audit-unit decomposition and worker behavior are owned by `orchestration-protocol.md`.

## Core rule

Sort active findings by **priority, then root-cause importance**, not file order, lens, discovery sequence, worker, or ID.

The report must make a crucial distinction visible:

> **No finding found** is not the same as **not reviewed**.

## Read prior audit state first

Before a re-review, inspect the workspace audit ledger for the target — `fsr-reports/<target>/INDEX.md` and the latest reports — and, when the audited repository carries its own committed audit convention, that too.

Carry forward:

- stable finding IDs and statuses;
- unresolved/root-cause relationships;
- prior Keep-As-Is decisions;
- Open Questions that remain unresolved;
- the last reviewed revision and relevant evidence limitations;
- prior Skill/Domain Pack versions when useful to explain changed conclusions.

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

For enumerable sets (see `orchestration-protocol.md`), the ledger row must name the member count and the source of truth, for example `gate keys 52/52, source: run_config producer`. A `sampled` depth can never support `COMPLETE` for such a set — mark `PARTIAL` with the uncovered members listed, or reach `deep` with full enumeration.

When orchestration uses multiple Audit Units, the Lead may add an `Audit Unit / Reviewer` column if it materially improves traceability. Do not expose vendor-specific worker IDs unless useful to the maintainer.

## Proportional reporting

The canonical artifact scales with the target.

- A narrow PR may use a compact report with a short Coverage Ledger and concise P2/P3 findings.
- A repository-wide audit may require extensive architecture/business evidence and a broader ledger.
- A parallel/distributed audit still produces one report; worker packets are evidence inputs, not separate final reports.

Do not drop evidence discipline because the report is short, and do not force a 30-line PR into a multi-thousand-word template when concise evidence is sufficient.

Sections 1–5 are the decision layer: a maintainer can approve, block, or order remediation from them alone. Sections 6+ are the repair layer. Keep the decision layer self-sufficient; never require reading every finding body to reach a verdict.

## Multi-wave convergence

A large target need not be covered in one session. An audit wave declares which Audit Units it covers; Units deferred to a later wave are `NOT_COVERED` with reason `deferred to next wave` — a planned state, not a failure. The ledger converges across waves: each wave binds its own revision, persists its own report under the same `<workspace>/fsr-reports/<target>/` root, and updates the same index. A full audit is the converged ledger, not a single heroic pass.

## Recommended report structure

```markdown
# Full-Spectrum Review Report

## 1. Audit Metadata
- Repository / target
- Reviewed revision / base / head
- Audit date
- Core Skill version from `VERSION` when available
- Core Skill revision when available
- Execution mode: single-unit / sequential-units / parallel-units
- Loaded Domain Packs + versions
- Domain Packs considered but rejected, with a one-line reason each
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
- Optional orchestration summary for multi-unit audits
```

Skip empty detailed priority sections if doing so improves signal, but the Priority Overview or Executive Summary must make zero counts clear.

Use the canonical finding schema and prose depth rules from `finding-protocol.md` instead of redefining another schema here.

## Skill / Domain Pack version traceability

A persisted report should record the Core Skill version from `VERSION` when that file is available in the installed Skill. If the harness exposes the Skill repository revision, record it as well.

This allows a re-review to distinguish:

```text
same target changed
vs
same target + audit protocol changed
```

Record each loaded Domain Pack's own version from its `DOMAIN.md` metadata. Domain Pack versions are independent from the Core Skill version.

Do not load `CHANGELOG.md` during ordinary audits merely to produce metadata. The current version is sufficient; consult changelog/history only when comparing audit-protocol behavior across versions.

## Orchestration traceability

For audits that used multiple logical Audit Units, record enough to understand coverage without dumping internal worker transcripts.

A compact appendix can state:

```markdown
### Audit Units
- Execution / order lifecycle — deep — COMPLETE
- Position / reconciliation — deep — COMPLETE
- Architecture / ownership cross-cut — deep — COMPLETE
- Web UI — sampled — PARTIAL
```

Do not persist raw worker scratch or concatenate Reviewer Packets into the report unless their contents are independently useful evidence.

The Lead remains accountable for the final report regardless of whether units ran in parallel or sequentially.

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

Every audited target has one working ledger in the auditor's workspace:

```text
<workspace>/fsr-reports/<target>/INDEX.md
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

When a previous finding changes because the Skill or Domain Pack protocol changed rather than the target changed, say so explicitly where material.

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

Audit artifacts live under a fixed root relative to the current workspace — the directory the audit session runs in:

```text
<workspace>/fsr-reports/<target>/INDEX.md
<workspace>/fsr-reports/<target>/INDEX.json
<workspace>/fsr-reports/<target>/<YYYY-MM-DD>-full-spectrum-review.md
<workspace>/fsr-reports/<target>/pr-<number>-<short-head>-full-spectrum-review.md
```

`INDEX.json` is the machine-readable source of truth — an array of `{id, title, firstSeen, priority, status, latestAudit}`. `INDEX.md` is rendered from it for human reading. Never hand-maintain the markdown table alone: a ledger edited in only one format drifts from the other.

`<target>` is the audited repository's name (`owner/name` when disambiguation is needed). All paths are workspace-relative: never absolute paths, OS-specific locations, or temp directories — behavior stays identical across harnesses and platforms.

1. write only audit artifacts — never implementation changes under audit authorization;
2. include exact reviewed revision(s);
3. include Core Skill and loaded Domain Pack versions when available;
4. do not overwrite a report for a different revision;
5. update INDEX.json after the report is finalized and re-render INDEX.md from it;
6. keep platform inline comments concise and secondary to the canonical report.

Publishing the audit into the audited repository is a separate, explicitly authorized export (read-only audit discipline): follow an existing audit/review convention there, otherwise `docs/reviews/`, and record the published location in the workspace INDEX rather than maintaining a second mutable ledger.

If the harness provides no writable workspace at all, return the complete report and the index delta the maintainer would need to persist.

## Completion check

Before declaring the audit complete, verify facts rather than self-certifying a checklist:

- the Coverage Ledger represents every materially relevant planned area/Audit Unit;
- `PARTIAL`, `NOT_COVERED`, and `INSUFFICIENT_EVIDENCE` are explicit rather than hidden behind "no finding";
- applicable Domain Packs and versions are recorded;
- Core Skill version/revision is recorded when available;
- prior stable IDs/statuses were reconciled on re-review;
- material cross-unit contradictions are resolved or explicitly left as insufficient evidence;
- findings passed `finding-protocol.md` and were root-cause deduplicated centrally;
- Recommended Execution Order reflects dependencies;
- unresolved business intent is in Open Questions;
- the report and index are persisted or returned as complete reusable artifacts.
