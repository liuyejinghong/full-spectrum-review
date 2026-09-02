# Business Logic Review Axis

Use this axis to answer: **Does the implemented behavior correctly represent the intended business/domain reality?**

Do not begin by hunting code smells. Reconstruct the domain first. Treat code, tests, documentation, and existing behavior as evidence; none of them is automatically the authoritative definition of correct business behavior.

## Build the business model first

Before publishing findings, reconstruct four internal artifacts when the domain is non-trivial:

1. **Domain glossary** — define the important entities and distinguish concepts that must not be conflated.
2. **Business rule inventory** — explicit and implicit rules the system is expected to enforce.
3. **Invariant ledger** — facts that must always remain true.
4. **Lifecycle/scenario matrix** — expected outcomes across normal, boundary, failure, duplicate, delayed, and recovery scenarios.

Do not publish these artifacts unless useful to the user; use them to reason.

## Core lenses

### Business intent

Ask whether the implementation solves the actual user/business problem rather than merely satisfying a local technical interpretation of the Issue.

Look for missing behavior, scope drift, contradictory requirements, and technically clean implementations of the wrong rule.

### Domain model

Identify the real entities and ownership boundaries. Check whether implementation concepts incorrectly collapse distinct domain concepts or create duplicate meanings.

Typical warning pattern:

```text
intent == request == acknowledgement == execution == final state
```

Those may be separate business facts even when represented by similar data.

### Business-rule completeness

Inventory the rules required for a business operation to be considered complete. Check whether the code enforces only the happy-path subset.

A feature can be locally correct yet business-incomplete when lifecycle, reconciliation, cancellation, expiry, reversal, or operator ownership is missing.

### Business invariants

Derive invariants from the domain rather than from the implementation.

Examples of generic forms:

- one event must not be accounted for twice;
- an object cannot simultaneously have incompatible owners;
- terminal state must not silently become active again;
- authoritative external truth and local derived state must eventually reconcile;
- quantity/value conservation must hold across transitions;
- UNKNOWN must not be silently interpreted as success or failure when the business requires confirmation.

### Lifecycle and state-machine semantics

Review a business entity across its whole lifecycle, not file-by-file.

For every meaningful transition, ask what happens on success, rejection, partial success, timeout, duplicate event, late event, reordered event, crash, restart, cancellation, and manual intervention when those states are reachable.

### Temporal semantics

Ask not only what happened, but **what was knowable at the decision time**.

Separate event time, receive time, decision time, submission time, acknowledgement time, persistence time, and reconciliation time when the domain depends on timing.

Look for future information, stale decisions, wrong ordering assumptions, or behavior that is correct only because tests collapse time.

### Economic and accounting semantics

When the domain moves money, inventory, credits, balances, quotas, or quantities, check conservation, rounding, fees, partial operations, reversals, average cost/basis, and ownership changes.

Treat this like an accounting audit: every change in value or quantity should have an explainable cause.

### External-reality mapping

Do not assume the repository's abstraction accurately models an external service, exchange, payment provider, queue, database, or protocol.

Check whether local statuses and method names are stronger than what the external system actually guarantees.

A local `success` often means only that a request was accepted, not that the desired business outcome completed.

### Cross-feature interaction

Review pairwise and multi-feature combinations when responsibilities overlap.

Examples:

- automation × manual takeover;
- retry × idempotency;
- cancellation × partial completion;
- restart × reconciliation;
- configuration reload × active workflow;
- protection mechanism × cleanup;
- cache × authoritative state.

Two features can each be correct alone and wrong together.

### Failure business semantics

A technically correct exception handler can still implement the wrong business action.

For each important failure, ask what the business-safe next state is. In ambiguous external operations, retry may be wrong until reconciliation proves whether the first operation occurred.

### Mode parity

When the same business exists in multiple modes—simulation/production, offline/online, dry-run/live, batch/realtime—compare semantics rather than shared source code.

Check timing, pricing/input assumptions, fees/costs, partial operations, rejection behavior, ordering, and state transitions.

### Counterfactual scenarios

Construct realistic scenarios and compare expected business outcome with actual implementation outcome.

Useful scenario classes include normal completion, partial completion, timeout with unknown external outcome, rejection, duplicate delivery, reordering, crash at a state boundary, restart, stale input, missing input, manual intervention, and recovery.

## Business finding bar

A publishable finding should state:

1. the business rule or invariant that should hold;
2. the realistic scenario that exercises it;
3. the implementation behavior;
4. the mismatch between expected and actual behavior;
5. the concrete consequence.

Do not report disagreements that are merely alternative product designs unless the repository/specification establishes which behavior is required.
