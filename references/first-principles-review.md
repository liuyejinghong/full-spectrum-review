# First-Principles & Accidental-Complexity Review

Use this stage to answer a question that ordinary correctness review often misses:

**If the same current requirements had to be implemented today from scratch, with full knowledge of the domain and constraints, what is the minimum sufficient mechanism — and how far has the current implementation drifted from it?**

This stage is mandatory in a full audit. Perform it before accepting the existing architecture, state machine, recovery machinery, or abstraction boundaries as given.

## Purpose

A system can be bug-free today and still be materially wrong as an engineering design because it solves a simple requirement through avoidable state, coordination, patch layers, abstractions, retries, workers, caches, or compatibility machinery.

The goal is not "fewer lines at any cost." The goal is to distinguish:

- **essential complexity** — required by the domain, external contract, concurrency model, failure semantics, scale, compatibility, or other real constraints;
- **justified implementation complexity** — not strictly irreducible, but supported by a demonstrated workload or operational requirement;
- **accidental complexity** — complexity created by historical patches, duplicated ownership, wrong abstractions, defensive layers, obsolete constraints, or local fixes that no longer serve an independent requirement.

## First-principles reconstruction

For each important subsystem or feature, reconstruct the solution independently of the current implementation.

### 1. Required outcome

State the actual externally meaningful result.

Do not describe the current classes, workers, states, or functions. Describe what the system must accomplish for the user/business/runtime.

### 2. Irreducible constraints

Identify constraints that are genuinely non-negotiable, such as:

- external API/protocol guarantees;
- business rules;
- safety or accounting invariants;
- concurrency and ordering realities;
- persistence/crash boundaries;
- latency/throughput/resource requirements;
- compatibility requirements that have real current consumers;
- operator or deployment requirements.

Do not inherit a constraint merely because the code assumes it.

### 3. Required invariants

List the facts that any valid implementation must preserve.

Examples:

- one authoritative owner for a mutable business fact;
- no double application of an event;
- uncertain external outcome must reconcile before unsafe retry;
- required protection survives or is re-established after restart;
- observable behavior remains compatible for supported consumers.

### 4. Minimum sufficient mechanism

Derive the smallest conceptual mechanism that can satisfy the required outcome, constraints, and invariants.

This is not pseudocode golfing. It should be simple enough to expose what responsibilities are truly necessary.

A useful representation is:

```text
required outcome
    +
irreducible constraints
    +
required invariants
    ↓
minimum sufficient mechanism
```

### 5. Current mechanism

Map how the repository actually implements the same responsibility:

- mutable states and sources of truth;
- components/owners;
- workers/tasks/queues;
- retries/fallbacks/watchdogs;
- caches/registries/snapshots;
- wrappers/adapters/factories;
- feature flags/configuration branches;
- recovery/reconciliation/cleanup paths;
- compatibility and migration layers.

### 6. Complexity delta

Compare the minimum sufficient mechanism with the current mechanism.

For every extra layer, ask:

- What independent requirement does this layer satisfy?
- What invariant becomes impossible to preserve if this layer is removed?
- Is the responsibility already satisfied elsewhere?
- Is this state authoritative, derived, cached, or duplicated convenience state?
- Is this recovery layer repairing failures created by another internal layer?
- Is this abstraction used by multiple real variants, or only one implementation?
- Does this compatibility path still have a supported consumer?
- Does this configuration option represent a real supported choice?
- Is the complexity justified by measured workload or only anticipated scale?

If no concrete requirement survives the challenge, treat the layer as a candidate for accidental complexity.

## The from-scratch test

Ask explicitly:

> If we implemented the same current requirements from scratch today, knowing everything we now know, would we still choose this design?

If the answer is no, explain exactly what would be different and why the current extra complexity is no longer justified.

Do not accept "historical reasons" by itself as justification. Identify the current requirement that still makes the history relevant.

## Patch-stack archaeology

Look for patterns where repeated local fixes may have accumulated into a structurally unnecessary subsystem:

```text
bug
→ guard
→ duplicated state
→ synchronization
→ retry
→ fallback
→ watchdog
→ cleanup/reconciliation
```

Do not assume every sequence like this is wrong. Determine whether a simpler ownership, state, or lifecycle model can remove several correction layers while preserving all required behavior.

High-value findings often identify one upstream design correction that makes multiple downstream patches unnecessary.

## State-machine challenge

State machines are sometimes essential and sometimes an artifact of fragmented ownership.

For each non-trivial state machine, ask:

1. Which states correspond to distinct real-world facts?
2. Which states exist only to coordinate implementation internals?
3. Which transitions are required by the external/business lifecycle?
4. Which transitions repair inconsistent local copies?
5. Could fewer authoritative states plus derived views preserve the same semantics?

Do not collapse states that represent genuinely different business or external outcomes merely to reduce count.

## Abstraction challenge

For each abstraction layer, ask whether it reduces total complexity.

A useful abstraction should normally do at least one of the following:

- isolate a real external boundary;
- support multiple real implementations;
- enforce an important invariant in one place;
- remove repeated meaningful logic;
- provide a stable contract across independent consumers.

An abstraction that only renames or forwards one implementation can increase entropy rather than reduce it.

## Reliability-complexity challenge

Reliability machinery deserves special scrutiny because complexity added "for safety" can create new failure modes.

Compare stacks such as:

```text
retry + fallback + watcher + cleanup + reconciliation
```

against simpler models such as:

```text
single authority + explicit UNKNOWN + bounded retry + reconciliation
```

The simpler model wins only if it preserves the same failure semantics and responsibilities.

## Performance and scale challenge

Do not preserve architectural complexity justified only by hypothetical future scale.

Ask:

- What actual workload requires this sharding/cache/queue/batching/concurrency layer?
- Is there benchmark, production evidence, or a credible bound?
- Is the optimization more complex than the cost it removes?

Likewise, do not remove proven performance mechanisms merely because the conceptual minimum is smaller.

## Finding threshold

A First-Principles / Accidental-Complexity finding does **not** require a currently reproduced bug.

It is publishable when you can show:

1. the required behavior and constraints;
2. a materially simpler sufficient mechanism;
3. current layers that do not carry independent requirements;
4. concrete cost from the extra complexity — state-space growth, synchronization, recovery paths, maintenance burden, resource cost, testing burden, or elevated defect risk;
5. a credible simplification direction that preserves behavior.

Do not report "this feels over-engineered" without that comparison.

## Priority

Use impact, not the absence of a current bug, to assign priority.

Typical guidance:

- **P1** may be justified when accidental complexity obscures ownership or safety in a core production/real-money path and materially threatens correct recovery or future changes.
- **P2** is appropriate for significant accidental complexity that materially increases state space, failure surface, operational burden, or development cost.
- **P3** is appropriate for bounded unnecessary indirection or cleanup with limited system impact.

Do not promote aesthetic simplification to P1/P2.

## Detailed finding shape

For this class of finding, include:

```text
Required outcome
Irreducible constraints / invariants
Minimum sufficient mechanism
Current mechanism
Accidental complexity delta
Why the extra layers are not independently required
Impact
Simplification direction
Behavior-preservation / verification plan
```

The strongest result is often not "rewrite this code." It is:

**remove the wrong responsibility boundary so several patches, states, workers, or recovery paths become unnecessary.**
