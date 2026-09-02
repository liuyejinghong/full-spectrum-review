# Full-Spectrum Review

> A model-neutral Agent Skill for **comprehensive software audits**: reconstruct the problem from first principles, audit engineering/business correctness and justified runtime cost, apply relevant Domain Packs, and persist verified findings as a prioritized re-reviewable audit record.

[简体中文](README.md) · **English**

## What it does

A normal invocation means a **full audit of the requested target**. Full does not mean reading every file at identical depth; it means every materially relevant boundary/flow is represented in an Audit Plan and the final Coverage Ledger states what was deeply reviewed, sampled, not covered, or blocked by insufficient evidence.

```text
exact target / revision
→ audit plan + coverage ledger
→ system/domain/ownership/invariants
→ first-principles minimum sufficient mechanism
→ 0..N applicable Domain Packs
→ engineering + business + cost review
→ candidate findings + evidence + disconfirmation
→ root-cause dedup + P0/P1/P2/P3
→ recommended execution order
→ persistent report + stable finding ledger
```

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

Coverage, re-review, Keep-As-Is persistence, and report structure are defined in [`references/reporting-protocol.md`](references/reporting-protocol.md). Canonical finding type/priority/confidence/status/schema are defined only in [`references/finding-protocol.md`](references/finding-protocol.md).

## Read-only audit discipline

Audit authorization is read-only for the audited implementation. Repository write permission authorizes audit artifacts only. Source/config/runtime fixes require a separate explicit follow-up authorization.

## Layout

```text
full-spectrum-review/
├── SKILL.md
├── README.md
├── README.en.md
├── references/
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

Progressive disclosure keeps the core Skill small while loading detailed/domain knowledge only when relevant.

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

Discovery and activation behavior evolves; consult the current client documentation. The Skill itself does not require a particular subagent system, tool name, or GitHub API.

## Use

```text
Use full-spectrum-review to perform a comprehensive audit of this repository.
Reconstruct important mechanisms from first principles, load all applicable Domain Packs, record honest coverage, verify/deduplicate/rank findings, and persist the canonical report plus audit ledger.
```

For a PR:

```text
Use full-spectrum-review to comprehensively audit PR #123.
Bind to the exact head, cover all materially affected paths, produce a compact canonical report, and request changes if blocking findings exist.
```

## References

- Agent Skills open standard: https://agentskills.io/
- Cursor Agent Skills: https://cursor.com/docs/skills
- Gemini CLI Agent Skills: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- GitHub Copilot Agent Skills: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- OpenAI Codex skills: https://github.com/openai/codex/tree/main/.codex/skills
- Claude Skills authoring guidance: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices

## License

MIT
