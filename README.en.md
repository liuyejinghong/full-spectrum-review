# Full-Spectrum Review

> A model-neutral Agent Skill for **comprehensive software audits**: engineering correctness, business logic, architecture, reliability, performance, and simplification are reviewed together and consolidated into a prioritized persistent report.

[简体中文](README.md) · **English**

## What it does

A normal invocation means a **full audit**. The user does not need to manually select Engineering, Business Logic, or Optimization modes.

The Skill reconstructs the system and its important business behavior, exercises all applicable review lenses, verifies candidate findings, deduplicates root causes, ranks findings P0 → P1 → P2 → P3, and produces a canonical Markdown audit report.

```text
understand system + domain
        ↓
map architecture / state / critical flows
        ↓
engineering + business + optimization audit
        ↓
high-recall candidate generation
        ↓
evidence verification + root-cause deduplication
        ↓
P0 / P1 / P2 / P3 prioritization
        ↓
persistent full audit report
```

## Coverage

As applicable, a full audit covers:

- engineering correctness and contract propagation;
- business rules, domain models, invariants, and lifecycles;
- architecture, ownership, boundaries, and sources of truth;
- failure, retry, restart, reconciliation, concurrency, and state consistency;
- data integrity, compatibility, configuration, migration, and external semantics;
- CPU, memory, I/O, networking, algorithmic cost, and long-running stability;
- redundancy, duplicated state, over-engineering, dead code, dependency/configuration bloat;
- tests, observability, deployment, rollback, and operability;
- security where real trust boundaries exist;
- optional domain packs.

Engineering, Business Logic, and Optimization remain separate reasoning lenses internally to reduce blind spots. The final result is **one coherent audit**, not three disconnected reports.

## Canonical deliverable

A complete audit must produce a reusable Markdown report containing audit metadata, executive summary, priority overview, recommended remediation order, detailed P0/P1/P2/P3 findings, important keep-as-is strengths, verification gaps, and evidence.

When repository writes are available and authorized, the report follows an existing project convention or defaults to:

```text
docs/reviews/<YYYY-MM-DD>-full-spectrum-review.md
```

For a PR:

```text
docs/reviews/pr-<number>-<short-head>-full-spectrum-review.md
```

Findings are sorted by impact, not by file order or discovery order.

## Priority model

| Priority | Meaning |
|---|---|
| **P0 Critical** | Catastrophic loss/corruption, systemic compromise, unrecoverable production state |
| **P1 High** | Realistic major correctness, business, state, recovery, security, performance, or production failure |
| **P2 Medium** | Real defect, significant weakness, meaningful optimization, or moderate-impact stability/maintenance issue |
| **P3 Low** | Concrete non-blocking improvement with limited impact |

The report also provides a **Recommended Execution Order** so root-cause fixes come before dependent symptom patches.

## Layout

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
    ├── reporting-protocol.md
    └── trading-domain.md
```

The base Skill stays compact while detailed audit knowledge lives in `references/` and is loaded when applicable.

## Install

```bash
# Claude Code — user scope
git clone https://github.com/liuyejinghong/full-spectrum-review.git ~/.claude/skills/full-spectrum-review

# Codex — user scope
git clone https://github.com/liuyejinghong/full-spectrum-review.git ~/.codex/skills/full-spectrum-review
```

Common project-scoped locations include `.claude/skills/`, `.codex/skills/`, `.cursor/skills/`, `.gemini/skills/`, and `.github/skills/`.

## Use

```text
Use full-spectrum-review to perform a comprehensive audit of this repository.
Review engineering correctness, business logic, architecture, performance, reliability, and simplification opportunities. Verify and rank findings P0/P1/P2/P3, then persist the complete audit report in the repository.
```

For a PR:

```text
Use full-spectrum-review to comprehensively audit PR #123.
Bind the audit to the exact head, inspect affected call chains and business behavior, rank all verified findings by priority, persist the canonical audit report, and request changes if blocking findings exist.
```

## Domain packs

`references/trading-domain.md` adds trading and real-money semantics such as market-data timing, look-ahead, backtest/live parity, order lifecycle, partial fills, unknown outcomes, position truth, reconciliation, precision, accounting, protection orders, and operator takeover.

## License

MIT
