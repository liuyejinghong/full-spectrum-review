# Finding Verification Protocol

This file is the **authoritative owner** of finding verification, types, priority, confidence, status, and canonical finding schema. Other files may reference these rules but should not redefine them.

Explore with high recall; publish with high precision.

## Verification bar

Every publishable finding must establish the following as applicable.

### Trigger / workload

What real input, state, workload, failure, ordering, maintenance action, recovery scenario, or supported evolution exposes the problem or cost?

Structural complexity does not need an already-reproduced runtime bug, but its current state-space, maintenance, recovery, or operational burden must be concrete rather than aesthetic.

### Mechanism

Why does the implementation or design produce the incorrect, unsafe, costly, or unnecessarily complex result?

### Impact

What concrete consequence follows? Valid impact includes correctness/business failure and also demonstrated state-space growth, synchronization/recovery burden, resource cost, operational complexity, test-matrix expansion, or elevated change risk.

### Reachability / incidence

Can the supported product/environment reach the scenario or incur the stated cost? Reachable edge cases count; merely constructible theoretical states do not.

State frequency as **measured** (field evidence, logs, queue lengths, latency samples) or **inferred** (code-path analysis only). A mechanism established code-only without any field/frequency measurement must say so explicitly; it must not borrow certainty from an unrelated passing test or from a different deployment's traffic.

### Scope

Why is the issue relevant to the audited target?

For PR/commit audits, valid relationships include introduced, exposed, relied upon, or required to change because a contract moved. For repository-wide audits, material current architectural/operational/maintenance problems are in scope even if old.

### Evidence

Point to concrete code, diff, tests, documentation, external contract, history, architecture/state mapping, profile, benchmark, or measured behavior.

If the bar cannot be met, record an observation, Open Question, or evidence gap instead of a finding.

## Disconfirmation for Accidental Complexity

Before publishing an `Accidental Complexity` finding, actively investigate why the challenged layer exists.

The finding must include:

```text
Why this layer exists / Disconfirmation attempt
- Evidence investigated: history / tests / ADRs / callers / operators / external constraints / other available sources
- Evidence found: current requirement that justifies the layer, or evidence that no current independent requirement was found
```

The reviewer does **not** need every evidence source and must not fabricate unavailable history. The requirement is a meaningful attempt to find contrary evidence.

No disconfirmation attempt → no Accidental Complexity finding. Keep it as an observation/hypothesis until investigated.

## Stated-rationale check for improvement-type findings

A finding that proposes new machinery — new tests, contracts, mechanisms, or fixtures — must first check available maintainer rationale in limitations, ADRs, and prior issue discussion about that proposal. If the same facts, consequences, and cost assumptions still hold, preserve the accepted tradeoff with its rationale instead of publishing the same demand as a fresh finding.

A rejected solution is not acceptance of every consequence of the underlying problem. New evidence, changed requirements or exposure, or a materially cheaper sufficient remedy warrants reassessment. Explain what changed; reuse the existing finding ID and use `REOPENED` when a previously accepted issue is current again. If intent remains unresolved, use an Open Question. Absence of a prior position changes nothing: proceed on evidence.

## Root-cause deduplication

Group symptoms that share one root cause. Do not inflate counts by reporting each downstream guard, retry, cache, or cleanup path independently when one ownership/state error explains them.

Do not merge unrelated root causes just because they occur in the same file.

When an upstream correction makes another finding unnecessary, preserve both stable IDs if both were previously published and mark the downstream one `SUPERSEDED` with `Superseded-by: <ID>`.

## Finding types

Use one primary type:

- `Defect` — implementation/behavior is wrong;
- `Business` — business/domain semantics are wrong or incomplete;
- `Reliability` — failure/recovery/concurrency/state behavior is unsafe;
- `Accidental Complexity` — required behavior is correct or potentially correct but implemented with materially unjustified responsibility/state/mechanism;
- `Performance` — real workload/resource inefficiency with meaningful impact;
- `Maintainability` — concrete structure makes supported change materially more error-prone or expensive;
- `Security` — real trust-boundary/privilege defect;
- `Test Gap` — important behavior is materially unproven and current tests create insufficient confidence.

Use area/domain tags for secondary dimensions instead of inventing extra primary types.

## Priority model

Priority communicates **impact**, not reviewer confidence.

- **P0 — Critical:** catastrophic loss/corruption, systemic compromise, or unrecoverable production state.
- **P1 — High:** realistic major correctness, business, money/state, recovery, security, performance, or production risk. Accidental complexity may reach P1 only when it materially obscures ownership/safety on a core path or makes safe operation/change genuinely hazardous.
- **P2 — Medium:** real defect/regression, meaningful requirement violation, material accidental complexity, or significant stability/efficiency/maintenance weakness with moderate impact.
- **P3 — Low:** concrete non-blocking improvement with limited impact.

Do not manufacture P3 findings to make a review look busy. Do not inflate aesthetic cleanup into P1/P2.

## Exposure and frequency discipline

Priority stays impact-only, but impact must be stated against the finding's real exposure, never against the mere existence of money somewhere in the system.

Record exposure in the conditional `Blast` header field (see Canonical schema): `live-active`, `tool-active`, `research-default-on`, `research-default-off`, `paused`, or `unknown`. Record measurement basis in `Frequency`: `measured` or `inferred`.

Apply the priority model to the credible consequence and exposure of the supported scenario under review, including normal activation, upgrade, and deployment of a proposed change. P1 does not require a prior production incident, measured frequency, or a money path: a directly established security, data-loss, or major availability defect may qualify before deployment.

Default-off or paused code is not evidence of active production impact. Establish whether and how the supported target can activate the path; state the resulting scope and bounded consequence. Missing frequency measurements remain unknown or `inferred`, not an automatic priority cap. An unverified fact essential to the mechanism limits confidence or publication, while an unknown incident count does not weaken a mechanism already proved. Unquantified financial impact stays unknown — never conclude "no loss" from a single fill, or "production is bleeding" from code alone.

## Confidence model

Confidence communicates how strongly the available evidence supports the mechanism/conclusion:

- **High:** mechanism and relevant evidence are directly established; important contrary explanations were checked where applicable.
- **Medium:** mechanism is well supported but one material fact remains inferred/unverified.
- **Low:** useful lead with material uncertainty. Prefer an observation/Open Question over a durable finding unless the uncertainty itself is decision-relevant.

Severity and confidence must remain independent.

## Finding status

Stable findings use one of:

- `OPEN` — current and unresolved;
- `FIXED` — verified corrected in a later revision;
- `ACCEPTED` — consciously accepted/not planned to change, with rationale;
- `SUPERSEDED` — replaced by another root-cause finding/design decision;
- `REOPENED` — previously fixed/accepted but evidence shows the problem is current again.

Do not delete old IDs from the audit ledger merely because their status changed.

## Stable identity

Finding IDs are repository-level identities, not report-local ordinal numbers.

- Reuse an existing ID for the same root cause across re-reviews.
- Never renumber a finding because its priority or sort order changed.
- Never reuse a retired ID for a different issue.
- For a repository without an existing audit ledger, allocate new IDs monotonically (`FSR-001`, `FSR-002`, ...). Subsequent audits continue from the highest assigned ID.
- When a conclusion changes because the Skill or Domain Pack protocol changed rather than the target changed, keep the ID, record both protocol versions and the reason, and change status only with that citation. Never mint a new ID to launder a protocol-driven reclassification.

The report sorts by priority independently of ID.

## Canonical schema

Required structured header:

```text
ID: FSR-###
Priority: P0 | P1 | P2 | P3
Confidence: High | Medium | Low
Status: OPEN | FIXED | ACCEPTED | SUPERSEDED | REOPENED
Type: ...
Area: ...
Evidence: path:line / test / contract / history / measurement
```

Conditional header fields only when meaningful:

```text
Blocking: yes | no
Depends-on: FSR-...
Superseded-by: FSR-...
Domain-Pack: <name@version>
Blast: live-active | tool-active | research-default-on | research-default-off | paused | unknown
Frequency: measured | inferred
```

Do not fill optional fields with repetitive `none` values.

### P0 / P1 body

Use the full shape:

```text
Problem / Opportunity
Trigger / Workload
Mechanism
Impact
Recommended direction
Verification
```

### P2 body

Keep the same evidence discipline but combine sections when clarity improves. Usually 3–5 short paragraphs/blocks are enough.

### P3 body

Keep it compact: concrete problem/cost, evidence, and recommended direction/verification. Do not give a P3 the same prose weight as a P0.

### Additional Accidental Complexity proof

For this type, also establish:

```text
Required outcome
Irreducible constraints / invariants
Minimum sufficient mechanism
Current mechanism
Accidental complexity delta
Why this layer exists / Disconfirmation attempt
Keep-As-Is reference (the preserved-design entry this simplification cites or overturns, with reason)
Responsibility transfer / behavior-preservation plan
```

These may be compact for P2/P3 but cannot be omitted when they are needed to prove the claim.

## Maintainability bar

Do not publish "hard to maintain" as a finding.

Show a concrete maintenance mechanism, such as a supported change that must be duplicated across several owners/mappings, a contract whose change requires non-local synchronized edits, or a structure that predictably creates inconsistent variants. State the likely change/error cost and evidence.

Duplicated mapping tables that must agree with each other — a key list copied in two or more places, a gate table versus its producer-side field list — are a concrete maintenance mechanism by themselves: a change to one copy that misses the other silently alters governed behavior. Show the copies, the drift (or the missing drift detection), and the change that would diverge them. Prefer a single source of truth; where copies remain, the gate must diff them.

## Test Gap bar

Do not publish "needs more tests" as a finding.

Identify:

1. the important behavior/invariant that is materially unproven;
2. the consequence if it is wrong;
3. why existing tests do not establish the behavior or create false confidence;
4. the smallest test/scenario/evidence that would close the gap.

Use the report's general Evidence/Verification Gaps section for uncertainties that cannot be responsibly assigned a finding priority.

## Tests and measurements

Passing tests are evidence, not proof. Failed tests are evidence only after confirming relevance.

For performance findings, prefer an asymptotic argument tied to real size, profile/trace, benchmark, measured growth, or clearly repeated expensive work. Never fabricate benchmark numbers.

For simplification findings, prefer responsibility/invariant proof over line-count claims.

## Repository writes vs review-platform writes

These are separate capabilities:

- **Repository write access** may be used only for audit artifacts when authorized by the user and the read-only audit discipline in `SKILL.md`.
- **Review-platform API access** (for example PR inline comments/reviews) is optional and separate. Use it only when available and authorized; otherwise place the evidence in the canonical report.

A durable report must not depend on GitHub/GitLab review API availability.
