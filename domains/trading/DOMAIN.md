---
domain: trading
version: 2
applies-when:
  - system consumes market data or generates trading signals
  - system submits, manages, cancels, reconciles, or accounts for orders and positions
  - system performs backtest, simulation, paper trading, or live trading
  - system manages real-money trading risk or operator takeover
extends: core
last-verified: 2026-09-02
---

# Trading Domain Pack

Use this pack for exchange/broker trading systems, including systematic/quant trading and real-money execution.

This pack supplies **trading-specific facts and scenarios**. Generic retry, concurrency, evidence, priority, First-Principles, and reporting rules remain owned by core.

## Domain Glossary

Keep these concepts distinct when they exist in the target:

- **Market event / candle** — observed market data, with event/exchange time and local receive/decision time.
- **Signal** — strategy conclusion; not an order or position.
- **Intent** — desired trading action after strategy/risk/business decisions.
- **Order request** — outbound request submitted to an exchange/broker.
- **Acknowledgement / exchange order** — external system accepted/identified an order; not necessarily filled.
- **Execution / fill** — actual quantity traded.
- **Trade/accounting event** — economic consequence derived from fills/fees/funding/etc.
- **Position** — current exposure after executions/reconciliation.
- **Protection order** — stop/take-profit/risk order whose existence/state may differ from the main position.
- **Account state** — balance, margin, leverage, mode, and other account-level facts that constrain positions/orders.

Do not collapse signal → request → acknowledgement → fill → position into one status chain unless the external/business semantics genuinely make them identical.

## Domain Invariants

Adapt these to the target's actual venue/strategy, but challenge violations explicitly:

- Decisions may only use market information knowable at the decision time; incomplete/future bars/events must not leak into a closed-bar strategy.
- The same logical signal/event must not create duplicate economic action unless repetition is explicitly intended.
- Request acceptance is not execution; filled quantity and position truth come from executions/reconciliation, not requested quantity alone.
- An uncertain external order outcome is not equivalent to rejection or absence. Unsafe resubmission requires reconciliation against venue truth.
- Every fill/economic event is accounted for exactly once.
- Closed/reduced quantity must not exceed the actual open exposure the system is authorized to close.
- Local position/protection state must not silently outrank authoritative venue/account state when the venue is the actual execution authority.
- Automation must not resume control while ownership, position, or required protection is materially uncertain.
- One real position/account action must not have conflicting active automation/operator owners.
- Balance/equity/PnL changes must be attributable to executions, fees, funding, transfers, adjustments, or other explicit economic events.
- Required protection is not considered present merely because local state says it was requested.

## External Semantics

Trading venues differ materially. Review the **actual provider contract** for the target rather than assuming one exchange's behavior is universal.

Verify as applicable:

- order acknowledgement, execution, cancellation, amend/replace, and terminal-status semantics;
- whether cancel success can coexist with prior/late partial fills;
- idempotency/client-order identifiers and duplicate-submit behavior;
- websocket/event ordering, duplication, gaps, reconnect/replay, and REST reconciliation semantics;
- precision/tick/step/minimum quantity/notional and rounding behavior;
- position mode, margin mode, leverage, liquidation, and risk-tier semantics;
- order flags such as reduce-only/close-position/post-only and time-in-force;
- stop/trigger semantics, including which price source triggers an order when the venue exposes alternatives;
- account/server timestamp windows or signing-time requirements;
- rate-limit weights/order limits, throttling responses, and temporary bans;
- symbol status, maintenance windows, delisting/expiry/contract lifecycle;
- fee, funding, rebate, settlement, and account-balance semantics.

A local abstraction must not claim guarantees stronger than the governing venue contract.

## Market-Data & Temporal Scenario Sweep

Check realistic paths such as:

- incomplete candle/event arrives before close/finality;
- delayed or missing candle/event;
- duplicate/out-of-order market event;
- exchange time vs local receive time drift;
- restart/backfill around a decision boundary;
- backtest data exposes information that live code would not yet know;
- strategy acts twice on the same logical close/event.

For closed-bar strategies, explicitly verify how "closed" is established and how late corrections are handled.

## Order / Execution Scenario Sweep

Exercise as applicable:

- normal full fill;
- partial fill then cancel of remainder;
- submit timeout where the venue actually accepted the order;
- rejection before an external order exists;
- duplicate submission/client-order identifier collision;
- cancel acknowledgement followed by/including a fill race;
- amend/replace race;
- reconnect with missed execution events;
- crash before/after local persistence at acknowledgement/fill boundaries;
- stale local order state after restart;
- reconciliation discovers an external order/position absent locally.

Core rule instantiated here: **unknown external side effect requires reconciliation before an unsafe retry**.

## Position, Ownership & Recovery Scenario Sweep

Check:

- partial fills producing actual position quantity;
- manual/operator trade while automation is active;
- automation takeover/resume after manual ownership;
- multiple application instances/processes acting on the same account/symbol/position;
- local position differs from venue position after outage/restart;
- one-way vs hedge/dual-side modes where applicable;
- reversal/flip behavior and close-vs-open semantics;
- restart while a protection order is missing/unknown;
- reconciliation that finds external exposure with no valid internal owner.

Fail closed when the supported real-money workflow cannot establish safe ownership/exposure/protection state.

## Exchange Mechanics

Do not treat these as provider-independent parameter names; treat them as **questions the reviewer must resolve against the actual venue**:

### Rate limits and availability

Can ordinary bursts, recovery storms, polling, or order-management loops exceed venue request/order limits? What happens after throttling or temporary bans, especially when the next required action is a protective/cancel order?

### Time/signature windows

If authenticated requests depend on server time, nonce, sequence, or receive windows, verify clock synchronization, retry classification, and error handling. A time-window rejection must not be mistaken for network uncertainty without evidence.

### Order flags and trigger semantics

Verify close/reduce-only semantics, post-only behavior, time-in-force, conditional-order activation, and trigger-price source where configurable. A "stop" abstraction is incomplete if the venue supports materially different trigger semantics that affect risk.

### Position and margin modes

Verify account/position-side assumptions, isolated/cross or analogous margin behavior, leverage/risk tiers, liquidation interactions, and provider-specific auto-deleveraging/insurance behavior where relevant.

### Instrument lifecycle

Long-running systems must handle non-trading status, maintenance, symbol metadata change, contract expiry/delivery/delisting, and precision/filter changes where supported by the venue.

## Account-Level Safety

Review trading-specific trust/ownership facts without turning the core into a generic security paper:

- API credentials should have only the permissions required by supported operation; unnecessary withdrawal/admin scope materially changes incident impact.
- IP/account restrictions and key rotation/revocation behavior matter when they affect trading availability/recovery.
- Multiple live instances operating the same account must have an explicit ownership/arbitration model; "each process is locally correct" is not sufficient.
- Account-level configuration (position mode, margin mode, leverage/risk settings) must be verified rather than assumed when it changes order semantics.

## Backtest / Simulation / Live Parity

Compare semantics, not merely code reuse:

- decision timing and market-data finality;
- fill/partial-fill/rejection assumptions;
- fees, funding, rebates, slippage, spread, latency where material;
- precision/minimum-order constraints;
- order-type/trigger semantics;
- cancellation/replacement behavior;
- position/margin constraints;
- restart/reconciliation and missing-data behavior.

A backtest can be internally correct yet business-invalid if it assumes information or executions unavailable live.

## Accounting & Conservation

Check:

- realized vs unrealized PnL;
- fees/rebates and funding/financing;
- average entry/cost basis after partial increase/reduce/reversal;
- duplicate/missing fill accounting;
- rounding/precision effects;
- transfers/adjustments if account equity is reconciled;
- consistency between execution history, position, balance, and reported PnL.

Do not infer economic truth solely from requested order quantity.

## Protection & Risk Controls

For stops, take-profit, liquidation protection, exposure limits, kill switches, or equivalent controls, verify the external truth needed to claim protection exists.

Scenario sweep should include protection placement failure, unknown result, partial position change, cancel/replace race, restart/outage, and operator takeover.

## Severity Context

Trading systems may move real money, so ordinary software defects can have asymmetric impact. Raise severity only when the mechanism actually reaches money/exposure/protection/ownership risk; do not label every trading bug P1/P0 merely because money exists somewhere in the system.

Uncertain real-money order/position/protection state on a reachable production path is generally more serious than the same state ambiguity in a read-only analytics component.

## Out of Scope / Core Boundary

This pack does not redefine:

- generic concurrency/idempotency/retry correctness;
- core finding priority/confidence/status;
- general security hardening;
- generic performance optimization;
- report structure or evidence bar.

It supplies trading instances of those concerns. If the target also has substantial distributed-systems, accounting, security, database, or AI-agent behavior and matching packs are available, load them alongside this pack rather than expanding trading into a catch-all.