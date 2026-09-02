# Optimization & Efficiency Review

Use this lens to answer:

> **Given a mechanism whose existence is justified, is its runtime, resource, operational, or external-service cost reasonable for the real workload?**

This is the **Cost** lens. It does not decide whether a subsystem, state, worker, abstraction, compatibility layer, or recovery path should exist at all; that is the responsibility of `first-principles-review.md`.

If an efficiency investigation reveals that the expensive mechanism has no independent requirement, hand the candidate to the First-Principles bar instead of maintaining a duplicate Optimization finding.

## Cost lenses

### Algorithmic and hot-path cost

Inspect real hot paths for:

- avoidable asymptotic cost;
- repeated scanning/sorting/searching;
- redundant parsing/serialization/conversion;
- excessive allocation, copying, cloning, or materialization;
- expensive work inside tight loops;
- repeated derivation of the same result.

Prefer structural wins over instruction-level trivia.

### I/O and network efficiency

Look for repeated reads, duplicate API calls, serial independent requests, over-fetching, chatty protocols, unnecessary fsync/write cycles, repeated metadata queries, and missing safe batching.

A cache is not automatically an optimization. Its ownership and invalidation cost must be lower than the work it removes; whether the cache needs to exist at all is a First-Principles question.

### Concurrency and throughput

Check whether the concurrency model delivers useful throughput for the expected workload.

Look for:

- lock contention;
- unnecessary queue/task handoffs;
- oversubscription;
- sequential bottlenecks hidden behind async syntax;
- head-of-line blocking;
- avoidable context switching;
- work that can safely batch or pipeline;
- synchronization whose cost grows materially with load.

Do not redesign ownership here merely because a different model looks cleaner. Escalate unnecessary ownership/state to First Principles.

### Memory and resource lifecycle

Inspect buffers, queues, caches, histories, registries, connections, descriptors, goroutines/tasks/threads, temporary files, and retained object graphs.

Distinguish:

- bounded steady-state use;
- temporary peak use;
- backlog accumulation;
- monotonic growth/leaks;
- resource exhaustion under supported concurrency.

For long-running services, sustained behavior matters more than short benchmark peaks.

### External-service and monetary cost

Where APIs, model calls, storage, databases, queues, compute, egress, or third-party services have material cost, look for duplicate calls, unnecessary frequency/precision, poor batching, redundant persistence, and expensive work that can be safely reused.

Do not fabricate prices or usage volumes. Tie the finding to a known/credible workload or explicitly state the evidence limitation.

### Operational efficiency

Review startup, shutdown, deployment, rollback, diagnostics, maintenance actions, and recovery operations for excessive latency, repeated work, unnecessary manual steps, or resource-heavy procedures.

Whether an operational mechanism is necessary belongs to First Principles; this lens evaluates its execution cost once justified.

### Long-running stability

Performance failures are often time-dependent. Look for resource growth, queue/backlog amplification, retry storms, repeated full scans, unbounded telemetry/cardinality, or work whose cost compounds across time.

If the root cause is unnecessary retry/recovery ownership rather than execution cost, classify the root finding under First Principles/Reliability rather than duplicating it here.

## Evidence bar

A publishable Performance/Optimization finding must satisfy `finding-protocol.md` and identify:

1. the real or credibly bounded workload;
2. the cost mechanism;
3. why the cost is material to the target;
4. the smallest reasonable efficiency direction;
5. how to measure or verify the improvement without changing required behavior.

Prefer one or more of:

- asymptotic argument tied to real input size;
- profile/trace;
- benchmark;
- measured resource growth;
- repeated expensive operation visible in the execution path;
- documented external-service cost/frequency.

Do not invent benchmark numbers.

## Avoid low-value findings

Do not report:

- syntax or style changes marketed as optimization;
- tiny allocations with no meaningful workload;
- speculative scale requirements unsupported by expected use;
- caches/batching/concurrency whose coordination cost is likely higher than the saved work;
- performance claims without an identifiable mechanism;
- "remove this subsystem" conclusions — route those through First Principles;
- behavior-changing shortcuts disguised as optimization.

Use the canonical schema, priority model, confidence model, and status rules from `finding-protocol.md`.