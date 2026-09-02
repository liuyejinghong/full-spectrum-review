---
name: full-spectrum-review
description: Independent multi-axis review for pull requests, commits, branches, or repository changes. Separates engineering correctness, business/domain logic, and optimization/simplification so each axis can reason independently before findings are verified and combined.
---

# Full-Spectrum Review

Use this Skill when the user wants an independent, evidence-driven review of a PR, commit range, branch, or repository change.

The core rule is simple: **do not collapse every kind of review into one giant checklist.** Run independent review axes, then verify and deduplicate findings.

## Review axes

Choose one or more axes based on the request:

1. **Engineering Review** — correctness, reliability, concurrency, security, integration, data integrity, tests, compatibility, operations.
2. **Business Logic Audit** — business intent, domain rules, invariants, lifecycles, temporal semantics, economics/accounting, external-reality mapping, cross-feature behavior.
3. **Optimization & Simplification Review** — remove unnecessary code/state/abstractions, reduce runtime cost and failure surface, improve performance and long-running stability while preserving behavior.

Read the matching reference file before performing that axis:

- `references/engineering-review.md`
- `references/business-logic-review.md`
- `references/optimization-review.md`

Always read `references/finding-protocol.md` before publishing findings.

For trading or real-money systems, also read `references/trading-domain.md` when relevant.

## Independence rule

When multiple axes are requested, reason about them independently before cross-reading conclusions.

Do not let an Engineering finding anchor the Business reviewer, or a Business finding anchor the Optimization reviewer. Generate candidate findings separately, then verify them together.

If subagents or independent workers are available, prefer one reviewer per axis. Otherwise run separate passes and avoid carrying tentative conclusions from one pass into the next.

## Evidence order

Before judging implementation:

1. Identify the exact review target.
2. Read the Issue/specification/PR description and repository instructions.
3. Reconstruct intended behavior and critical invariants.
4. Read the complete relevant diff and enough surrounding code to understand contracts and ownership.
5. Follow changed behavior across callers, callees, persisted state, configuration, external APIs, and tests where necessary.
6. Run the selected review axes.
7. Verify candidate findings using `finding-protocol.md`.
8. Deduplicate by root cause.
9. Recheck the exact head before a terminal verdict when reviewing a moving PR.

## Exact-head rule

For PR review, bind the result to a concrete commit SHA whenever the platform exposes it.

If the user supplied an expected head and the current head differs, stop that review target and report head drift instead of silently reviewing the newer commit.

Before publishing a terminal verdict, re-read the current PR head. Do not attach an old verdict to a new head.

Multiple PRs are independent review transactions: drift or failure in one must not block completion of the others.

## Scope rule

Changed lines are the starting point, not the full reasoning boundary.

Read unchanged code when the change alters its assumptions, relies on it, exposes a latent defect through a newly reachable path, or modifies a caller/callee contract.

Do not turn the review into a repository-wide historical-tech-debt hunt.

## Anti-noise rule

High recall is useful during candidate generation; high precision is mandatory when publishing findings.

Do not report:

- style preferences without correctness or maintenance impact;
- hypothetical edge cases unreachable through supported product behavior;
- speculative security hardening without a real trust boundary or attack path;
- micro-optimizations without a meaningful workload;
- new wrappers, compatibility layers, feature flags, migration scaffolding, checksums, or defensive machinery unless a real current requirement justifies them;
- unrelated historical debt.

## Terminal verdicts

Use a small, explicit verdict set when the user asks for a merge decision:

- `APPROVE`
- `APPROVE_WITH_NON_BLOCKING_FINDINGS`
- `REQUEST_CHANGES`
- `HEAD_DRIFT`
- `INSUFFICIENT_EVIDENCE`

One verified blocking correctness or business-semantic defect is enough for `REQUEST_CHANGES`.

## Output

Keep the final summary compact. Put durable detail in the code review surface when the user authorized repository writes.

Recommended summary:

```text
Review target: <PR / range>
Reviewed base: <sha>
Reviewed head: <sha>
Axes: Engineering / Business Logic / Optimization
Verdict: <verdict>
Findings: P0=x P1=x P2=x P3=x
```

Then list finding titles and the evidence/tests reviewed.

The value of this Skill is not the number of comments. The value is finding real defects, semantic mismatches, and removable complexity before they become production incidents.
