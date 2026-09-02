# Full-Spectrum Review

> A model-neutral Agent Skill for **comprehensive software audits**: reconstruct the problem from first principles, audit engineering/business correctness and justified runtime cost, apply relevant Domain Packs, scale large reviews through bounded Audit Units, and persist verified findings as a prioritized re-reviewable audit record.

**Current Core version: `v0.3.0`** · [CHANGELOG](CHANGELOG.md) · [简体中文](README.md) · **English**

## What it does

A normal invocation means a **full audit of the requested target**. Full does not mean reading every file at identical depth; it means every materially relevant boundary/flow is represented in an Audit Plan and the final Coverage Ledger states what was deeply reviewed, sampled, not covered, or blocked by insufficient evidence.

```text
exact target / revision
→ audit plan + coverage ledger
→ bounded Audit Units when useful
→ system/domain/ownership/invariants
→ first-principles minimum sufficient mechanism
→ 0..N applicable Domain Packs
→ engineering + business + cost review
→ candidate findings + evidence + disconfirmation
→ cross-unit verification + root-cause dedup
→ P0/P1/P2/P3 + recommended execution order
→ persistent report + stable finding ledger
```

## Large repositories and limited context

Full-Spectrum Review does **not** require a 1M-context model.

Large targets can be decomposed into bounded **Audit Units**. If the current harness supports isolated workers/subagents and parallelism is useful, suitable units may run concurrently. If workers are unavailable, the exact same logical units run sequentially.

```text
                    Lead / Coordinator
                           │
                  Shared Audit Brief
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   Execution Unit     Position Unit      Backtest Unit
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                 Cross-boundary Verify
                           │
              Evidence + Root-cause Dedup
                           │
                    Canonical Report
```

Prefer subsystem/business-flow/external-boundary decomposition over creating one repository-wide Engineering worker, one Business worker, and one Optimization worker. Subsystem workers apply all relevant lenses and Domain Packs inside their scope; cross-cutting units inspect ownership, end-to-end business lifecycles, performance/resource behavior, or other boundaries that span modules.

Workers receive a compact **Shared Audit Brief** containing the exact revision, system map, important authority/invariant facts, Business Authority Map, selected Domain Packs, prior findings/Keep-As-Is decisions, and their assigned scope.

Workers return **Reviewer Packets** containing candidate findings and evidence. They do not allocate canonical `FSR-###` IDs or finalize priority, blocking, status, or terminal verdicts. The Lead/Coordinator centrally verifies, resolves contradictions, deduplicates root causes, reuses stable IDs, and produces the one canonical report.

Parallel mode therefore does not mean concatenating several worker reports.

See [`references/orchestration-protocol.md`](references/orchestration-protocol.md).

## First Principles: Necessity

Before accepting a materially important architecture, the reviewer reconstructs:

```text
Required Outcome
+ Irreducible Constraints
+ Required Invariants
→ Minimum Sufficient Mechanism
```

It then challenges whether additional state, ownership, workers, caches, abstractions, compatibility paths, recovery layers, and configuration branches carry independent current requirements.

An `Accidental Complexity` finding does not require a reproduced bug, but it requires an explicit **disconfirmation attempt**: investigate why the challenged layer exists using available history, tests, ADRs, callers, operators, or external contracts. No meaningful contrary-evidence search means observation/hypothesis, not a publishable finding.

Authoritative rules: [`references/first-principles-review.md`](references/first-principles-review.md) and [`references/finding-protocol.md`](references/finding-protocol.md).

## Optimization: Cost

The optimization lens is intentionally narrower:

> Given that a mechanism is justified, is its runtime/resource/operational/external-service cost reasonable?

It covers algorithmic cost, CPU, memory, I/O, network, batching, contention, resource lifecycle, external-service cost, and long-running stability. "This subsystem should not exist" belongs to First Principles rather than a competing optimization rule.

See [`references/optimization-review.md`](references/optimization-review.md).

## Business authority

Business review builds a target-specific **Business Authority Map** from the evidence actually governing the system: external contracts, specs/ADRs, user-facing commitments, tests, and implementation/operational evidence.

There is no universal hard-coded ordering across every domain. When required intent cannot be established responsibly, the report records an **Open Question for the Maintainer** rather than manufacturing a business defect.

## Domain Packs

Core owns **how to audit**. Domain Packs own **domain facts a generic reviewer cannot reliably infer from source alone**.

```text
Core Audit Method + 0..N Domain Packs
```

Packs live under `domains/<domain>/DOMAIN.md` and follow [`domains/_CONTRACT.md`](domains/_CONTRACT.md). Multiple packs may apply to one system.

Packs may add domain glossary, invariants, external semantics, scenarios, and severity context. They may not redefine core priority/confidence/finding/reporting rules.

Core does not register packs one-by-one. Adding `domains/payments/DOMAIN.md` should not require editing `SKILL.md`.

`domains/_CONTRACT.md` is an authoring contract; ordinary audits load only applicable `DOMAIN.md` packs.

### Trading pack

[`domains/trading/DOMAIN.md`](domains/trading/DOMAIN.md) v2 covers market-data timing/look-ahead, backtest/live parity, signal/order/fill/position semantics, partial fills, unknown order outcomes, reconciliation, precision, accounting, protection, rate limits, time/signature windows, order flags/trigger sources, position/margin modes, instrument lifecycle, multi-instance account ownership, and credential permissions.

It stays provider-neutral and tells the reviewer to verify the actual venue contract rather than treating one exchange's parameters as universal truth.

## Persistent audit lifecycle

Findings have stable repository-level IDs and statuses:

```text
OPEN / FIXED / ACCEPTED / SUPERSEDED / REOPENED
```

Priority changes do not renumber findings. If the audited repository has no equivalent convention, the Skill uses a lightweight ledger:

```text
docs/reviews/
├── INDEX.md
└── <audit reports>.md
```

The index is intentionally not an issue tracker.

Coverage, re-review, Keep-As-Is persistence, orchestration traceability, and report structure are defined in [`references/reporting-protocol.md`](references/reporting-protocol.md). Canonical finding type/priority/confidence/status/schema are defined only in [`references/finding-protocol.md`](references/finding-protocol.md).

## Report traceability

Persisted reports record, when available:

- exact target revision/base/head;
- Core Skill version and Skill revision;
- execution mode (`single-unit`, `sequential-units`, or `parallel-units`);
- loaded Domain Packs and their independent versions;
- Coverage Ledger;
- stable finding states and evidence.

This makes it possible to tell whether a changed conclusion came from a changed target, changed audit protocol, changed Domain Pack knowledge, or newly available evidence.

## Read-only audit discipline

Audit authorization is read-only for the audited implementation. Repository write permission authorizes audit artifacts only. Source/config/runtime fixes require a separate explicit follow-up authorization.

## Versioning

The Core Skill follows Semantic Versioning. [`VERSION`](VERSION) is the canonical current Core version and [`CHANGELOG.md`](CHANGELOG.md) records user-visible protocol changes.

The project is still pre-1.0:

- `MINOR` — new capabilities or material audit/report-contract changes; pre-1.0 incompatible protocol changes may also increment MINOR;
- `PATCH` — corrections/clarifications that do not materially change the main audit contract;
- `MAJOR` — reserved after 1.0 for incompatible core-protocol changes.

Domain Packs version independently. Core `0.3.0` can therefore be used with Trading Pack `v2`, and a report records both.

Git tags/releases may mirror `VERSION` when maintainers publish them, but runtime behavior does not depend on release infrastructure.

## Layout

```text
full-spectrum-review/
├── SKILL.md
├── VERSION
├── CHANGELOG.md
├── README.md
├── README.en.md
├── references/
│   ├── orchestration-protocol.md
│   ├── first-principles-review.md
│   ├── engineering-review.md
│   ├── business-logic-review.md
│   ├── optimization-review.md
│   ├── finding-protocol.md
│   ├── reporting-protocol.md
│   └── example-finding.md
└── domains/
    ├── _CONTRACT.md
    └── trading/
        └── DOMAIN.md
```

Progressive disclosure keeps the core Skill small while loading detailed/domain knowledge only when relevant. `CHANGELOG.md` and the Domain Pack authoring contract are not loaded during ordinary audits.

## Install

Prefer the vendor-neutral Agent Skills location when your client supports it:

```bash
git clone https://github.com/liuyejinghong/full-spectrum-review.git .agents/skills/full-spectrum-review
```

Common currently supported locations include:

| Client | Project / workspace | User / global |
|---|---|---|
| Cursor | `.agents/skills/` or `.cursor/skills/` | `~/.agents/skills/` or `~/.cursor/skills/` |
| Gemini CLI | `.agents/skills/` or `.gemini/skills/` | `~/.agents/skills/` or `~/.gemini/skills/` |
| GitHub Copilot | `.agents/skills/`, `.github/skills/`, `.claude/skills/` | `~/.agents/skills/`, `~/.copilot/skills/` |
| Codex | `.codex/skills/` | `$CODEX_HOME/skills/` (commonly `~/.codex/skills/`) |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

Discovery and activation behavior evolves; consult current client documentation. The Skill itself does not require a particular subagent system, tool name, or GitHub API.

## Use

Repository-wide audit:

```text
Use full-spectrum-review to perform a comprehensive audit of this repository.
Reconstruct important mechanisms from first principles, load all applicable Domain Packs, and — when the target is large and the harness supports workers/subagents — execute bounded Audit Units in parallel; otherwise use the same units sequentially. Record honest coverage, centrally verify/deduplicate/rank findings, and persist the canonical report plus audit ledger.
```

For a PR:

```text
Use full-spectrum-review to comprehensively audit PR #123.
Bind to the exact head, cover all materially affected paths, produce a compact canonical report, and request changes if blocking findings exist.
```

## Design principles

- Comprehensive audit is the default; narrow review is an explicit exception.
- Comprehensive means provable coverage, not identical-depth scanning of every file.
- Large targets decompose into bounded subsystem/flow Audit Units; parallelism is an optimization, not a protocol dependency.
- Workers produce candidate evidence; the Lead owns canonical findings, stable IDs, root-cause deduplication, and verdicts.
- Reconstruct the problem before accepting the current solution.
- Separate Necessity from Cost.
- Accidental-complexity claims require active disconfirmation.
- Tests are evidence, not truth.
- Changed lines are a starting point, not the reasoning boundary.
- Severity and confidence are separate.
- Domain knowledge is pluggable; core method does not grow one branch per domain.
- Audits are read-only for the implementation by default.

## References

- Agent Skills open standard: https://agentskills.io/
- Cursor Agent Skills: https://cursor.com/docs/skills
- Gemini CLI Agent Skills: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- GitHub Copilot Agent Skills: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- OpenAI Codex skills: https://github.com/openai/codex/tree/main/.codex/skills
- Claude Skills authoring guidance: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices

## License

MIT
