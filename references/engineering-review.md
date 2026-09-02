# Engineering Review Axis

Use this axis to answer: **Does the implementation correctly, safely, and reliably implement its intended contract?**

Do not primarily judge whether the business rule itself is correct; that belongs to the Business Logic axis.

## Core lenses

### Contract and change propagation

Check whether the change satisfies the stated acceptance criteria and whether callers, callees, adapters, schemas, configuration, persistence, and public APIs still agree on the same contract.

Look for local code that is correct in isolation but incompatible with unchanged consumers or producers.

### Functional correctness

Trace real execution paths, including conditions, branching, early returns, mutation, initialization, cleanup, error propagation, and state transitions.

Prefer concrete failure mechanisms over general suspicion.

### Invariants and state machines

Identify technical invariants that must always hold. Examine success, failure, retry, timeout, restart, duplicate events, late events, and reordered events.

### Data integrity

Check loss, duplication, overwrite, stale caches, partial writes, atomicity, transaction boundaries, serialization, precision, rounding, unit conversion, identifiers, and crash boundaries.

Ask what persistent and runtime state looks like if the process dies immediately before or after each important write.

### Failure and recovery

Exercise network timeout, dependency rejection, partial success, rate limiting, malformed response, process crash, shutdown, restart, delayed messages, duplicate retry, and stale responses when reachable.

Look for fail-open behavior, unsafe retries, retry storms, unbounded retries, and partial success interpreted as full success.

### Concurrency and ordering

When threads, async tasks, queues, callbacks, or shared state exist, inspect races, stale reads, lost updates, check-then-act, cancellation, lock ordering, duplicate execution, and shutdown races.

A reproducible race test is useful but not required when a concrete reachable interleaving can be demonstrated.

### Security and trust boundaries

Identify actual untrusted inputs and privilege boundaries before reporting a security finding. Check injection, command execution, authentication, authorization, secret exposure, path handling, unsafe deserialization, permission expansion, and sensitive logging.

Do not report speculative hardening as a vulnerability.

### Performance and resource safety

Inspect real hot paths for accidental quadratic work, repeated parsing/serialization, redundant I/O or network calls, blocking work in async paths, allocation/cloning pressure, memory growth, unbounded queues/caches, task leaks, connection leaks, and file-descriptor leaks.

Only report performance findings when a meaningful workload and impact can be described.

### Compatibility and migration

For public APIs, configuration, persisted data, events, schemas, or CLI changes, check defaults, old data, version skew, upgrade ordering, downgrade/rollback behavior, and missing-field semantics.

### Tests

Map changed behavior to tests. Check happy, negative, failure, boundary, integration, restart/recovery, and concurrency behavior where relevant.

Review the tests themselves: an assertion may validate the wrong thing, a mock may erase the production risk, or expected values may simply reproduce the implementation.

Passing tests are evidence, not proof.

### Observability and operations

For important new failure modes, ask whether an operator can detect, identify, and diagnose the incident from existing logs, metrics, alerts, health checks, and audit context.

Avoid generic requests for more logging.

## Engineering finding bar

A publishable finding should explain:

1. the reachable trigger or execution ordering;
2. the exact implementation mechanism;
3. the concrete impact;
4. why it is in scope for this change;
5. evidence in code, tests, or contract.

If those cannot be stated, keep it as an observation or discard it.
