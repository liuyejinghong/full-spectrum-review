# Finding Verification Protocol

Use this protocol after candidate generation and before publishing findings.

The goal is high recall during exploration and high precision in durable review output.

## Verification questions

Every candidate finding must answer all of the following:

### Trigger

What real input, state, workload, failure, or execution ordering triggers the problem?

### Mechanism

Why does the implementation produce the incorrect, unsafe, wasteful, or overly complex behavior?

### Impact

What concrete consequence follows?

### Reachability

Can the supported product or operating environment actually reach the scenario?

Reachable edge cases count. Merely constructible theoretical states do not.

### Scope

Why is the issue relevant to the reviewed change?

Acceptable scope relationships include:

- introduced by the change;
- exposed by a newly reachable path;
- relied upon by the change;
- required to be updated because a contract changed.

### Evidence

Point to concrete code, diff, tests, documentation, external contract, or measured behavior.

If these cannot be answered, downgrade the candidate to an observation or discard it.

## Root-cause deduplication

Group symptoms that share one root cause into one finding. Do not inflate counts by reporting every manifestation separately.

Conversely, do not merge unrelated root causes just because they occur in the same file.

## Severity

Use severity to communicate impact, not reviewer confidence.

- **P0 Critical** — catastrophic loss/corruption, systemic compromise, or unrecoverable production state.
- **P1 High** — realistic major correctness, money/state, recovery, security, or production failure.
- **P2 Medium** — real defect/regression or meaningful requirement violation with smaller blast radius.
- **P3 Low** — non-blocking but concrete maintainability, robustness, efficiency, or operability issue.

Do not manufacture P3 findings to make a review look busy.

## Finding format

```text
[P?] Short imperative title
path/to/file:line

Problem
What is wrong.

Trigger
The real scenario that reaches it.

Mechanism
Why the implementation behaves this way.

Impact
The concrete consequence.

Evidence
Code/test/contract evidence.

Minimal fix direction
The smallest reasonable correction direction, not a full implementation.

Regression test / measurement
What should prove the fix or optimization safe.
```

For an Optimization recommendation, replace `Problem` with `Opportunity` when the current implementation is correct but unnecessarily costly or complex. Clearly distinguish defects from optional improvements.

## Confidence discipline

Do not use vague language such as "might be problematic" as a substitute for mechanism.

When evidence is incomplete, explicitly say what is known and what remains unproven. Use `INSUFFICIENT_EVIDENCE` when a terminal verdict cannot responsibly be made.

## Tests and measurements

Passing tests support a conclusion but do not prove correctness. Failed tests are evidence only after confirming the failure is relevant.

For performance findings, prefer an asymptotic argument, profile, benchmark, resource-growth observation, or a clearly repeated expensive operation. Do not fabricate benchmark numbers.

## Repository persistence

When the user explicitly authorizes repository writes:

- put line-local findings in inline review comments when an accurate diff position is available;
- put cross-file/system findings in the review body;
- bind the review to the exact commit when the platform supports it;
- recheck PR head immediately before submitting a terminal verdict;
- if head drifted, do not apply the old verdict to the new head.

Keep the chat summary shorter than the durable review.
