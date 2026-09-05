# Worked Finding Example

This is a **format/mechanism example**, not a finding about this repository. It demonstrates how a high-impact Accidental Complexity finding should satisfy the canonical protocol without relying on "looks over-engineered" judgment.

````markdown
### FSR-042 — Duplicate order-recovery owners create avoidable state divergence

ID: FSR-042
Priority: P1
Confidence: High
Status: OPEN
Type: Accidental Complexity
Area: Order submission / recovery
Evidence: `execution/submit.*`, `recovery/pending.*`, restart tests, introducing incident fix history
Blocking: yes
Domain-Pack: trading@2

**Problem / Opportunity**

Three components independently own whether an order submission is still pending: the submitter cache, pending-order registry, and recovery watcher. Each has its own retry/cleanup transition. The business requirement is not three pending states; it is to avoid duplicate economic action when submission outcome is unknown.

**Trigger / Workload**

A submit request times out after the venue accepts the order, followed by process restart before the websocket acknowledgement is persisted.

**Mechanism**

The three local owners can recover from different persistence/event evidence. One may mark the request retryable while another still treats it as externally unresolved, so recovery correctness depends on synchronization between internal copies rather than one authoritative uncertainty/reconciliation rule.

**Impact**

On a real-money path this expands restart state space and can make an unsafe resubmit reachable. Even if existing tests currently pass, every future order-state change must keep three owners and their cleanup paths consistent.

**Required outcome**

After an order submission with uncertain outcome, the system must establish external order truth before deciding that resubmission is safe.

**Irreducible constraints / invariants**

- Request timeout does not prove external absence.
- A logical intent must not create duplicate unintended exposure.
- Restart must preserve or reconstruct unresolved external side effects.

**Minimum sufficient mechanism**

```text
single persisted unresolved-intent authority
→ reconcile by venue/client identifier
→ converge to confirmed external state or confirmed absence
→ only then allow safe next action
```

**Current mechanism**

```text
submitter pending cache
+ persisted pending registry
+ recovery watcher state
+ independent retry/cleanup transitions
```

**Accidental complexity delta**

Two mutable ownership copies and their synchronization/cleanup transitions do not carry an independent business invariant once unresolved intent is durably represented and reconciled by one owner.

**Why this layer exists / Disconfirmation attempt**

Investigated the introducing commits, restart tests, current callers, and operator recovery docs. The extra registry/watcher layers were added in two historical fixes for (a) process restart losing in-memory pending orders and (b) websocket acknowledgement gaps. Both requirements remain real, but both can be carried by one durable unresolved-intent record plus venue reconciliation; no current consumer requires independent mutable ownership.

**Recommended direction**

Make the durable unresolved-intent/reconciliation component the sole owner. Convert submitter/watcher state to derived views or remove them. Preserve bounded retry only after reconciliation proves external absence.

**Verification**

Exercise full fill, partial fill, timeout-with-accepted-order, confirmed rejection, crash before/after local persistence, websocket gap, restart, and duplicate client identifier. Assert that one logical intent never produces duplicate unintended exposure and that unresolved state always converges.
````

## Why this example passes the bar

- It identifies a real trigger rather than "too many classes."
- It distinguishes required reliability semantics from accidental internal ownership.
- It actively investigates historical reasons instead of assuming old guards are obsolete.
- It proposes responsibility transfer, not deletion by line count.
- Priority comes from reachable money/state risk; confidence comes from evidence strength.
- The format is detailed because it is P1. A P3 finding should be substantially shorter.
