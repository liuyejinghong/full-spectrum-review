# Finding Verification Protocol

Use this protocol after candidate generation and before publishing findings.

The goal is high recall during exploration and high precision in durable review output.

## Verification questions

Every candidate finding must answer all of the following:

### Trigger

What real input, state, workload, failure, execution ordering, maintenance action, recovery scenario, or supported evolution exposes the problem or cost?

For First-Principles / Accidental-Complexity findings, the trigger does not need to be an already-reproduced runtime bug. It may be the current maintenance/state-space/recovery burden itself, but the reviewer must identify a concrete mechanism and cost rather than a subjective preference.

### Mechanism

Why does the implementation produce the incorrect, unsafe, wasteful, or overly complex behavior?

For accidental complexity, explain which current layers do not carry independent requirements and why the same required behavior can be achieved by a materially simpler sufficient mechanism.

### Impact

What concrete consequence follows?

Valid impact includes correctness or safety failure, but can also include measurable or structurally demonstrated state-space growth, synchronization burden, additional recovery paths, operational complexity, resource cost, test-matrix expansion, or elevated maintenance/change risk.

### Reachability

Can the supported product or operating environment actually reach the scenario or incur the stated cost?

Reachable edge cases count. Merely constructible theoretical states do not.

For structural complexity findings, the current code path and maintenance/recovery burden are already reachable if they are part of supported production behavior; do not invent hypothetical future scale or consumers to justify the finding.

### Scope

Why is the issue relevant to the reviewed target?

For a PR/commit, acceptable scope relationships include:

- introduced by the change;
- exposed by a newly reachable path;
- relied upon by the change;
- required to be updated because a contract changed.

For repository-wide audits, high-value existing architectural or complexity problems are in scope when they materially affect current supported behavior, operations, or maintainability.

### Evidence

Point to concrete code, diff, tests, documentation, external contract, architecture/state mapping, benchmark, or measured behavior.

For an accidental-complexity finding, evidence must support both sides of the comparison:

1. the actual responsibilities/constraints that must be preserved; and
2. the extra current layers claimed to be unnecessary or consolidatable.

If these cannot be answered, downgrade the candidate to an observation or discard it.

## Root-cause deduplication

Group symptoms that share one root cause into one finding. Do not inflate counts by reporting every manifestation separately.

Conversely, do not merge unrelated root causes just because they occur in the same file.

If one incorrect ownership or state model created several guards, retries, caches, and cleanup paths, prefer one root-cause finding that explains which downstream layers become unnecessary after the root correction.

## Severity

Use severity to communicate impact, not reviewer confidence or whether a bug has already been observed.

- **P0 Critical** — catastrophic loss/corruption, systemic compromise, or unrecoverable production state.
- **P1 High** — realistic major correctness, money/state, recovery, security, performance, or production risk; may include accidental complexity that materially obscures ownership/safety on a core path.
- **P2 Medium** — real defect/regression, meaningful requirement violation, or material accidental complexity that significantly increases state/failure/operational/maintenance cost.
- **P3 Low** — non-blocking but concrete maintainability, robustness, efficiency, operability, or bounded simplification issue.

Do not manufacture P3 findings to make a review look busy, and do not inflate aesthetic cleanup into P1/P2.

## Finding format

```text
[P?] Short imperative title
path/to/file:line

Problem / Opportunity
What is wrong or unnecessarily complex.

Trigger / Workload
The real scenario or supported burden that exposes it.

Mechanism
Why the implementation behaves this way.

Impact
The concrete consequence.

Evidence
Code/test/contract/architecture evidence.

Minimal fix / simplification direction
The smallest reasonable correction direction, not a full implementation.

Regression test / measurement / invariant proof
What should prove the fix or simplification safe.
```

For First-Principles / Accidental-Complexity findings, also establish:

```text
Required outcome
Irreducible constraints / invariants
Minimum sufficient mechanism
Current mechanism
Accidental complexity delta
Responsibility transfer
Behavior-preservation plan
```

Do not publish "this feels over-engineered" without that proof.

## Confidence discipline

Do not use vague language such as "might be problematic" as a substitute for mechanism.

When evidence is incomplete, explicitly say what is known and what remains unproven. Use `INSUFFICIENT_EVIDENCE` when a terminal verdict cannot responsibly be made.

## Tests and measurements

Passing tests support a conclusion but do not prove correctness, business validity, or architectural necessity. Failed tests are evidence only after confirming the failure is relevant.

For performance findings, prefer an asymptotic argument, profile, benchmark, resource-growth observation, or a clearly repeated expensive operation. Do not fabricate benchmark numbers.

For simplification findings, prefer a responsibility/invariant proof over line-count claims.

## Repository persistence

When the user explicitly authorizes repository writes:

- put line-local findings in inline review comments when an accurate diff position is available;
- put cross-file/system findings in the review body or canonical report;
- bind the review to the exact commit when the platform supports it;
- recheck PR head immediately before submitting a terminal verdict;
- if head drifted, do not apply the old verdict to the new head.

Keep the chat summary shorter than the durable review.
