# Full-Spectrum Review

> **English** · [简体中文](README.md)

A model-neutral, open Agent Skill for independent software review.

Instead of giving one reviewer a giant checklist, Full-Spectrum Review separates review into three independent axes:

| Axis | Core question |
|---|---|
| **Engineering Review** | Is the implementation correct, reliable, safe, and well integrated? |
| **Business Logic Audit** | Does the implemented behavior correctly represent the intended domain reality? |
| **Optimization & Simplification Review** | Can the same required behavior be delivered with less code, state, cost, complexity, and failure surface? |

Candidate findings are generated independently, then verified through one evidence protocol and deduplicated by root cause.

## Why three axes?

Different reviewers should be allowed to disagree productively.

An Engineering reviewer may suggest another guard. An Optimization reviewer should be free to ask whether that guard is compensating for duplicated state or confused ownership. A Business reviewer establishes the domain invariant that either design must preserve.

Keeping the axes separate reduces anchoring and makes independent third-party review materially more independent.

## Structure

```text
full-spectrum-review/
├── SKILL.md
├── README.md
├── README.en.md
├── LICENSE
├── ACKNOWLEDGEMENTS.md
└── references/
    ├── engineering-review.md
    ├── business-logic-review.md
    ├── optimization-review.md
    ├── finding-protocol.md
    └── trading-domain.md
```

`SKILL.md` stays intentionally compact. Detailed review guidance lives under `references/` and is loaded only when the selected review axis needs it.

## Install

This repository follows the open Agent Skills `SKILL.md` format. Clone or copy the repository as a skill directory for your client.

Examples:

```bash
# Claude Code — user scope
git clone https://github.com/liuyejinghong/full-spectrum-review.git ~/.claude/skills/full-spectrum-review

# Codex — user scope
git clone https://github.com/liuyejinghong/full-spectrum-review.git ~/.codex/skills/full-spectrum-review
```

Project-scoped locations vary by client. Common locations include `.claude/skills/`, `.codex/skills/`, `.cursor/skills/`, `.gemini/skills/`, and `.github/skills/`.

If your client supports Agent Skills but uses a different discovery path, place this directory at that client's documented skill location.

## Use

### Full review

```text
Use the full-spectrum-review skill to review PR #123.
Run Engineering, Business Logic, and Optimization/Simplification as independent passes, then verify and deduplicate findings. Bind the verdict to the exact PR head.
```

### Business-only audit

```text
Use full-spectrum-review in Business Logic mode.
Reconstruct the domain rules and invariants before judging the implementation. Focus on business-semantic mismatches rather than code style.
```

### Optimization-only audit

```text
Use full-spectrum-review in Optimization & Simplification mode.
Preserve required behavior. Prioritize deleting duplicated state, responsibility, recovery machinery, and redundant work over adding new abstractions or micro-optimizations.
```

### Real-money trading system

```text
Use full-spectrum-review with the trading-domain pack.
Review the exact commit for engineering correctness, business semantics, and behavior-preserving simplification. Treat unknown exchange/order state as something that requires reconciliation rather than an implicit success/failure.
```

## Design principles

- Specialized review passes beat one giant checklist.
- Spec and domain reconstruction come before implementation judgment.
- Candidate generation favors recall; durable findings require evidence.
- Tests are evidence, not proof.
- Changed lines are the starting point, not the reasoning boundary.
- Reachable failures matter; merely constructible hypotheticals do not.
- Optimization must preserve required behavior and account for transferred responsibilities.
- Reducing state and ownership ambiguity can improve reliability more than adding guards.
- PR verdicts should be exact-head-bound whenever the platform exposes the head SHA.
- The number of comments is not a quality metric.

## Domain packs

The core skill is domain-neutral. Optional reference packs can extend it without bloating the base prompt.

The first included pack is:

- `references/trading-domain.md` — market-data timing, backtest/live parity, order lifecycle, partial fills, unknown outcomes, reconciliation, position truth, precision, accounting, protection orders, and operator takeover.

Additional domain packs can be added without changing the three-axis review model.

## License

MIT
