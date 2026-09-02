# Full-Spectrum Review

> A model-neutral Agent Skill for **comprehensive software audits**: reconstruct requirements from first principles, then review engineering correctness, business logic, architecture, reliability, performance, and complexity, and consolidate verified findings into a prioritized persistent report.

[简体中文](README.md) · **English**

## What it does

A normal invocation means a **full audit**. The user does not need to manually select review modes.

The Skill first asks what the system actually needs to accomplish and derives the **minimum sufficient mechanism** from real requirements, constraints, and invariants. Only then does it compare that model with the current implementation and continue through engineering, business, reliability, performance, and simplification lenses.

```text
understand real requirements + constraints
        ↓
first-principles minimum sufficient mechanism
        ↓
compare against current architecture / state / patch layers
        ↓
engineering + business + reliability + performance audit
        ↓
high-recall candidate generation
        ↓
evidence verification + root-cause deduplication
        ↓
P0 / P1 / P2 / P3 prioritization
        ↓
persistent full audit report
```

## First-principles review

Before accepting an important subsystem's current design as necessary, the reviewer reconstructs:

1. required externally meaningful outcome;
2. irreducible business/external/concurrency/recovery/performance/compatibility constraints;
3. invariants any valid implementation must preserve;
4. the minimum sufficient conceptual mechanism.

Then it challenges extra state, owners, workers, queues, caches, retries, fallbacks, watchdogs, wrappers, abstractions, compatibility layers, and configuration branches by asking which **current independent requirement** each one satisfies.

If the same current requirements can be satisfied by a materially simpler mechanism, and the extra layers carry no independent requirement while increasing state space, synchronization, failure paths, operational burden, resource cost, or maintenance risk, the difference can be reported as an **Accidental Complexity** finding even when no current bug is reproduced.

This is not code-golf minimalism. Real business, concurrency, failure, compatibility, and performance semantics may require substantial complexity. Simplification is valid only when all required responsibilities and invariants remain preserved.

See [`references/first-principles-review.md`](references/first-principles-review.md).

## Coverage

As applicable, a full audit covers:

- first-principles reconstruction and accidental complexity;
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

The final result is **one coherent audit**, not separate mini-reviews.

## Canonical deliverable

A complete audit produces a reusable Markdown report containing audit metadata, executive summary, priority overview, recommended remediation order, detailed P0/P1/P2/P3 findings, important keep-as-is strengths, verification gaps, and evidence.

Supported finding classes include defects, business-semantic issues, reliability problems, performance problems, optimization opportunities, maintainability/security/test gaps, and **Accidental Complexity**.

For accidental-complexity findings, the report should show:

```text
Required outcome
Irreducible constraints / invariants
Minimum sufficient mechanism
Current mechanism
Accidental complexity delta
Simplification direction
Behavior-preservation plan
```

When repository writes are available and authorized, the report follows an existing project convention or defaults to:

```text
docs/reviews/<YYYY-MM-DD>-full-spectrum-review.md
```

For a PR:

```text
docs/reviews/pr-<number>-<short-head>-full-spectrum-review.md
```

## Priority model

| Priority | Meaning |
|---|---|
| **P0 Critical** | Catastrophic loss/corruption, systemic compromise, unrecoverable production state |
| **P1 High** | Realistic major correctness, business, state, recovery, security, performance, or production risk; severe accidental complexity may qualify when it materially obscures ownership/safety on a core path |
| **P2 Medium** | Real defect, significant weakness, meaningful optimization, or material accidental complexity that increases failure/state/operational/maintenance cost |
| **P3 Low** | Concrete non-blocking improvement with limited impact |

The report also provides a **Recommended Execution Order** so root-cause and ownership corrections come before dependent symptom patches.

## Layout

```text
full-spectrum-review/
├── SKILL.md
├── README.md
├── README.en.md
├── LICENSE
├── ACKNOWLEDGEMENTS.md
└── references/
    ├── first-principles-review.md
    ├── engineering-review.md
    ├── business-logic-review.md
    ├── optimization-review.md
    ├── finding-protocol.md
    ├── reporting-protocol.md
    └── trading-domain.md
```

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
Reconstruct important features from first principles instead of assuming the current architecture is necessary. Review engineering correctness, business logic, architecture, performance, reliability, and simplification opportunities. Verify and rank findings P0/P1/P2/P3, then persist the complete audit report in the repository.
```

For a PR:

```text
Use full-spectrum-review to comprehensively audit PR #123.
Bind the audit to the exact head, challenge unnecessary complexity from first principles, inspect affected call chains and business behavior, rank all verified findings by priority, persist the canonical audit report, and request changes if blocking findings exist.
```

## Domain packs

`references/trading-domain.md` adds trading and real-money semantics such as market-data timing, look-ahead, backtest/live parity, order lifecycle, partial fills, unknown outcomes, position truth, reconciliation, precision, accounting, protection orders, and operator takeover.

## License

MIT
