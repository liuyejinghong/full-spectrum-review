# Domain Pack Contract

Domain Packs extend Full-Spectrum Review with **domain knowledge**, not a second review methodology.

The core Skill owns how audits are planned, how findings are verified/ranked, how First Principles works, and how reports/ledgers are persisted. Packs instantiate that method with vocabulary, invariants, external semantics, and realistic scenarios that a domain-neutral core cannot know.

## Layout

Bundled packs use:

```text
domains/<domain>/DOMAIN.md
```

A project or Agent harness may provide additional private packs outside this repository. They should follow the same contract when possible.

## Required metadata

Each `DOMAIN.md` begins with simple YAML frontmatter:

```yaml
---
domain: payments
version: 1
applies-when:
  - system creates, authorizes, captures, refunds, or reconciles payments
extends: core
last-verified: 2026-09-02
---
```

Fields:

- `domain` — stable domain identifier;
- `version` — pack contract/content version used in audit metadata;
- `applies-when` — human/agent-readable applicability conditions based on real entities, dependencies, external systems, or behavior;
- `extends` — must remain `core`; a pack extends rather than replaces core rules;
- `last-verified` — date the pack's domain guidance was last reviewed against current knowledge/evidence.

Optional metadata may name authoritative references or known overlap, but do not turn metadata into a configuration framework.

## Required sections

### Domain Glossary

Concepts that reviewers must distinguish. Focus on domain terms whose accidental conflation causes wrong behavior.

### Domain Invariants

Facts any valid implementation in this domain must preserve. State business/external truth rather than implementation preference.

### External Semantics

What external systems/protocols can guarantee, what they do **not** guarantee, and which provider-specific contracts the reviewer must verify for the target.

### Scenario Sweep

Realistic normal/failure/recovery/interleaving scenarios that should be exercised during Business/Engineering review.

### Severity Context

Domain facts that can raise/lower the impact of a core finding. This does not redefine P0–P3.

### Out of Scope / Core Boundary

Explicitly state which general rules belong to core so the pack does not copy a parallel finding bar or generic distributed-systems checklist.

## Core vs Pack ownership

### Core owns

- audit workflow and coverage accounting;
- First-Principles method;
- generic engineering/business/cost reasoning;
- canonical finding types, priority, confidence, status, schema;
- evidence/disconfirmation bar;
- root-cause deduplication;
- report and audit-ledger lifecycle.

### Pack owns

- domain vocabulary;
- domain-specific invariants;
- external-domain realities;
- domain-specific scenarios/failure patterns;
- domain-specific severity context;
- pointers to provider/standard contracts that must be checked.

A pack may **instantiate** a core principle using domain language, but should not restate the whole generic rule.

Example:

```text
Core principle:
  uncertain external side effect must not be treated as confirmed absence/presence without reconciliation

Trading instantiation:
  order-submit timeout may mean the exchange accepted the order; reconcile before unsafe resubmit

Payments instantiation:
  authorization timeout may still have created an authorization; query provider state before duplicate charge
```

## Selection

The reviewer inspects all Domain Packs available to the current Skill/harness and loads every pack whose `applies-when` matches the audited target.

Zero, one, or multiple packs are valid. Multi-domain systems are normal, for example:

```text
trading + distributed-systems + accounting
```

Record loaded pack names, versions, and freshness in Audit Metadata.

Do not modify `SKILL.md` merely to register a newly added pack.

## Conflicts and overlap

- Core contracts always win over pack instructions.
- A pack states distilled domain experience, **not universal law**: its statements are high-base-rate verify/challenge questions. Where the target has an evidenced reason to differ, the reasoning is recorded instead of forced compliance; actual external/venue contracts and evidenced business requirements always win over pack assumptions.
- A pack cannot lower the core evidence/finding bar or redefine priority/report schema.
- If two packs surface the same root cause, merge the domain evidence and publish one finding.
- If pack-specific domain facts genuinely conflict and cannot be resolved from authoritative evidence, expose the conflict as an Open Question/evidence limitation rather than silently selecting one.
- Prefer provider/standard contracts that actually govern the audited target over generic pack assumptions.

## Private packs

Organizations may maintain private packs for internal settlement, risk, compliance, protocols, or business rules. The core Skill must remain usable without knowing those packs in advance.

A private pack should be discoverable through whatever skill/project paths the current Agent harness supports; do not require forking this repository or editing the core Skill solely to add private domain knowledge.

## Distilling pack content

Packs are distilled from three source types with different evidentiary characters, plus a shared curation gate.

### From incident postmortems

Each postmortem yields a generalized mechanism (project names, parameters, and version numbers removed), its trigger, a classification, and a verify/challenge phrasing. Test generality by asking whether the clause would still catch the problem in a different stack and at a different scale within the domain.

### From regulatory frameworks

Extract control **categories**, not legal text. Translate each category into a verify/challenge question and state its applicability honestly: the control category is domain truth; the legal obligation is jurisdiction- and role-dependent and travels as a scope note, not as a claim on the target.

### From reference implementations

Extract how mature systems answer a failure class, then phrase it as a comparative question. **Convergence is the evidence**: multiple independent implementations reaching the same design answer earns a clause; a single project's design choice is a reference, never a rule. These clauses remain subject to the experience-not-law framing.

### Shared curation gate

Every candidate clause must pass:

1. **generality test** — holds in a different system in the domain, or is explicitly feature-conditional;
2. **no source-system vocabulary** — plain domain terms only;
3. **experience-not-law framing** — evidenced target deviations are recorded, never forced into compliance;
4. **correct section** per this contract (glossary / invariant / external semantics / scenario / severity), without duplicating core method;
5. **cost evidence** — at least one of: a real incident, a regulatory mandate, or independent reference convergence. Absent all three, it is a preference, not pack content.

## Quality bar for a new pack

A pack is worth adding when it contributes knowledge that a competent domain-neutral software reviewer would not reliably infer from source code alone.

Do not create a pack merely to duplicate generic concurrency, retry, testing, security, or performance advice already owned by core. Domain Packs should increase **domain truth density**, not checklist length.