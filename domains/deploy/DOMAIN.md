---
domain: deploy
version: 4
applies-when:
  - system ships versioned artifacts to remote or stateful targets
  - release performs staged/canary rollout, rollback, or state migration
  - a failed release can leave targets mixed, degraded, or partially migrated
extends: core
last-verified: 2026-09-05
---

# Deploy Domain Pack

Use this pack for systems whose release itself is a risk surface: versioned
artifacts deployed to stateful or remote targets, where rollback, migration,
and partial-fleet states are first-class concerns.

This pack supplies **release-specific facts and scenarios**. Generic retry,
concurrency, evidence, priority, First-Principles, and reporting rules remain
owned by core. Trading-specific semantics belong to the trading pack.

This pack is distilled review experience from three source types — production
release-incident postmortems of a live stateful system (cross-generation
rollback splices, false-success migrations, preflight lockouts, remediation
loops), a frozen single-fact-chain release runbook (exact source, one build,
frozen manifest, ordered single-shot transactions, terminal receipts), and
reference-implementation convergence across independent progressive-delivery
systems (Argo Rollouts canary/pause/abort semantics, Flagger automated
metric-gated promotion and rollback, SRE Workbook canarying: per-population
evaluation, one-canary-at-a-time, reproducible builds) — generalized without
referencing any deployment. It is high-value experience to check, **not universal law**:
every statement is a verify/challenge question. A target with an evidenced
reason to differ records its reasoning instead of complying. Statements
conditioned on features the target does not have (canary lanes, migration
machinery, flag systems) simply do not apply. Where this pack conflicts with
the target's evidenced requirements, those win and the conflict is recorded.

This pack judges the **release machinery**, not the current live consistency
of any target. Whether the artifact *can* be shipped, rolled back, and
verified is auditable from the repository; what is running on a remote host
right now is operational truth for the operator to read, not for the audit
to declare.

## Domain Glossary

Keep these concepts distinct when they exist in the target:

- **Candidate / artifact** — the immutable bytes proposed for release, identified by digest, not by tag or filename.
- **Manifest / release declaration** — the release inputs binding source, artifact, targets, and applicable migration or rollout policy. A manifest is one representation; an equivalent authoritative platform record can carry the same facts.
- **Preflight** — read-only checks run before any mutation. A rejection here must leave every target untouched.
- **Terminal receipt / result** — a recoverable outcome bound to a release attempt and target. A platform status record or structured log can serve this purpose if its identity and outcome are unambiguous.
- **Generation** — a state snapshot paired with the external facts it was reconciled against. Same bytes with different external facts are different generations and are not interchangeable.
- **Canary** — the first real target(s) in rollout order, observed under real behavior. Not a sandbox, not a mock.
- **Rehearsal** — a proof run against copies or staging that grants no production authority.
- **fail-closed terminal** — named end states (`recovered`, `blocked`) that stop the rollout and preserve evidence, as opposed to silent retries.

Do not collapse build → qualify → deploy → verify → rollback into one
"release succeeded" flag unless the machinery genuinely makes them atomic.

## Domain Invariants

Adapt these to the target's actual platform, but challenge violations explicitly:

- Qualification applies to the artifact actually deployed. Preserve artifact identity through promotion; if rebuilding changes the bytes, establish what qualification still applies rather than silently inheriting the earlier result.
- Release inputs have an authoritative identity. Target, artifact, migration, or rollout-policy overrides must be authorized and reflected in that identity; do not let independently supplied inputs silently diverge.
- Rollback is generation-safe: prior state may be restored only while external facts are unchanged. If the outside world progressed, reconcile forward — never blind-restore old state over a new world.
- Preflight is read-only: rejection before mutation is the safe shape. Preflight identity must bind semantic identity (what the action means), not representation churn (revision counters, refreshed display fields).
- Release and recovery paths agree on state ownership, identity, and supported recovery semantics. A separate rollback controller is valid when it preserves those contracts and cannot race an active rollout.
- Distinguish a confirmed failure from an unknown transport outcome. Recover the attempt's status before an unsafe retry; retry is valid when the platform's idempotency and recovery contract establishes that it cannot duplicate or conflict with an earlier action.
- Release success does not itself restore permission or resolve degradation. Access or mode changes require the target's authorization and recovery conditions, whether carried by the release transaction or a separate operation.
- Where staged rollout is supported, promotion obeys its declared policy and evidence. A failing canary must not silently promote; continuing after recovery requires that the policy's conditions and authorization still hold.
- Migration exactness: accept only exact observed deltas; unrelated drift is rejected, not absorbed. A migration that reports success is not proof — verify by composition against a copy of the target state.
- Old-running is not recovered: rollback success must prove the full baseline (identity, state, writers, external coverage, access) — a revived process passing a liveness check is not a recovery.
- Distinguish an artifact defect from a transient environment or delivery failure. A defective candidate needs correction and qualification; retrying unchanged bytes after an external failure may be valid when its cause is resolved and the retry is safe and authorized. Preserve each attempt's outcome and identity.
- The prior artifact stays available for the rollback window: retention shorter than the window voids the rollback path — a rollback target that no longer exists is not a rollback plan.
- A failed attempt's deciding reason is recoverable from its result or a durable linked diagnostic; operators must not need to guess which failure controls promotion.
- Operator and emergency changes must preserve authorization, state integrity, and traceability. Do not infer the deployed state solely from artifact identity when supported configuration or repair operations can change it.

## External Semantics

Release machinery depends on external systems whose guarantees are weaker
than they look. Review the **actual platform contracts** for the target
rather than assuming them.

Verify as applicable:

- artifact registry semantics: tag mutability vs digest immutability; retention vs the rollback window;
- orchestrator status APIs: eventual consistency, transport uncertainty, and the difference between a status screen and field truth;
- target host semantics: what a health endpoint actually proves (process alive vs dependencies reachable vs business acceptance);
- migration tooling semantics: ordering, idempotency, locking behavior on large tables, and whether re-running is safe;
- secret/config injection semantics: what the deploy pipeline can and cannot override, and where per-environment values live.

A release dashboard is a claim, not evidence. Every load-bearing fact
(what version runs where, whether protection/coverage holds) needs an
independent read-back from the target itself.

## Scenario Sweep

Exercise these against the release machinery during Business/Engineering review:

- repeated release failures: check whether the next attempt addresses the observed cause or merely repeats an unsafe mutation; stopping conditions follow the target's incident policy and failure semantics;
- partial fleet: some targets activated, mid-fleet blocked — the remainder must stay untouched with no silent continuation;
- migration reports success while changing only a version envelope: composition verification against a target-state copy must reject it;
- preflight rejects on representation churn with unchanged semantics: the lease identity is too wide;
- an emergency mechanism is created from missing local proof without verifying external coverage: proof absence is not protection absence — the gate must check external facts first;
- an acceptance gate couples unrelated verifications (stale-cleanup tied to full-plan proof, capability readers stacked beyond the active schema): over-wide gates fail closed into gridlock — scope each gate to its own action's preconditions;
- a product release smuggles a deployment-tooling upgrade without independent platform acceptance: tooling and product version independently — verify tooling identity first, then consume it as a frozen input;
- rollback with a progressed outside world: the machinery must refuse the restore and reconcile instead;
- unknown receipt or transport: establish the earlier attempt's outcome or the platform's safe retry guarantee before resubmission;
- canary passes but relevant facts drift before the remainder: reassess the changed preconditions and obtain any authorization required by the promotion policy;
- post-release verification relies on liveness alone: demand an end-to-end smoke slice, not just a health check;
- the canary is judged by aggregate fleet health while per-population service metrics (success rate, latency, canary vs control) diverge: evaluation is blind by construction — demand per-population breakdown on service-level metrics, never infra-only signals;
- overlapping rollouts share traffic or metrics: verify failures remain attributable and rollback ownership does not conflict; serialize when the platform cannot isolate their evidence and effects;
- several changes share one artifact: check whether reverting them together violates a real availability, compatibility, or recovery requirement before proposing flags or finer release granularity;
- a new tooling layer's only output is new failures: the layer itself is the suspect — shrink or remove it rather than staffing around it.

## Severity Context

Domain facts that raise the impact of a core finding (never redefining P0–P3):

- a required rollback path is absent or unproven: identify which failure becomes harder to recover from and its concrete consequence; assess it with the core priority model, without automatic priority increments;
- deploy verification is liveness-only: every deploy defect's blast radius grows by the detection delay;
- flag/configuration debt without owner or removal date: each stale branch raises change risk and incident-confusability;
- second failure without a stop line: turns a contained failure into a remediation loop — process amplification, not just mechanism cost;
- mixed-generation state reachable after rollback: the highest-severity shape in this domain, because every subsequent decision reasons from a false past.

## Out of Scope / Core Boundary

Explicitly core-owned (do not duplicate): generic retry/backoff/idempotency
reasoning, concurrency hazards, evidence and priority models,
First-Principles necessity method, report and ledger lifecycle.

Explicitly another domain: trading semantics (venue truth, protection
orders, fill accounting) belong to the trading pack; combine facts and
deduplicate by root cause when both packs fire.

Explicitly operations, not audit: live-target forensics (logging into hosts,
declaring what runs now). The pack covers whether the machinery *can*
guarantee consistency, never the current live consistency itself.
