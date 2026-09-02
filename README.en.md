# Full-Spectrum Review

> A comprehensive software-audit Skill for AI coding agents: reconstruct what problem the system is actually solving, then judge engineering correctness, business truth, reliability, and cost in one pass — and persist the conclusions as a re-reviewable audit asset, not a read-once review comment.

**Current Core version: `v0.4.0`** · [CHANGELOG](CHANGELOG.md) · [简体中文](README.md) · **English**

## What ordinary AI review misses

Ask an AI to review code and you usually get one of two things: a line-by-line bug hunt over the diff, or a long checklist ticked item by item. Neither answers the more important question:

**The code has no bugs and every test passes — but it is a perfect answer to the wrong question. Now what?**

The expensive defects in real projects are rarely a wrong line of code. They look like this: all that was needed was one authoritative piece of state, but the system grew a cache, a registry, a retry coordinator, a watchdog, a fallback reconciler, and a cleanup worker — six layers patching each other. Or the code faithfully implements a business rule that was misunderstood from day one.

`full-spectrum-review` exists for that layer of review: let a third-party agent that never worked on the project first understand the problem itself, then judge whether the system solves it correctly, necessarily, and sustainably.

## Six core judgments

The rule files are just these six judgments, expanded:

### 1. Reconstruct the problem before accepting the solution

Before judging any important design, the reviewer independently derives the required outcome, the irreducible constraints, and the minimum sufficient mechanism — and only then compares it with what exists. **The current architecture is the answer under review, not the definition of the question.** Even with no known bugs, "six layers grew where one authoritative state would do" can be a formal finding.

### 2. No findings ≠ not reviewed

The report's Coverage Ledger records the actually-achieved depth per area: deep / sampled / not covered / insufficient evidence. A "all clear" report with vague coverage is less trustworthy than a report that says "I could not responsibly conclude on these two areas." "Full" means every materially relevant boundary and flow enters the plan and gets an honest coverage status — not that every file is read at identical depth.

### 3. Audit "should it exist" separately from "is it expensive"

Necessity (the First Principles lens) and Cost (the Optimization lens) are independent questions with independent rules. Mix them and you get the wrong prescription: "it's slow, delete it" or "it's redundant, optimize it." If an optimization investigation reveals a mechanism should not exist at all, the candidate is handed to the Necessity bar instead of spawning a competing rule.

### 4. An over-engineering accusation requires disconfirmation

Before publishing "this layer is over-engineered," the reviewer must actively investigate **why it exists**: commit history, ADRs, tests, callers, operational constraints — looking for contrary evidence that it is justified. The accusation stands only after a meaningful disconfirmation attempt finds no surviving independent requirement; without one, it stays a hypothesis. This is what separates the Skill from review tools that see over-engineering everywhere — preventing agents from over-building and requiring proof before accusing an existing layer are two sides of the same coin.

### 5. Business truth is not the code by default

Code, tests, and documentation are evidence, not automatically the definition of "correct." The reviewer first builds a Business Authority Map for the target: which evidence governs in this domain — external protocols, formal specs, user-facing commitments, or the implementation itself? The ordering differs per domain and is not hard-coded in core. When business intent cannot be established reliably, the report raises an Open Question for the maintainer instead of manufacturing a P1/P2 finding.

### 6. An audit is an asset, not a snapshot

Findings persist under stable IDs (FSR-001, FSR-002, ...) with a lifecycle: OPEN / FIXED / ACCEPTED / SUPERSEDED / REOPENED. A re-review continues from the previous conclusions; priority may change, the ID does not. Design decisions worth preserving are recorded as Keep-As-Is so later agents do not casually "simplify" them away. Repositories without their own audit convention get a lightweight ledger under `docs/reviews/` — deliberately not another Jira.

## What a real finding looks like

(Abridged from the full worked example in [`references/example-finding.md`](references/example-finding.md). Scenario: in a trading system, three components each independently own "is this order submission still pending".)

> **FSR-042 · Duplicate order-recovery ownership** (P1 · Accidental Complexity · Confidence: High)
>
> The business requirement is not three pending states; it is "when the submission outcome is unknown, do not create duplicate economic action." As built, the submitter cache, the pending-order registry, and the recovery watcher each carry their own retry/cleanup transitions, so recovery correctness depends on synchronization between internal copies.
>
> **Disconfirmation:** investigated the introducing commits, restart tests, current callers, and operator recovery docs — the two extra layers came from two historical incident fixes and those requirements are still real; but both can be carried by "one persisted unresolved-intent record + venue reconciliation", and no caller needs independent mutable ownership.
>
> **Direction:** make the persisted unresolved-intent/reconciliation component the sole owner; convert the rest to derived views or remove them; allow bounded retry only after reconciliation proves external absence. Green tests are not a rebuttal — they only prove the three synchronization paths happen to agree today.

One audit pass — high-recall candidates → evidence verification → disconfirmation → cross-boundary verification → root-cause dedup → unified ranking — lands on paper as something like this.

## How it works

A normal invocation is a full audit by default (a narrow review is the explicit exception). Execution shape scales with the target; the protocol and the final artifact do not change:

```text
bind exact target and revision
        ↓
audit plan + coverage ledger
        ↓        small target → one unit, directly
medium/large target → bounded Audit Units by subsystem / business flow
        ↓        parallel workers if the harness has them; same units sequentially otherwise
Shared Audit Brief (behavior-changing facts only) → independent full-spectrum review per unit → Reviewer Packets (candidates)
        ↓
cross-boundary verification → evidence check / disconfirmation → root-cause dedup → P0–P3 ranking
        ↓
one canonical report + a re-reviewable finding ledger
```

The key trade-offs:

- **Decompose by subsystem, not by "engineering / business / optimization"** — the latter forces every agent to re-read the whole repository. Each unit runs all lenses and domain packs inside its scope; ownership and end-to-end business chains get a few cross-cutting units.
- **Share facts, not tentative conclusions** — prevents workers from anchoring each other and from re-deriving the same model.
- **Workers have candidate authority only** — canonical IDs, final priorities, blocking flags, and terminal verdicts are decided centrally by the Lead. A parallel audit never becomes "eight reports stapled together".
- **Context is saved by method, never by word caps** — duplicate reading is eliminated structurally: each module is audited by exactly one unit, cross-boundary code is read-only, and the brief carries only facts that change what some unit inspects or how it reads what it sees. No size budgets anywhere: an admitted fact is never cut for length, and a packet keeps every candidate's evidence intact (any candidate the packet omits is lost with the worker's context) — what gets excluded is process narrative only; a follow-up unit must first name the still-open question it will settle.
- **Domain knowledge is pluggable** — Domain Packs own "the real rules in this domain that cannot be derived from source"; core owns "how to audit". The bundled trading pack covers candle timing semantics, UNKNOWN order outcomes, reconciliation, precision, rate limits, multi-instance ownership, ...; adding payments / accounting packs requires no SKILL.md change.

The final deliverable is one report: metadata and exact revision, coverage ledger, executive summary, findings ranked by priority, recommended execution order, open questions for the maintainer, Keep-As-Is, and evidence gaps — compact for a narrow PR, extensive for a repository-wide audit.

The authoritative rules live in [`references/`](references/) and [`domains/_CONTRACT.md`](domains/_CONTRACT.md); this README is only the tour.

## When to use it — and when not to

**Use it for:** repository-wide audits; merge decisions on important PRs/commits; production-readiness assessments; architecture and ownership reviews; high-stakes domains such as trading (with the matching Domain Pack).

**Do not use it for:** glancing over a two-line change — an ordinary review is enough and the full protocol is a sledgehammer; fixing code directly — this Skill is read-only toward the audited implementation, and fixes are a separately authorized follow-up; replacing tests or CI — it consumes evidence, it does not produce coverage.

Honest boundary: it does not guarantee finding something every time. What it guarantees is that five things are stated clearly: **what was reviewed, what was not, why, what to fix first, and what must not be touched.**

## Install

This repository follows the `SKILL.md` Agent Skills directory format. Prefer the vendor-neutral location when your client supports it:

```bash
git clone https://github.com/liuyejinghong/full-spectrum-review.git .agents/skills/full-spectrum-review
```

Common verified locations:

| Client | Project / workspace | User / global |
|---|---|---|
| Cursor | `.agents/skills/` or `.cursor/skills/` | `~/.agents/skills/` or `~/.cursor/skills/` |
| Gemini CLI | `.agents/skills/` or `.gemini/skills/` | `~/.agents/skills/` or `~/.gemini/skills/` |
| GitHub Copilot | `.agents/skills/` / `.github/skills/` / `.claude/skills/` | `~/.agents/skills/` / `~/.copilot/skills/` |
| Codex | `.codex/skills/` | `$CODEX_HOME/skills/` (commonly `~/.codex/skills/`) |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

Discovery and activation behavior evolves; consult the current client documentation. The Skill itself does not depend on any harness's tool names, subagents, or the GitHub API.

## Use

Repository-wide audit:

```text
Use full-spectrum-review to comprehensively audit this project.
Understand the business and architecture, rebuild key mechanisms from first
principles, and load all applicable Domain Packs. Execute bounded audit units
in parallel when the target is large and the harness supports workers;
otherwise run the same units sequentially. Record honest coverage, centrally
verify/deduplicate/rank findings, and persist the canonical report plus the
audit ledger.
```

PR audit:

```text
Use full-spectrum-review to comprehensively audit PR #123.
Bind the exact head, cover all materially affected paths, and produce a
compact canonical report; return REQUEST_CHANGES if blocking findings exist.
```

## Layout

```text
full-spectrum-review/
├── SKILL.md                 # lean core workflow and contracts
├── VERSION / CHANGELOG.md
├── references/
│   ├── orchestration-protocol.md   # unit decomposition, parallel/sequential, context-saving method
│   ├── first-principles-review.md  # necessity: minimum sufficient mechanism
│   ├── engineering-review.md       # correctness/state/failure/concurrency/compat
│   ├── business-logic-review.md    # business authority map/domain model/lifecycle
│   ├── optimization-review.md      # cost: pricing justified mechanisms
│   ├── finding-protocol.md         # sole authority for types/bar/priority/IDs
│   ├── reporting-protocol.md       # coverage ledger/report/re-review lifecycle
│   └── example-finding.md          # full worked finding
└── domains/
    ├── _CONTRACT.md                # Domain Pack authoring contract (not loaded during audits)
    └── trading/DOMAIN.md           # trading pack v2
```

`SKILL.md` stays lean and details load on demand, so a fixed giant prompt never crowds out the audited code's context.

## Versioning and packs

[`VERSION`](VERSION) is the single source of the current Core version (pre-1.0 SemVer; policy at the top of [CHANGELOG](CHANGELOG.md)). Domain Packs version independently — Core `0.4.0` can ship alongside Trading Pack `v2`, and an audit report records both.

## References

- Agent Skills open standard: https://agentskills.io/
- Cursor Agent Skills: https://cursor.com/docs/skills
- Gemini CLI Agent Skills: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- GitHub Copilot Agent Skills: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- OpenAI Codex skills examples/docs: https://github.com/openai/codex/tree/main/.codex/skills
- Claude Agent Skills authoring guidance: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices

## License

MIT
