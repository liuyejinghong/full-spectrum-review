# Audit Reporting Protocol

A full-spectrum audit must end in one consolidated, persistent report. The report is the canonical artifact; chat summaries and inline comments are secondary surfaces.

## Core rule

**Sort by priority, then by root-cause importance.** Do not organize the main findings by file order, reviewer lens, or discovery sequence.

First Principles, Engineering, Business Logic, and Optimization are dimensions used to discover and classify findings. They are not separate final reports unless the user explicitly requests that format.

A correct-but-unnecessarily-complex design can be a real audit finding. Do not bury verified accidental complexity in an informal "nice to have" section merely because no current bug is reproduced.

## Recommended report structure

```markdown
# Full-Spectrum Review Report

## 1. Audit Metadata
- Repository / target
- Reviewed revision / base / head
- Date
- Audit scope
- Evidence available
- Important evidence limitations

## 2. Executive Summary
- Overall assessment
- Highest-risk themes
- Whether production/merge should be blocked
- Total findings by priority
- Most important first-principles/simplification/performance opportunities

## 3. Priority Overview
| Priority | Count | Meaning |
|---|---:|---|
| P0 | ... | ... |
| P1 | ... | ... |
| P2 | ... | ... |
| P3 | ... | ... |

## 4. Recommended Execution Order
1. Fix the first root cause...
2. Then address...
3. Then simplify/optimize...

## 5. Findings — P0 Critical
...

## 6. Findings — P1 High
...

## 7. Findings — P2 Medium
...

## 8. Findings — P3 Low
...

## 9. Positive Findings / Keep As-Is
- Sound architecture or invariant worth preserving
- Existing mechanism that should not be replaced without evidence

## 10. Test / Verification Gaps
- Important behavior not proven by current evidence

## 11. Appendix
- Commands/tests/benchmarks inspected or executed
- Architecture/business-rule/first-principles notes when useful
```

Skip empty priority sections, but never hide the fact that no findings exist at a priority.

## Priority overview

At the top of the report, include a compact table listing each finding in final priority order:

```markdown
| ID | Priority | Type | Area | Finding | Impact |
|---|---|---|---|---|---|
| FSR-001 | P0 | Defect | Business / Trading | ... | ... |
| FSR-002 | P1 | Reliability | Execution | ... | ... |
| FSR-003 | P2 | Accidental Complexity | Architecture | ... | ... |
```

Use stable IDs (`FSR-001`, `FSR-002`, ...). IDs follow final priority order, not discovery order.

## Finding types

Use one of these when useful:

- `Defect` — implementation or behavior is wrong;
- `Business` — domain/business semantics are wrong or incomplete;
- `Reliability` — failure/recovery/concurrency/state behavior is unsafe;
- `Performance` — real workload/resource inefficiency with meaningful impact;
- `Accidental Complexity` — current requirements can be satisfied by a materially simpler sufficient mechanism and the extra layers carry no independent current requirement while increasing state/failure/maintenance/operational cost;
- `Optimization` — current behavior is correct but materially more costly than necessary;
- `Maintainability` — concrete entropy or ownership problem likely to cause future defects;
- `Security` — real trust-boundary or privilege defect;
- `Test Gap` — important behavior is materially unproven.

A finding may include multiple area tags, but keep one primary type.

## Detailed finding format

Each detailed finding should normally contain:

```markdown
### FSR-00X — [P?] Short title

**Type:** Defect / Business / Reliability / Performance / Accidental Complexity / Optimization / ...
**Area:** module / business flow / subsystem
**Evidence:** `path:line`, tests, contract, benchmark, external semantics

**Problem / Opportunity**
What is wrong or unnecessarily complex/expensive.

**Trigger / Workload**
The realistic scenario or workload that exposes it.

**Mechanism**
Why the current system produces the result.

**Impact**
What actually happens and why the assigned priority is justified.

**Recommended direction**
The smallest sensible correction or simplification direction. Do not write a full implementation unless requested.

**Verification**
What test, scenario, measurement, or invariant should prove the fix safe.
```

For First-Principles / Accidental-Complexity findings, use the stronger shape below when it improves clarity:

```markdown
**Required outcome**
What the subsystem actually must accomplish.

**Irreducible constraints / invariants**
What a valid solution cannot violate.

**Minimum sufficient mechanism**
The smallest conceptual mechanism that satisfies those requirements.

**Current mechanism**
The actual states, owners, workers, caches, retries, wrappers, or recovery layers.

**Accidental complexity delta**
Which extra layers do not carry an independent current requirement and what cost they create.

**Simplification direction**
What responsibility boundary/state model can be removed or consolidated.

**Behavior-preservation plan**
How to prove the simplified mechanism preserves all required semantics.
```

Do not use this type merely because code looks verbose. The report must demonstrate the simpler sufficient mechanism and preserved responsibilities.

## Recommended execution order

Priority alone is not always sufficient. Dependencies between fixes matter.

After ranking findings, produce a recommended remediation sequence that considers:

1. stop-the-bleeding production/real-money risk;
2. first-principles/root-cause corrections that invalidate multiple downstream patches;
3. authoritative state/ownership corrections;
4. correctness and recovery defects;
5. performance/stability bottlenecks;
6. simplification and entropy reduction;
7. lower-impact cleanup.

If one ownership or architectural correction makes several lower-priority findings disappear, say so explicitly rather than recommending independent patches.

## Positive findings

A comprehensive audit should also identify a small number of important things that are already sound when evidence supports it. This helps prevent later agents from "optimizing" away valuable invariants or architecture.

Do not add praise for politeness. Include only design choices worth preserving.

## Persistence rules

When the audited repository is writable and the user authorized writes:

1. follow an existing repository convention for audit/review docs if present;
2. otherwise create `docs/reviews/`;
3. persist the complete report as Markdown;
4. include the exact revision(s) reviewed;
5. do not overwrite an older audit for a different revision;
6. use a new report or clearly marked re-review section for a new head;
7. keep inline PR comments concise and point to the canonical report when appropriate.

Default filenames:

```text
docs/reviews/<YYYY-MM-DD>-full-spectrum-review.md
docs/reviews/pr-<number>-<short-head>-full-spectrum-review.md
```

If writes are not available, provide the report in full and state that persistence could not be performed.

## Completeness check before finalizing

Before declaring the audit complete, verify:

- first-principles reconstruction was performed for important subsystems rather than assuming the current architecture is necessary;
- all other applicable review lenses were exercised;
- high-risk architecture/business flows were traced end-to-end;
- accidental-complexity findings demonstrate a simpler sufficient mechanism and preserved invariants;
- findings were verified and deduplicated;
- priority reflects impact rather than reviewer confidence;
- findings are ordered P0 → P1 → P2 → P3;
- remediation dependencies are reflected in execution order;
- important evidence gaps are explicit;
- the report is saved or returned as a complete reusable artifact.
