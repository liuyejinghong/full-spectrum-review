---
name: full-spectrum-review
description: Comprehensive, evidence-driven software audit for repositories, subsystems, PRs, and architecture. Invoke only when explicitly named or a full audit is requested — never for ordinary, quick, or diff-only reviews.
---

# Full-Spectrum Review

Use this Skill when explicitly invoked — by name or by an explicit request for a comprehensive audit — for repository, subsystem, PR, commit, production-readiness, or architecture audits. It is deliberately heavyweight; do not pull it into ordinary or quick review requests.

Current Skill version is recorded in `VERSION`. Record that version in persisted audit metadata when available. `CHANGELOG.md` is for maintainers and should not be loaded during ordinary audits unless version/history is relevant to the task.

## Default contract

A normal invocation means a **full audit of the requested target**. Do not ask the user to choose review axes unless they explicitly request a narrow audit.

"Full" means every materially relevant subsystem, boundary, business flow, and risk dimension is included in the audit plan and receives an explicit coverage status. It does **not** mean every file must be read at identical depth.

For a PR or commit, the target is the change and all materially affected contracts, callers, callees, state, tests, operations, and business behavior. For a repository audit, the target is the repository's important production and business behavior.

## Read-only audit discipline

The audited implementation is **read-only by default**. Repository write authorization permits writing audit artifacts only; it does not authorize modifying audited source code, configuration, migrations, runtime behavior, or business data.

Read-only binds **modification of the audited implementation**, not evidence gathering. Running the target's tests, executing benchmarks or reproducible experiments (sandboxed outside the audited tree, or with ephemeral artifacts cleaned up), and verifying external contracts over the network are expected evidence work — use every capability the harness and the user actually grant. Never self-impose a narrower mode (offline, read/grep-only, no test execution) and present it as discipline: an audit that could have run the tests and chose not to is guessing, not reviewing. When the environment genuinely lacks a capability, record it as an evidence gap with its confidence impact.

Any implementation fix is a separate follow-up task requiring explicit user authorization. Do not "fix while reviewing."

## Core workflow

1. **Read prior audit state.** If the target repository already contains audit reports or an audit index, read them first so finding identity, status, prior Keep-As-Is decisions, and unresolved questions survive re-review.
2. **Bind the target.** Record repository/target and exact revision when available. For PRs, record base and head.
3. **Create an audit plan.** Identify important subsystems, execution paths, stateful components, external boundaries, business flows, and operational surfaces. Declare this wave's coverage; deferred Units converge in later waves under the same ledger. Assign intended depth such as `deep`, `sampled`, or `none`. Flag enumerable sets (gate/allowlist/key tables, lifecycle state×event matrices, mode pairs, route×auth decisions) as must-enumerate: `sampled` is never sufficient for them.
4. **Choose execution mode.** For large targets, use bounded Audit Units. If the current harness supports isolated workers/subagents and parallelism is materially useful, run suitable units concurrently; otherwise execute the same units sequentially. Follow `references/orchestration-protocol.md`.
5. **Reconstruct the system.** Read repository instructions, specifications, ADRs, architecture docs, Issues/PRs, configuration, tests, and relevant operational material. Reconstruct purpose, entities, ownership, authoritative state, lifecycles, and invariants. In multi-worker mode, the Lead produces a compact Shared Audit Brief.
6. **Select Domain Packs.** Inspect available Domain Packs, load every applicable pack, and record which packs were used. Follow the Domain Pack rules below.
7. **Apply First Principles before accepting architecture.** For important or structurally non-trivial areas, derive the required outcome, irreducible constraints, invariants, and minimum sufficient mechanism before judging the current mechanism. Treat loaded Domain Pack invariants and external semantics as constraint inputs: essential domain complexity that source code alone cannot derive must not be judged accidental. Read `references/first-principles-review.md`.
8. **Run all applicable core lenses.** Read and apply the engineering, business, and optimization references. These are reasoning lenses, not separate final reports. Subsystem Audit Units apply the relevant lenses within their own scope.
9. **Generate candidates with high recall.** Follow behavior across changed and unchanged code where required to understand the target correctly. Worker outputs are candidate packets, not canonical findings.
10. **Verify findings with high precision.** Apply `references/finding-protocol.md`, including disconfirmation for accidental-complexity claims. Resolve material cross-unit contradictions before final classification.
11. **Deduplicate by root cause and rank.** The Lead preserves stable finding identity across re-reviews and centrally assigns final priority/status; workers must not allocate canonical IDs or terminal verdicts.
12. **Finalize coverage honestly.** Mark each planned area `COMPLETE`, `PARTIAL`, `NOT_COVERED`, or `INSUFFICIENT_EVIDENCE` and state why.
13. **Produce the canonical audit artifact.** Follow `references/reporting-protocol.md`; persist the report and audit index when writes are authorized.

## Core references

During a full audit, load the references needed for the target:

- `references/orchestration-protocol.md` — model-neutral Audit Unit decomposition, optional parallel workers, Shared Audit Brief, Reviewer Packets, cross-boundary verification, sequential fallback.
- `references/first-principles-review.md` — **Necessity**: what must exist, what is accidental complexity.
- `references/engineering-review.md` — correctness, contracts, state, failure/recovery, concurrency, data, compatibility, tests, operations.
- `references/business-logic-review.md` — domain truth, business rules, invariants, lifecycle, timing, economics, external reality.
- `references/optimization-review.md` — **Cost**: given justified mechanisms, evaluate algorithmic, CPU, memory, I/O, network, concurrency, resource, and external-service cost.
- `references/finding-protocol.md` — canonical finding types, priority, confidence, status, evidence bar, and schema.
- `references/reporting-protocol.md` — coverage ledger, stable audit ledger, report structure, re-review, and persistence.

For a single-unit target (see Execution sizing under Audit orchestration boundary), the orchestration reference may be skipped; load only the references that unit needs.

Do not duplicate normative definitions from these references in ad-hoc output.

## Audit orchestration boundary

The Skill defines **logical Audit Units and packet contracts**, not a vendor-specific subagent API.

### Execution sizing

Size execution to the target — a general preference for "staying light" loses to concrete process, so the tiers are explicit:

- **single-unit** — narrow PR, small subsystem, or bounded question: skip the orchestration reference, Shared Audit Brief, and multi-phase structure; one compact report with a short Coverage Ledger;
- **sequential-units** — medium target, or isolated workers unavailable: the same bounded units executed one by one with durably recorded Reviewer Packets;
- **parallel-units** — large target with isolated workers available: units run concurrently.

All three modes share the same finding bar and produce the same canonical artifact. A single-unit audit is a correctly sized audit, not a lower-standard one.

Prefer subsystem/flow decomposition over splitting the whole repository into one Engineering worker, one Business worker, and one Optimization worker. Each subsystem worker should apply all relevant lenses and Domain Packs inside its scope; use separate cross-cutting units only for questions such as architecture/ownership, end-to-end business lifecycle, or long-running resource behavior.

Workers share factual context but should keep first-pass candidate conclusions independent when practical. Workers may suggest candidate impact/confidence, but only the Lead/Coordinator may allocate/reuse `FSR-###` IDs, assign final priority/blocking/status, root-cause deduplicate, persist the canonical report, or issue a terminal verdict.

If workers are unavailable, execute the same Audit Units sequentially and retain compact Reviewer Packets so context compression does not erase earlier evidence.

## Domain Pack contract

Domain knowledge is extensible and must not be hard-coded into the core Skill.

Bundled packs live under `domains/<domain>/DOMAIN.md`. Also consider project/private Domain Packs that the current Agent harness makes available. Inspect pack metadata and load **all** packs whose applicability matches the audited system; zero, one, or several packs may apply.

A Domain Pack may add:

- domain vocabulary and concept distinctions;
- domain invariants;
- external-system semantics;
- domain-specific scenario sweeps and failure patterns;
- domain-specific severity context.

A Domain Pack must **not** redefine the core priority model, finding verification bar, report schema, or First-Principles method. Core contracts win on conflict. When packs overlap, combine the domain facts and deduplicate the final finding by root cause; do not emit duplicate findings merely because two packs surfaced the same issue.

`domains/_CONTRACT.md` defines the authoring contract for creating/validating packs. **Do not load it during ordinary audits** unless pack structure itself is under review; load only the applicable `DOMAIN.md` files. Record loaded packs and versions in Audit Metadata.

Domain Packs version independently from the core Skill. A report should record both the core Skill version and every loaded pack version when available.

## First-Principles boundary

First Principles answers **"does this mechanism need to exist?"** It owns accidental complexity, duplicated ownership/state, unnecessary abstraction, unnecessary recovery layers, obsolete compatibility/configuration paths, and minimum-sufficient-mechanism reasoning.

Optimization answers **"given that the mechanism is justified, is its runtime/operational cost reasonable?"** If an optimization investigation reveals that a layer is unnecessary rather than merely expensive, hand that conclusion to the First-Principles bar instead of maintaining two competing rules.

## Business authority discipline

Do not assume code, tests, docs, or current behavior are automatically business truth. Build a target-specific **Business Authority Map** from available external contracts, specifications/ADRs, user-facing commitments, tests, and implementation evidence. State material conflicts.

If required business intent cannot be established with sufficient confidence, record an Open Question rather than manufacturing a business finding.

## Exact-revision discipline

When the platform exposes revisions, bind the audit to the exact reviewed revision. If the user supplied an expected head and the current head differs, report drift instead of silently applying an old conclusion to new code.

For a PR, re-read the current head immediately before a terminal verdict. A drifted head invalidates the old terminal verdict but does not invalidate already persisted historical evidence for the old revision.

All Audit Units in one audit wave should inspect the same bound revision. Do not silently merge worker evidence from different heads.

## Anti-noise rules

Do not publish:

- style preferences without meaningful correctness, maintenance, or efficiency impact;
- hypothetical edge cases unreachable through supported behavior;
- speculative security hardening without a real trust boundary or attack path;
- micro-optimizations without a plausible meaningful workload;
- extra wrappers, flags, compatibility layers, migration frameworks, checksums, or defensive machinery without a current requirement;
- "over-engineered" judgments that cannot identify a simpler sufficient mechanism and investigate why the current layer exists;
- unrelated historical debt outside the audited target's meaningful behavior;
- duplicate symptoms of one root cause as separate findings.

Passing tests are evidence, not proof of correctness, business validity, or architectural necessity.

## Required deliverable

A full audit is incomplete until one coherent canonical report is produced. Parallel execution does not create multiple final reports. The report may be compact for a narrow PR and extensive for a repository-wide audit, but it must still record scope/coverage, exact revision when available, Skill/Domain Pack versions when available, verified findings, priorities, and evidence.

Persist audit artifacts under the workspace root defined by `references/reporting-protocol.md` (`fsr-reports/<target>/`). Writing into the audited repository itself is a separate, explicitly authorized export. If no writable workspace exists, return the complete artifact to the user unchanged.

## Versioning

`VERSION` is the canonical current core version; record it in Audit Metadata. Versioning policy — pre-1.0 SemVer, independently versioned Domain Packs, optional tags/releases — is defined at the top of `CHANGELOG.md`, which ordinary audits do not need to load.

## Terminal result

For PR merge decisions, the verdict is one of:

- `APPROVE`
- `APPROVE_WITH_NON_BLOCKING_FINDINGS`
- `REQUEST_CHANGES`

Two conditions terminate a PR audit without a merge verdict; they are outcomes, not verdicts:

- `HEAD_DRIFT` — the head moved, so the previous verdict no longer applies;
- `INSUFFICIENT_EVIDENCE` — the available evidence cannot responsibly support any verdict.

For repository-wide audits, give an overall health/risk assessment instead of forcing a merge verdict.

The audit succeeds when a maintainer can tell **what was actually covered, what matters most, what to fix first, why, what remains uncertain, and what should be preserved**.
