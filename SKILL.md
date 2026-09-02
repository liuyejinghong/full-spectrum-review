---
name: full-spectrum-review
description: Comprehensive evidence-driven software audit. Reconstructs requirements from first principles, then reviews engineering correctness, business/domain logic, architecture, reliability, performance, simplification, maintainability, security, testing, and operations; verified findings are consolidated into a prioritized persistent audit report.
---

# Full-Spectrum Review

Use this Skill when the user asks for a comprehensive review, audit, health check, production-readiness assessment, codebase review, PR review, or repository review.

## Default behavior

**A normal invocation means a full audit.** Do not ask the user to choose review axes unless they explicitly request a narrow audit.

The audit must cover, as applicable to the target:

1. first-principles reconstruction and accidental complexity;
2. engineering correctness and contract propagation;
3. business/domain logic and invariants;
4. architecture, ownership, boundaries, and sources of truth;
5. failure handling, recovery, restart, idempotency, and concurrency;
6. data integrity, compatibility, configuration, migration, and external-system semantics;
7. performance, I/O, memory, resource use, scalability, and long-running stability;
8. simplification, redundancy removal, dead code, over-engineering, and dependency/configuration bloat;
9. tests, observability, operability, deployment, rollback, and maintenance risk;
10. security and trust boundaries where real untrusted inputs or privileges exist;
11. domain-specific risks from an applicable domain pack.

The files under `references/` are review lenses, not separate products. Load and use all relevant lenses during a full audit:

- `references/first-principles-review.md`
- `references/engineering-review.md`
- `references/business-logic-review.md`
- `references/optimization-review.md`
- `references/finding-protocol.md`
- `references/reporting-protocol.md`

For trading or real-money systems also read `references/trading-domain.md`.

## First-principles rule

Do not accept the current architecture as the definition of the problem.

Before deeply evaluating an important subsystem's implementation, independently reconstruct:

1. the required externally meaningful outcome;
2. the real irreducible constraints;
3. the invariants any valid implementation must preserve;
4. the minimum sufficient conceptual mechanism.

Then compare that model with the current implementation.

Challenge every additional state, owner, worker, queue, cache, retry, fallback, watchdog, wrapper, abstraction, compatibility layer, and configuration branch by asking what **current independent requirement** it satisfies.

If the same current requirements could be satisfied by a materially simpler mechanism, and the extra layers carry no independent requirement while adding state space, synchronization, recovery paths, operational burden, resource cost, or maintenance risk, treat that difference as candidate **accidental complexity** even if no current bug is reproduced.

This is not a mandate for minimum line count. Real business, concurrency, failure, compatibility, and performance constraints may require substantial complexity. Do not remove a layer unless its responsibility is either unnecessary or safely transferred while all required behavior and invariants remain preserved.

Read and follow `references/first-principles-review.md`.

## Audit objective

The goal is not to produce many comments. The goal is to produce a **decision-useful, prioritized technical audit artifact** that tells maintainers:

- what is actually wrong or materially weak;
- where the design is more complex than the requirements justify;
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
4. perform first-principles reconstruction of important subsystems **before accepting their existing architecture as necessary**;
5. map the actual architecture and execution/data paths, then compare them with the minimum sufficient mechanisms;
6. inspect the implementation and enough surrounding code to understand callers, callees, persistence, external APIs, configuration, tests, and failure boundaries;
7. run all remaining applicable audit lenses;
8. generate candidate findings with high recall, including accidental-complexity candidates;
9. verify every publishable finding using `references/finding-protocol.md`;
10. deduplicate by root cause and rank by priority;
11. produce and persist the audit report using `references/reporting-protocol.md`.

## Comprehensive scope

For a repository audit, review the system broadly enough to form a reliable view of its architecture and critical behavior. Prioritize high-value execution paths, stateful subsystems, external boundaries, production/runtime paths, and business-critical flows; do not waste effort enumerating trivial style issues.

For a PR or commit audit, the change is the primary scope, but changed lines are only the starting point. Follow affected contracts and behavior into unchanged callers, callees, state, tests, and external interfaces when required to judge the change correctly.

## Independence of reasoning

First Principles, Engineering, Business Logic, and Optimization/Simplification are distinct reasoning lenses. During candidate generation, avoid letting a tentative conclusion from one lens prematurely close another line of inquiry.

In particular, do not let the existence of passing tests or a bug-free implementation prove that the design itself is justified. A function can behave correctly while solving the problem through unnecessary machinery.

After candidate generation, combine all lenses into one root-cause-oriented result. The user should receive **one coherent audit**, not disconnected mini-reviews.

## Exact-revision discipline

When reviewing a PR or moving branch and the platform exposes commit SHAs, bind the audit to the exact reviewed revision.

If the user supplied an expected head and the current head differs, report revision drift rather than silently applying an old conclusion to new code.

Recheck the current head immediately before a terminal PR verdict.

## Anti-noise rules

Do not report:

- style preferences without meaningful correctness, maintenance, or efficiency impact;
- "over-engineered" judgments that cannot identify a simpler sufficient mechanism and preserved invariants;
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
- `P1 — High`: realistic major correctness, business, state, recovery, security, performance, or production failure; may also include accidental complexity that materially obscures ownership/safety in a core production path.
- `P2 — Medium`: real defect, significant weakness, meaningful optimization, or material accidental complexity that increases state space, failure surface, operational burden, or maintenance risk.
- `P3 — Low`: concrete non-blocking improvement with limited impact.

Do not inflate priority. Optional cleanup or aesthetic simplification should not become P0/P1/P2.

## Terminal result

For PR merge decisions, use one of:

- `APPROVE`
- `APPROVE_WITH_NON_BLOCKING_FINDINGS`
- `REQUEST_CHANGES`
- `HEAD_DRIFT`
- `INSUFFICIENT_EVIDENCE`

For repository-wide audits, give an overall health/risk assessment rather than forcing a merge verdict.

The audit is successful when a maintainer can read the report from top to bottom and immediately know **what to fix first, why, what can be removed, and what evidence supports that priority**.
