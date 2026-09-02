# Audit Orchestration Protocol

Use this protocol to make full-spectrum audits scale beyond a single agent's comfortable context window without binding the Skill to any vendor-specific subagent API.

This file owns **audit execution decomposition and synthesis**. It does not redefine finding verification, priority, reporting, or Domain Pack semantics.

## Core principle

Treat a large audit as a set of bounded **Audit Units** coordinated by one logical Lead/Coordinator.

If the current Agent harness supports isolated workers/subagents and parallel execution is materially useful, execute suitable Audit Units concurrently. If it does not, execute the same units sequentially.

The audit contract and final artifact must be equivalent in both modes.

```text
same audit plan
      ↓
parallel workers when available
      OR
sequential bounded units otherwise
      ↓
same candidate-packet contract
      ↓
same verification / dedup / report
```

Do not assume tool names such as `Task`, `spawn_agent`, Agent Teams, Codex workers, or any specific provider API.

## When to use multiple Audit Units

Decompose when doing so materially improves context isolation, coverage, or throughput. Typical signals:

- repository/source material is larger than one reviewer's reliable working context;
- important subsystems have clear ownership or execution boundaries;
- several high-risk flows can be inspected independently before synthesis;
- the audit would otherwise require repeated context compression that risks losing earlier evidence;
- parallel workers are available and the coordination cost is lower than the expected review cost.

Do **not** force parallelism for a small target. One reviewer is often better for a narrow PR or compact repository.

## Preferred decomposition: system first, lens second

Prefer Audit Units that own a coherent subsystem, business flow, or external boundary.

Examples:

```text
Execution / order lifecycle
Position / reconciliation
Market data / strategy
Backtest / simulation
Persistence / restart
Operator control
API / control plane
Deployment / operations
```

Each subsystem worker applies all relevant core lenses and Domain Packs inside its assigned scope.

Avoid making the primary decomposition merely:

```text
Engineering worker
Business worker
Optimization worker
```

because each worker may then need to reread most of the repository and rebuild the same architecture/domain model.

### Cross-cutting Audit Units

After or alongside subsystem review, create cross-cutting units only where they add distinct value, for example:

- First-Principles / architecture / ownership across subsystem boundaries;
- end-to-end business/domain lifecycle;
- performance/resource/long-running behavior across queues, tasks, caches, I/O, and services;
- security/trust boundaries when materially applicable;
- a Domain Pack scenario that spans several modules.

These units should inspect cross-boundary contracts rather than duplicate every subsystem review.

## Lead / Coordinator responsibilities

The Lead owns the audit as a whole. It must:

1. bind the exact target/revision;
2. read prior audit state;
3. build the Audit Plan and Coverage Ledger skeleton;
4. reconstruct enough repository-level purpose/architecture/domain context to create a Shared Audit Brief;
5. select applicable Domain Packs and record their versions;
6. define Audit Units with explicit boundaries and expected depth;
7. dispatch/execute units using the current harness's available mechanism;
8. resolve cross-unit contradictions and evidence gaps;
9. verify publishable findings against `finding-protocol.md`;
10. deduplicate by root cause;
11. allocate/reuse stable finding IDs and final priority/status;
12. produce the canonical report and terminal verdict when applicable.

The Lead does **not** need to retain every source file in active context. It must retain enough shared facts and evidence references to judge worker packets and reopen source evidence when needed.

## Shared Audit Brief

Before independent worker passes, provide a compact shared factual brief. Keep it materially smaller than the repository and avoid preloading tentative findings.

Recommended contents:

```text
Audit target + exact revision
Requested scope
Repository purpose
High-level architecture / subsystem map
Critical business/domain entities
Known authoritative state / ownership boundaries
Critical invariants already supported by evidence
Business Authority Map
Applicable Domain Packs + versions
Repository-specific instructions / constraints
Prior open findings and important Keep-As-Is constraints
Audit Unit boundary for this worker
```

Separate **shared facts** from **tentative conclusions**.

Workers may share the same factual brief, but their first-pass candidate conclusions should remain independent when possible to reduce anchoring.

## Independent first pass

During the initial discovery pass:

- do not feed one worker's tentative findings to another merely to make them agree;
- allow different workers to reach conflicting explanations;
- preserve evidence supporting those disagreements;
- treat contradictions as signals for targeted verification, not as a reason to average opinions.

Example:

```text
Worker A: local PositionState appears authoritative
Worker B: exchange snapshot appears authoritative
```

The Lead should create a focused verification task for the authority boundary rather than selecting whichever statement arrived first.

## Reviewer Packet

Every Audit Unit returns a compact evidence packet with a common logical shape. Exact formatting may vary by harness.

```text
Audit Unit
Reviewed revision
Assigned scope / expected depth
Actual coverage status
Files / components / contracts inspected
Relevant invariants / authority assumptions
Domain Packs applied

Candidate Findings
- local candidate label
- primary type / area
- trigger or workload
- mechanism
- impact
- evidence references
- confidence in the candidate
- disconfirmation work when required

Cross-boundary concerns
- fact or contract another unit / Lead must verify

Keep-As-Is candidates
- important proven design/invariant worth preserving

Evidence gaps
- what could not be established and why
```

Packets should reference concrete source locations, contracts, tests, commands, or other evidence so the Lead can verify without rereading the worker's entire local context.

## Candidate-only authority

A worker/subagent produces **candidate findings**, not canonical findings.

Workers must not independently:

- allocate or reuse repository-level `FSR-###` IDs;
- finalize P0/P1/P2/P3 priority;
- decide final `Blocking` status;
- mark prior findings `FIXED`, `SUPERSEDED`, or `REOPENED` without Lead verification;
- submit a terminal PR verdict;
- persist an independent final audit report.

A worker may suggest likely impact/severity to help synthesis, but the Lead owns the final classification after cross-unit verification and deduplication.

This prevents several workers from publishing multiple symptoms of one root cause as separate canonical findings.

## Multi-phase execution

A robust large-repository audit normally follows four phases.

### Phase 0 — Plan and shared model

Lead:

- maps the repository/target;
- chooses Domain Packs;
- creates the Coverage Ledger skeleton;
- builds the Shared Audit Brief;
- defines Audit Units.

### Phase 1 — Independent discovery

Execute subsystem/flow units in parallel when supported and useful.

Each unit performs full-spectrum reasoning within its scope and returns a Reviewer Packet.

### Phase 2 — Cross-boundary verification

The Lead compares packets and creates targeted follow-up units for:

- contradictory authority/state assumptions;
- lifecycle gaps between modules;
- candidate findings whose mechanism crosses unit boundaries;
- duplicated candidate symptoms;
- missing evidence required for a high-impact conclusion.

Follow-up units should be narrow and evidence-driven rather than rerunning the entire audit.

### Phase 3 — Canonical synthesis

Lead:

- verifies candidates;
- performs required disconfirmation;
- deduplicates by root cause;
- reconciles prior stable IDs/statuses;
- assigns final priority/confidence/blocking where applicable;
- updates Coverage Ledger truthfully;
- produces one canonical report.

## Exact-revision consistency

All workers in one audit wave must review the same exact revision when the platform exposes one.

If a moving branch or PR head drifts during the audit:

- do not mix evidence from different heads into one canonical conclusion without explicitly rebinding/reviewing the affected units;
- historical packets remain evidence for their original revision;
- a terminal PR verdict requires the Lead to recheck the current head as required by `SKILL.md`.

## Domain Packs in distributed review

The Lead records the selected Domain Packs in the Shared Audit Brief.

A worker loads only packs relevant to its Audit Unit unless the whole-pack context is needed. Cross-cutting domain reviewers may apply one pack across several units.

Do not duplicate Domain Pack rules into every packet; record the pack/version and the domain-specific evidence/result.

## Context-compaction resilience

The orchestration design should survive context compression.

Prefer compact durable/recoverable coordination artifacts:

- Audit Plan / Coverage Ledger skeleton;
- Shared Audit Brief;
- Reviewer Packets;
- prior audit index/reports;
- concrete evidence references.

Do not rely on the Lead remembering undocumented conclusions from a long earlier context.

Internal worker scratch is not a canonical audit artifact and should not be committed to the audited repository unless the user/repository explicitly wants it.

## Sequential fallback

When isolated workers are unavailable, the Lead executes the same Audit Units one by one.

After each unit:

1. produce the same Reviewer Packet;
2. retain the compact packet and shared brief;
3. allow local implementation detail to leave active context when no longer needed;
4. proceed to the next unit;
5. perform the same Phase 2 verification and Phase 3 synthesis.

Sequential fallback is not a lower-standard audit. It is the same logical protocol with less execution concurrency.

## Avoid orchestration overhead

Do not create more Audit Units than the target justifies.

Bad decomposition indicators:

- two workers repeatedly inspect the same files without distinct questions;
- coordination packets are larger than the code each worker reviews;
- most findings require immediate cross-worker reconstruction because unit boundaries cut through one coherent lifecycle;
- workers exist only to satisfy a fixed number rather than a real architecture/risk boundary.

Merge units when coordination cost exceeds context/throughput benefit.

## Completion condition

A parallel/distributed audit is complete only when:

- every planned Audit Unit has an explicit coverage state;
- cross-boundary contradictions relevant to final findings are resolved or marked `INSUFFICIENT_EVIDENCE`;
- candidate findings have been verified and root-cause deduplicated centrally;
- the final report is one canonical artifact, not a concatenation of worker reports.
