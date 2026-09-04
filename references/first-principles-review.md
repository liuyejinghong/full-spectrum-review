# First-Principles & Accidental-Complexity Review

Use this lens to answer one question:

> **What is the minimum sufficient mechanism required by the current real requirements, and which parts of the current design have no independent reason to exist?**

This is the **Necessity** lens. It decides whether state, ownership, workers, queues, caches, retries, fallbacks, state-machine states, abstractions, compatibility paths, configuration branches, and recovery layers are actually required.

Do not use this lens for ordinary runtime tuning of mechanisms whose necessity is already justified; that belongs to `optimization-review.md`.

## First-principles reconstruction

For each important or structurally non-trivial subsystem/feature, reconstruct the problem before accepting the current solution.

### 1. Required outcome

Describe the externally or operationally meaningful result. Do not define the requirement in terms of existing classes, workers, states, or functions.

### 2. Irreducible constraints

Identify constraints that any valid implementation must respect, such as:

- external API/protocol semantics;
- business rules and accounting/safety invariants;
- concurrency, ordering, persistence, and crash boundaries;
- supported compatibility consumers;
- operator/deployment requirements;
- demonstrated latency/throughput/resource bounds when they genuinely require structure.

A constraint is not irreducible merely because the current implementation assumes it.

### 3. Required invariants

List the facts that every acceptable design must preserve. Examples include one authoritative owner for a mutable fact, no double application of an event, reconciliation of uncertain external outcomes before unsafe retry, and preservation of supported externally visible behavior.

### 4. Minimum sufficient mechanism

Derive the smallest **conceptual** mechanism that satisfies the required outcome, constraints, and invariants.

This is not line-count minimization. The purpose is to expose which responsibilities are truly necessary.

```text
required outcome
+ irreducible constraints
+ required invariants
→ minimum sufficient mechanism
```

### 5. Current mechanism

Map how the repository currently carries the same responsibilities:

- authoritative and derived mutable state;
- owners/components;
- workers/tasks/queues;
- retries/fallbacks/watchdogs/reconcilers;
- caches/registries/snapshots;
- wrappers/adapters/factories/frameworks;
- feature flags/configuration branches;
- compatibility/migration paths;
- cleanup and recovery machinery.

### 6. Necessity challenge

For each layer beyond the minimum mechanism, ask:

- Which **current independent requirement** does it satisfy?
- Which invariant becomes impossible to preserve without it?
- Is the responsibility already carried elsewhere?
- Is the state authoritative, derived, cached, or duplicated convenience state?
- Is a recovery layer repairing failures created by another internal layer?
- Does an abstraction support multiple real variants or only forward one implementation?
- Does a compatibility path still have a supported consumer?
- Does a configuration branch represent a real supported choice?

If no independent requirement survives this challenge, the layer is a candidate for accidental complexity.

## Mandatory disconfirmation attempt

Before publishing an Accidental Complexity finding, actively investigate **why the challenged layer exists**.

Use the evidence available in the current environment, such as:

- git history, blame, introducing commits, or PR discussion;
- ADRs, comments, design docs, incident notes, or issue history;
- tests that name a failure scenario or compatibility requirement;
- current callers, consumers, operators, and configuration;
- external contracts or operational constraints.

Do not require every source above. The obligation is to **seek contrary evidence**, not to mechanically run `git blame`.

When git history is unavailable (snapshot, tarball, external mirror), substitute at least two of callers/consumers, configuration, and tests as the disconfirmation base. If even those cannot be established, the conclusion stays an observation/hypothesis — "no history" never upgrades it to a finding.

Record the result as `Why this layer exists / Disconfirmation attempt` in the finding. If you have not meaningfully investigated the layer's reason for existence, the conclusion is an observation/hypothesis, **not a publishable Accidental Complexity finding**.

Historical origin alone neither proves nor disproves necessity. Determine whether the reason that introduced the layer still corresponds to a current supported requirement.

## High-value challenges

### Patch-stack archaeology

Look for accumulated correction stacks such as:

```text
bug → guard → duplicated state → synchronization → retry → fallback → watchdog → cleanup/reconciliation
```

Do not assume the stack is wrong. Ask whether one upstream ownership/state/lifecycle correction can remove several downstream mechanisms while preserving every real failure semantic.

### State-machine necessity

For each non-trivial state machine, distinguish:

- states representing different real business/external facts;
- states that exist only to coordinate internal implementation;
- transitions required by the real lifecycle;
- transitions that repair inconsistent internal copies.

Do not collapse states that represent genuinely different outcomes merely to reduce state count.

### Ownership and duplicated state

Inventory important mutable facts and their owners. Prefer one authoritative source plus derived views when that satisfies the real requirements. Multiple copies are justified only when their independent responsibility, consistency model, and recovery semantics are explicit.

### Abstraction necessity

An abstraction normally earns its existence by isolating a real boundary, supporting multiple real implementations, enforcing an invariant once, removing meaningful duplication, or serving independent consumers through a stable contract.

A layer that only renames/forwards one implementation may be accidental complexity unless it serves another demonstrated requirement.

### Reliability machinery necessity

Reliability code deserves the same necessity test as feature code. A stack of retry + fallback + watcher + cleanup + reconciliation may be essential, or it may compensate for unclear authority.

A simpler model wins only when it preserves all supported partial-success, timeout, restart, ordering, and external-uncertainty semantics.

### Compatibility, dependency, and configuration necessity

Challenge compatibility shims with no supported consumer, dependencies that exist only to provide trivial local behavior, and configuration knobs that expose no meaningful supported choice.

Do not delete current compatibility or operational requirements just because they make the conceptual model larger.

## From-scratch test

Ask:

> If the same current requirements were implemented today from scratch, with full knowledge of the domain and constraints, would this design still be chosen?

A "no" is only the start of analysis. Explain what would change, which current requirements remain satisfied, and why the extra current layers no longer have independent responsibility.

## Finding threshold

An Accidental Complexity finding does **not** require a reproduced runtime bug, but it must satisfy the canonical finding protocol and additionally prove:

1. the required outcome, constraints, and invariants;
2. a materially simpler sufficient mechanism;
3. the current extra mechanism(s);
4. a concrete cost from the difference, such as state-space growth, synchronization/recovery paths, operational burden, test-matrix expansion, maintenance/change risk, or resource cost;
5. a meaningful disconfirmation attempt;
6. responsibility transfer and behavior preservation after simplification.

Do not publish "this feels over-engineered." Do not treat fewer lines as proof.

Use the canonical schema, priority model, confidence model, and status rules from `finding-protocol.md`; do not redefine them here.

The strongest First-Principles result is often not a rewrite. It is identifying the wrong responsibility boundary so several patches, states, workers, or recovery paths can safely disappear together.