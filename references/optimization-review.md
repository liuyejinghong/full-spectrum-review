# Optimization & Simplification Review Axis

Use this axis to answer: **Can the system become smaller, faster, cheaper, simpler, and more stable without changing required behavior?**

The default preference is **behavior-preserving simplification**. Do not add machinery unless the net system becomes clearly simpler or more efficient.

## Core principle

Optimization is broader than micro-performance tuning.

The highest-value opportunities often come from reducing:

- code paths;
- duplicated responsibility;
- duplicated state;
- synchronization points;
- retries/fallbacks/watchdogs that compensate for a confused ownership model;
- unnecessary abstractions;
- repeated I/O or network work;
- runtime resource growth.

A deleted source of truth can improve performance and reliability more than a faster data structure.

## Core lenses

### Redundant code and responsibility

Look for duplicated logic, repeated validation, copied transformations, parallel implementations of the same rule, and multiple components that believe they own the same responsibility.

Prefer one clear owner over several synchronized copies.

### State reduction

Inventory copies of important state and ask which are authoritative, derived, cached, persisted, or merely convenient.

Repeated state creates synchronization and recovery complexity. If a value can be derived cheaply and reliably, storing another mutable copy may be negative value.

Do not recommend deleting state until the former responsibility and recovery semantics are accounted for.

### Over-engineering and indirection

Look for abstractions, wrappers, factories, strategy layers, compatibility shims, feature flags, adapters, generic frameworks, and configuration knobs that have no current consumer or do not reduce total complexity.

Judge net complexity, not number of classes or functions.

### Dead weight

Find dead code, unreachable branches, obsolete compatibility paths, unused configuration, stale fallbacks, redundant migrations, duplicate helper layers, and tests that exist only for behavior no longer reachable.

Require evidence before deletion.

### Hot-path performance

Inspect actual hot paths for algorithmic complexity, excessive allocation/cloning, repeated parsing/serialization, redundant conversions, avoidable sorting/scanning, lock contention, unnecessary context switching, and expensive operations inside tight loops.

Prefer structural wins over tiny instruction-level changes.

### I/O and network efficiency

Find repeated reads, duplicate API calls, serial independent requests, over-fetching, chatty protocols, repeated metadata queries, unnecessary fsync/write cycles, and opportunities for safe batching or caching.

Do not introduce caches unless invalidation and ownership are simpler than the cost they remove.

### Concurrency efficiency

Check whether concurrency creates useful throughput or only coordination overhead.

Look for excessive tasks, oversubscription, lock contention, queue handoffs, sequential bottlenecks hidden behind async syntax, and concurrency where batching or a single owner would be simpler.

### Memory and resource efficiency

Inspect unbounded queues, caches, buffers, histories, task registries, connections, descriptors, and retained objects.

For long-running services, distinguish temporary peak use from monotonic growth or backlog accumulation.

### Dependency and configuration reduction

Ask whether a dependency is justified by the functionality it provides and whether its lifecycle/security/build cost outweighs a small local implementation.

Likewise, remove knobs that expose no meaningful supported choice and create extra state combinations.

### Recovery-path simplification

Complex reliability machinery can itself reduce reliability.

Look for stacks such as retry + fallback + cleanup + watchdog + reconciliation where a simpler ownership or authoritative-state model could eliminate layers.

Prefer explicit authority, bounded retry, and clear reconciliation over several components correcting one another.

### Operational efficiency

Review startup, shutdown, deployment, rollback, configuration reload, diagnostics, and operator actions for unnecessary steps or duplicated mechanisms.

Simpler operational paths reduce incident surface.

### Cost efficiency

Where external APIs, model calls, storage, compute, database operations, or egress have material cost, look for duplicate work, missing batching, unnecessary precision/frequency, and repeated derivation that can be safely reused.

### Complexity-induced instability

Ask whether bugs are being patched by adding more state and more guards around a fundamentally unclear model.

High-value optimization can be deleting entire correction layers after clarifying ownership and lifecycle.

## Behavior-preservation proof

For every meaningful recommendation, establish:

1. **Current mechanism** — what exists and what responsibility it serves.
2. **Waste/complexity mechanism** — why it is unnecessarily expensive or complicated.
3. **Simpler mechanism** — the proposed reduced design.
4. **Responsibility transfer** — who performs every still-required responsibility after simplification.
5. **Behavior equivalence** — which invariants and externally visible behaviors remain unchanged.
6. **Benefit** — deleted code/state, lower asymptotic or measured cost, fewer failure paths, lower resource use, or simpler operations.
7. **Regression risk** — what tests or measurements are needed before adopting it.

If responsibility transfer or behavior equivalence cannot be explained, do not recommend deletion as safe.

## Avoid low-value optimization findings

Do not report:

- style-only refactors;
- tiny allocation or syntax changes with no meaningful workload;
- speculative scale work unsupported by expected usage;
- caches whose invalidation is harder than the saved work;
- abstractions added merely to make code look cleaner;
- simplifications that erase real failure, recovery, compatibility, or business semantics;
- performance claims without a mechanism or plausible workload.

## Recommendation priority

Prefer, in order:

1. eliminate unnecessary responsibility/state/path;
2. remove duplicate work;
3. simplify ownership and recovery;
4. reduce algorithmic/I/O/resource cost;
5. tune implementation details only when the preceding layers are already sound.

The best optimization finding may be: **this subsystem can safely disappear.**
