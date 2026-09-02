# Trading / Real-Money Domain Pack

Use this reference in addition to the Business Logic and Engineering axes when the reviewed system can place orders, manage positions, account for money, or influence real capital.

The default safety posture is: **uncertainty about real-money state must not be silently treated as success.**

## Market-data semantics

Check:

- candle open/close semantics;
- incomplete candles;
- event/exchange/receive timestamps;
- UTC/timezone handling;
- missing, duplicate, delayed, stale, or out-of-order market data;
- look-ahead/future-data leakage;
- whether the decision engine uses only information actually knowable at decision time.

## Backtest / simulation / live parity

Compare semantics rather than shared code:

- signal timing;
- price used for decision and execution;
- fee and funding treatment;
- slippage assumptions;
- order rejection;
- partial fills;
- latency/order timing;
- quantity and precision rules.

A strategy can be implemented consistently in code while backtest economics differ materially from live execution.

## Order lifecycle

Distinguish at least where applicable:

```text
signal
intent
order request
request acknowledgement
exchange order
execution/fill
trade/accounting event
position
```

Review NEW/ACK/REJECTED/PARTIALLY_FILLED/FILLED/CANCELED/EXPIRED/UNKNOWN or equivalent states, including duplicate, delayed, missing, and reordered events.

Request acceptance is not equivalent to fill.

Cancellation success is not proof that no quantity filled before cancellation.

## Idempotency and unknown outcomes

A request timeout can mean the exchange accepted the request but the response was lost.

Do not blindly retry order-creating operations when the first result is unknown. Reconcile by stable client/exchange identifiers or another authoritative mechanism before deciding whether resubmission is safe.

## Position truth and reconciliation

Identify the authoritative position source.

Review what happens when:

- local state disagrees with exchange state;
- the process restarts with an open position;
- an order fills while the process is offline;
- websocket/event delivery is incomplete;
- manual activity occurs outside the automation.

Derived local state should converge to authoritative external reality.

## Quantity, precision, and exchange filters

Check:

- tick size;
- step size;
- minimum quantity/notional;
- decimal precision;
- rounding direction;
- leverage and margin constraints;
- conversion between requested, acknowledged, filled, and remaining quantity.

Avoid treating binary floating-point equality as an accounting invariant when exact decimal/filter semantics matter.

## Accounting

Review:

- realized and unrealized PnL;
- commissions;
- funding;
- average entry/basis;
- partial close;
- position reversal;
- duplicate fill accounting;
- quantity/value conservation.

Each monetary or quantity change should be attributable to a real event.

## Risk controls and protection

Review stop-loss, take-profit, exposure limits, circuit breakers, liquidation protection, and emergency shutdown across failure/restart scenarios.

If the system cannot confirm that required protection exists, it must not merely assume protection is active.

## Manual operator takeover

When humans and automation can both act on the same capital, define ownership explicitly.

Review:

- when automation relinquishes control;
- what happens to existing protective orders;
- whether manual and automatic components can issue conflicting actions;
- restart during manual ownership;
- reconciliation and criteria for resuming automation.

## Trading-specific scenario sweep

At minimum, consider realistic cases such as:

- normal entry and exit;
- partial fill followed by cancel;
- submit timeout where the order actually exists;
- duplicate execution event;
- fill after cancel request;
- crash after submit but before persistence;
- crash after fill but before local state update;
- protection-order creation failure;
- network outage and later recovery;
- exchange/local position mismatch;
- missing or delayed candle;
- quantity exactly near exchange precision/minimum boundaries;
- manual takeover of an existing automated position.

For each scenario, compare expected business-safe outcome with actual implementation behavior.
