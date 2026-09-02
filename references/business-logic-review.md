# Business Logic Review

Use this lens to answer:

> **Does the implemented behavior correctly represent the intended business/domain reality?**

Do not begin by hunting code smells. Reconstruct the domain first. Code, tests, documentation, and existing behavior are evidence; none is automatically the authoritative definition of correct business behavior.

## Build a Business Authority Map

Before publishing material business findings, identify which evidence sources are authoritative **for this target** and why.

Possible sources include:

- external protocols, exchange/provider contracts, laws/standards, or other realities the software cannot redefine;
- explicit product/business specifications and ADRs;
- user-facing commitments/documentation;
- tests that encode intended behavior;
- existing implementation and operational behavior.

Do **not** hard-code one universal ordering across all domains. A protocol implementation, an internal product, and a trading system may have different authority relationships.

Record material conflicts. If only code/tests exist, do not pretend they establish an independent business truth; use them to detect internal inconsistency and compare against any external reality that is available.

If the required intent remains ambiguous, emit an **Open Question for the Maintainer** through `reporting-protocol.md` instead of manufacturing a business finding.

## Reconstruct the business model

For non-trivial domains, build these internal reasoning artifacts:

1. **Domain glossary** — important entities and concepts that must not be conflated.
2. **Business rule inventory** — explicit/implicit rules required for valid behavior.
3. **Invariant ledger** — facts that must remain true.
4. **Lifecycle/scenario matrix** — expected outcomes across normal, boundary, failure, duplicate, delayed, and recovery scenarios.

Publish them only when useful; their primary purpose is to discipline reasoning.

## Core lenses

### Business intent

Ask whether the implementation solves the actual user/business problem rather than a local technical interpretation of an Issue or test.

Look for missing behavior, scope drift, contradictory requirements, and technically clean implementations of the wrong rule.

### Domain model

Identify real entities, ownership, and concept boundaries. Check whether implementation concepts collapse distinct facts or create duplicate meanings.

Typical warning pattern:

```text
intent == request == acknowledgement == execution == final state
```

These may be different business facts even if represented by similar data.

### Business-rule completeness

Inventory what must be true for a business operation to be complete. Check whether the code implements only the happy-path subset while omitting cancellation, expiry, reconciliation, reversal, partial completion, or operator ownership that the domain requires.

### Business invariants

Derive invariants from the authority map/domain rather than from current implementation shape.

Generic forms include:

- one event/value change must not be accounted for twice;
- one business object must not have incompatible active owners;
- terminal state must not silently become active again;
- authoritative external truth and local derived state must reconcile when the domain requires convergence;
- quantity/value conservation must hold across transitions;
- `UNKNOWN` must not silently become success/failure when confirmation is required.

### Lifecycle and state semantics

Review an entity across its whole lifecycle, not file-by-file.

For meaningful transitions, consider success, rejection, partial success, timeout, duplicate/late/reordered event, crash, restart, cancellation, expiry, and manual intervention when reachable.

### Temporal semantics

Ask not only what happened but **what was knowable at decision time**.

Separate event time, receive time, decision time, submission time, acknowledgement time, persistence time, and reconciliation time when timing matters.

Look for future information, stale decisions, wrong ordering assumptions, or tests that accidentally collapse time.

### Economic/accounting semantics

When the domain moves money, inventory, credits, balances, quotas, or quantities, check conservation, rounding, fees, partial operations, reversal, average cost/basis, and ownership changes.

Every value/quantity change should have an explainable business cause.

### External-reality mapping

Do not assume a repository abstraction accurately represents an exchange, payment provider, queue, database, broker, protocol, or other external system.

Local names/statuses may be stronger than the external guarantee. `success` may mean request accepted rather than business outcome completed.

### Cross-feature interaction

Review combinations where responsibilities overlap, for example:

- automation × manual takeover;
- retry × idempotency;
- cancellation × partial completion;
- restart × reconciliation;
- configuration reload × active workflow;
- protection mechanism × cleanup;
- cache × authoritative state.

Two features can each be correct alone and wrong together.

### Failure business semantics

A technically correct exception handler may still choose the wrong business next state.

For important failures, determine the business-safe next state. For uncertain external side effects, retry may be invalid until reconciliation establishes whether the first operation happened.

### Mode parity

When the same business exists in simulation/production, offline/online, dry-run/live, batch/realtime, or similar modes, compare semantics rather than shared source code.

Check timing, input/pricing assumptions, fees/costs, partial operations, rejection behavior, ordering, and state transitions.

### Counterfactual scenarios

Construct realistic scenarios and compare expected business outcome with actual implementation outcome: normal completion, partial completion, unknown external outcome, rejection, duplicate delivery, reordering, crash boundary, restart, stale/missing input, manual intervention, and recovery.

Domain Packs may add domain-specific scenarios and invariants; they do not replace this reasoning method.

## Business finding bar

A publishable business finding must state:

1. the Business Authority Map evidence supporting the rule/invariant;
2. the rule/invariant that should hold;
3. a realistic scenario exercising it;
4. current implementation behavior;
5. the mismatch;
6. the concrete consequence.

Do not publish a mere alternative product design as a defect. When intent is not resolvable from available authority, use an Open Question.

Use canonical type/priority/confidence/status/schema rules from `finding-protocol.md`.