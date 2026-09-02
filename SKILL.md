---
name: full-spectrum-review
description: Comprehensive evidence-driven software audit. Reviews engineering correctness, business/domain logic, architecture, reliability, performance, simplification, maintainability, security, testing, and operations; then consolidates verified findings into a prioritized persistent audit report.
---

# Full-Spectrum Review

Use this Skill when the user asks for a comprehensive review, audit, health check, production-readiness assessment, codebase review, PR review, or repository review.

## Default behavior

**A normal invocation means a full audit.** Do not ask the user to choose review axes unless they explicitly request a narrow audit.

The audit must cover, as applicable to the target:

1. engineering correctness and contract propagation;
2. business/domain logic and invariants;
3. architecture, ownership, boundaries, and sources of truth;
4. failure handling, recovery, restart, idempotency, and concurrency;
5. data integrity, compatibility, configuration, migration, and external-system semantics;
6. performance, I/O, memory, resource use, scalability, and long-running stability;
7. simplification, redundancy removal, dead code, over-engineering, and dependency/configuration bloat;
8. tests, observability, operability, deployment, rollback, and maintenance risk;
9. security and trust boundaries where real untrusted inputs or privileges exist;
10. domain-specific risks from an applicable domain pack.

The files under `references/` are review lenses, not separate products. Load and use all relevant lenses during a full audit:

- `references/engineering-review.md`
- `references/business-logic-review.md`
- `references/optimization-review.md`
- `references/finding-protocol.md`
- `references/reporting-protocol.md`

For trading or real-money systems also read `references/trading-domain.md`.

## Audit objective

The goal is not to produce many comments. The goal is to produce a **decision-useful, prioritized technical audit artifact** that tells maintainers:

- what is actually wrong or materially weak;
- why it matters;
- what evidence proves it;
- what should be fixed first;
- what can be simplified or removed;
- what is already sound and should not be churned;
- what remains uncertain because evidence is missing.

## Evidence order

Before judging implementation:

1. identify the exact review target and available source revision;
2. read repository instructions, README, architecture docs, specifications, Issues/PR descriptions, ADRs, configuration, and relevant operational docs;
3. reconstruct the system's purpose, major flows, domain entities, ownership, authoritative state, and critical invariants;
4. map the relevant architecture and execution/data paths;
5. inspect the implementation and enough surrounding code to understand callers, callees, persistence, external APIs, configuration, tests, and failure boundaries;
6. run all applicable audit lenses;
7. generate candidate findings with high recall;
8. verify every publishable finding using `references/finding-protocol.md`;
9. deduplicate by root cause and rank by priority;
10. produce and persist the audit report using `references/reporting-protocol.md`.

## Comprehensive scope

For a repository audit, review the system broadly enough to form a reliable view of its architecture and critical behavior. Prioritize high-value execution paths, stateful subsystems, external boundaries, production/runtime paths, and business-critical flows; do not waste effort enumerating trivial style issues.

For a PR or commit audit, the change is the primary scope, but changed lines are only the starting point. Follow affected contracts and behavior into unchanged callers, callees, state, tests, and external interfaces when required to judge the change correctly.

## Independence of reasoning

Engineering, Business Logic, and Optimization/Simplification are distinct reasoning lenses. During candidate generation, avoid letting a tentative conclusion from one lens prematurely close another line of inquiry.

After candidate generation, combine all lenses into one root-cause-oriented result. The user should receive **one coherent audit**, not three disconnected mini-reviews.

## Exact-revision discipline

When reviewing a PR or moving branch and the platform exposes commit SHAs, bind the audit to the exact reviewed revision.

If the user supplied an expected head and the current head differs, report revision drift rather than silently applying an old conclusion to new code.

Recheck the current head immediately before a terminal PR verdict.

## Anti-noise rules

Do not report:

- style preferences without meaningful correctness, maintenance, or efficiency impact;
- hypothetical edge cases unreachable through supported behavior;
- speculative security hardening without a real trust boundary or attack path;
- micro-optimizations without a plausible meaningful workload;
- additional wrappers, feature flags, compatibility layers, migration frameworks, checksums, or defensive machinery without a real current requirement;
- unrelated historical debt that does not materially affect the audited system or change;
- duplicate symptoms of one root cause as separate findings.

High recall is desirable while exploring. High precision is mandatory in the final report.

## Required deliverable

A full audit is incomplete until a consolidated report is produced.

If repository writes are available and authorized, persist the report in the audited repository. Follow an existing audit/review-doc convention if one exists. Otherwise default to:

```text
docs/reviews/<YYYY-MM-DD>-full-spectrum-review.md
```

For a specific PR or revision, prefer a stable target-aware name such as:

```text
docs/reviews/pr-<number>-<short-head>-full-spectrum-review.md
```

If repository writes are unavailable, return the complete report to the user so it can be saved unchanged.

The report must be sorted by priority, not by discovery order or file order. Read and follow `references/reporting-protocol.md`.

## Priority model

Use:

- `P0 — Critical`: catastrophic loss/corruption, systemic compromise, or unrecoverable production state.
- `P1 — High`: realistic major correctness, business, state, recovery, security, performance, or production failure.
- `P2 — Medium`: real defect, significant weakness, meaningful optimization, or maintainability/stability issue with moderate impact.
- `P3 — Low`: concrete non-blocking improvement with limited impact.

Do not inflate priority. Optional cleanup should not become P0/P1 merely because it is aesthetically desirable.

## Terminal result

For PR merge decisions, use one of:

- `APPROVE`
- `APPROVE_WITH_NON_BLOCKING_FINDINGS`
- `REQUEST_CHANGES`
- `HEAD_DRIFT`
- `INSUFFICIENT_EVIDENCE`

For repository-wide audits, give an overall health/risk assessment rather than forcing a merge verdict.

The audit is successful when a maintainer can read the report from top to bottom and immediately know **what to fix first, why, and what evidence supports that priority**.
