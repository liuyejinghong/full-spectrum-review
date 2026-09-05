---
domain: trading
version: 5
applies-when:
  - system consumes market data or generates trading signals
  - system submits, manages, cancels, reconciles, or accounts for orders and positions
  - system performs backtest, simulation, paper trading, or live trading
  - system manages real-money trading risk or operator takeover
extends: core
last-verified: 2026-09-05
---

# Trading Domain Pack

Use this pack for exchange/broker trading systems, including systematic/quant trading and real-money execution.

This pack supplies **trading-specific facts and scenarios**. Generic retry, concurrency, evidence, priority, First-Principles, and reporting rules remain owned by core.

This pack is distilled review experience from three source types — production incident postmortems of live trading systems (silent data-chain freezes, protection churn loops, rollback incidents, cross-endpoint misreads), regulatory control categories for algorithmic trading (translated into review questions, obligation-scoped), and reference-implementation convergence across mature open-source trading platforms — generalized without referencing any deployment. It is high-value experience to check, **not universal law**: every statement is a verify/challenge question that has been true often enough, and cost enough, to be worth asking on every audit. A target may have a legitimate, evidenced reason to differ — when it does, record the reasoning instead of forcing compliance. Statements conditioned on features the target does not have (runners, tiered exits, release machinery, a notification pipeline) simply do not apply. Where this pack conflicts with the actual venue contract or the target's evidenced business requirements, those win and the conflict is recorded. Most statements assume a system that holds positions over time, manages protection orders, restarts, and reconciles against a venue.

## Domain Glossary

Keep these concepts distinct when they exist in the target:

- **Market event / candle** — observed market data, with event/exchange time and local receive/decision time.
- **Signal** — strategy conclusion; not an order or position.
- **Intent** — desired trading action after strategy/risk/business decisions.
- **Business obligation** — the economic result the system owes (reduce a fixed fraction, preserve a runner, maintain full stop coverage); it is discharged by facts, not by placing any single order.
- **Mechanism** — the disposable means used to discharge an obligation (maker, market compensation, bridge stop, retry); replacing a mechanism must not create a second obligation.
- **Order request** — outbound request submitted to an exchange/broker.
- **Acknowledgement / exchange order** — external system accepted/identified an order; not necessarily filled.
- **Execution / fill** — actual quantity traded.
- **Trade/accounting event** — economic consequence derived from fills/fees/funding/etc.
- **Position** — current exposure after executions/reconciliation.
- **Protection order** — stop/take-profit/risk order whose existence/state may differ from the main position.
- **Canonical proof** — the durable, restart-surviving record that a specific obligation was discharged by specific exchange facts; distinct from exchange coverage itself.
- **Runner** — an economic identity (origin cycle + entry basis + preserved quantity + exit policy), not "a small residual position".
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
- Exit facts and entry candidates are independent intents: a pending/unconfirmed entry must never suppress an already-satisfied exit; a reverse executes as close → confirmed flat → open, aborting the new leg if the close fails.
- No anonymous irreversible action: every system-initiated order/flatten carries a durable identity tying it to the position/trade it serves, minted before POST — otherwise fills cannot be attributed to the intent that caused them and obligations cannot be closed.
- Every computable exit obligation has a durable intent/order before its trigger can be crossed; absence of intent at a crossed target is itself a defect, not a market event.
- Missing canonical proof is not missing exchange protection: it must not automatically trigger a second emergency order. Verify actual venue coverage across all system stops before replacing.
- "Risk handled" is not "trade succeeded": outcome models distinguish confirmed-executed / aborted-flat / deferred-protected / failed-unknown.
- Protection maintenance and reduce-only exits keep running in degraded and partial-fault states; entry capability is what the fault gates. Model restricted states as per-action capability sets, not one mode-equality gate.
- A signal consumed without execution is a visible, repairable lifecycle event — replay/state must not advance past an entry that never executed.
- Every reconcile blocker has an owner-mediated clear path once fresh matching facts arrive; irremovable blockers manufacture churn loops.
- Restoring an older local snapshot is valid only while the venue-side world (position, protection, fills) provably still matches it; any exchange-side progress since the snapshot forbids blind restore — reconcile forward against current venue truth instead.
- An absent recovery plan or unknown ownership means observe-only: never interpret the absence as "expected zero protection" and cancel real venue stops.
- Threshold-crossing states (protection upgrades, milestones) must be reconstructable from position-period history, not only from live observation — a missed live window must not lose the fact forever.

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
- fee, funding, rebate, settlement, and account-balance semantics;
- the **enforcement boundary** of rate limits and bans (e.g., egress IP) versus the system's instance/container boundary — processes sharing an egress boundary must share one backoff state and request budget, and a rate-limit warning is a stop signal: continuing converts it into an escalating ban;
- exclusivity constraints on same-direction close-position orders: replacement needs deterministic bridge-cancel-place sequencing and must tolerate the transient old+new overlap window with same-operation resume;
- representation semantics on read-back: an omitted field may be normalized to a default, `quantity=0` may mean full coverage, and a 200-level envelope may still carry a business failure code;
- economic values reported by different endpoints (order avgPrice vs position entryPrice) must be precision-normalized before comparison — exact float equality across endpoints reclassifies your own position as external drift;
- the signature input must be byte-identical to the transmitted body: one serialization feeds both signing and dispatch, boolean/number formatting included;
- every venue rejection is logged with the authoritative error code and response body — transport status alone is unattributable;
- rate-limit budgets reflect endpoint weights in one shared, weighted pool per enforcement boundary — reference platforms converge on weighted rate pools owned by the exchange-client layer; per-call-site counters and per-instance backoff are the known failure shape;
- on startup, live systems fetch existing open orders and positions from the venue before making any decision — reference implementations converge on startup reconciliation rather than assuming an empty world.

A local abstraction must not claim guarantees stronger than the governing venue contract.

## Market-Data & Temporal Scenario Sweep

Check realistic paths such as:

- incomplete candle/event arrives before close/finality;
- delayed or missing candle/event;
- duplicate/out-of-order market event;
- exchange time vs local receive time drift;
- restart/backfill around a decision boundary;
- backtest data exposes information that live code would not yet know;
- strategy acts twice on the same logical close/event;
- a completion event fires but the data read for the decision does not yet contain the declared fact — defensive trimming that silently demotes the decision to older data is a systematic one-period lag, not safety;
- an in-flight newer fetch reports lag: it must neither invalidate still-fresh processed data nor consume signals without execution — freshness is judged by what was last successfully processed, not by what was last fetched;
- signal/decision price domain and fill/exit price domain are the same instrument: structural price levels computed on one symbol must never gate or trigger exits on another.

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
- reconciliation discovers an external order/position absent locally;
- a failed order attempt persists a failure/backoff record that gates re-evaluation — absence of an open order alone is never a re-place trigger, and all venue egress funnels through the single client owning the limit/backoff contract;
- every position-conditional order re-confirms the venue position at submit time: if the position is gone, clear local state and abort;
- a fast market gaps through a fixed target: verify the obligation already had a durable intent, and that an already-crossed exit abandons maker preference for deterministic reduce-only execution;
- an on-exchange protection order manually cancelled at the venue: the system detects its absence against venue truth and re-places it — protection presence is enforced, not assumed from the last local action (reference convergence).

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
- reconciliation that finds external exposure with no valid internal owner;
- restart/reconnect transient windows are first-class scenarios (lock contention, replay, dual projections) — verify the recovery window, not only steady state;
- startup classifies positions from the authoritative current state, not from a stale secondary view — a legacy or cached projection must not reclassify the system's own position as external;
- a single unbound fill blocks only its own binding — raw fill ingest and notification for subsequent fills continue;
- a protection/emergency incident persists a durable latch that survives restart and blocks new entries until explicitly reopened with fresh evidence;
- healthy and repair paths return the same proof contract: an ok-only snapshot must not be able to downgrade a previously verified state;
- migration/release windows model the real venue events that occur during them — a pre-window snapshot is not terminal truth, and configuration changes apply to future cycles while active cycles keep their frozen contract.

Fail closed when the supported real-money workflow cannot establish safe ownership/exposure/protection state — but scope the closure to the unknown fact, not to the whole system: local uncertainty must not starve unrelated facts, fills, or authorized reduce-only risk reduction.

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
- restart/reconciliation and missing-data behavior;
- unknown config/enum values fail closed in **every** engine — silent fall-through to a default branch in one engine is a parity bug;
- internally expanded representations (step counts, indices, expansion counters) are never used directly as semantic labels in gating, display, or exports;
- adjudicating historical live results requires a time-segmented replay of then-effective config/release/state — a current-parameter rerun of history answers "what would today's strategy have done", not "why did live behave that way"; reports carry their provenance mode;
- the backtest **declares its intra-bar ordering assumption explicitly**; the conservative default is stop-loss before favorable extremes within the same bar. An undeclared assumption is a finding, not a detail (reference convergence on declared conservative ordering);
- backtest and live share one execution interpreter where feasible — reference platforms converge on a shared kernel (event ordering, time handling, execution flow) precisely to eliminate the interpreter-drift failure class; dual research/live engines require an explicit parity contract with shared fixtures;
- live orders are asynchronous while backtest orders complete synchronously — verify code shared between both modes does not assume synchronous fills;
- identical limit orders fill differently in live by queue position — live-vs-backtest comparisons must attribute divergence to fill assumptions, not only to signals;
- composition tests run against a deterministic simulated venue (injectable clock and network, adversarial fills/cancels/rejects) rather than hand-written fakes; leading practice is continuous randomized testing against the deterministic simulator — unit-green components have repeatedly failed at first real composition.
- bar timestamp conventions are traced end to end (ingest loader → wire/parquet → engine input → receipt claim): raw open time, bar close/available time, signal decision time, and fill event time stay distinct, and the receipt's declared convention matches the actual execution-leg wire — a validator or reference-key contract that only covers the signal leg never proves the execution leg's time meaning.

A backtest can be internally correct yet business-invalid if it assumes information or executions unavailable live.

## Accounting & Conservation

Check:

- realized vs unrealized PnL;
- fees/rebates and funding/financing;
- average entry/cost basis after partial increase/reduce/reversal;
- duplicate/missing fill accounting;
- rounding/precision effects;
- transfers/adjustments if account equity is reconciled;
- consistency between execution history, position, balance, and reported PnL;
- residual computations use the intent-frozen quantity as their base, not a snapshot already advanced by the same action.

Do not infer economic truth solely from requested order quantity.

## Protection & Risk Controls

For stops, take-profit, liquidation protection, exposure limits, kill switches, or equivalent controls, verify the external truth needed to claim protection exists.

Scenario sweep should include protection placement failure, unknown result, partial position change, cancel/replace race, restart/outage, and operator takeover.

Additionally:

- a newly placed stop/exit never evaluates against the current bar's pre-establishment extremes — aggregate OHLC carries no intra-bar ordering, and same-bar activation is a real-loss failure mode;
- emergency protection installation first proves insufficient fresh coverage across **all** system stops (not only its own client-order namespace);
- protection validation checks trigger/anchor semantics, not only quantity coverage — an earlier-triggered or over-covering stop is a semantic failure, not a pass;
- an authorized reduce-only de-risk path cannot be blocked by pending strategy obligations or readiness gates: safety gates must distinguish "forbidden to add risk" from "forbidden to reduce risk".

## Pre-Trade Controls & Kill Functionality

Control categories distilled from regulated-market requirements for algorithmic trading (EU RTS 6, US Market Access Rule). The categories are domain truth; the legal obligation is jurisdiction- and role-dependent — most retail/deployments are not bound, but every category below has prevented real loss somewhere and earns its place as a review target:

- an **independent pre-trade guard layer** stands between strategy output and the venue, not bypassable by strategy code and not removable through strategy configuration; reference implementations converge on placing it in the execution-client/risk engine, not in the strategy;
- numeric guardrails verify: price collars (max distance from a reference price), maximum order value/volume, and maximum order/message rate per venue enforcement boundary;
- duplicate and fat-finger prevention at the gate: resubmission of the same identifier/quantity/symbol is blocked, and prices/sizes outside declared bounds are rejected before the venue sees them;
- **kill functionality**: a single operator action cancels all open orders (and optionally flattens), is reachable in degraded states, and whose authority is independent of the strategy process — verify it is exercised in tests, not merely present;
- guard configuration changes require authority separate from strategy deployment (the risk layer holds exclusive control of its own controls);
- protections are periodically exercised against stressed shapes — gaps, one-sided books, repeated rejections — not only normal conditions.

## Notification & Alerting Semantics

Trading systems fail through their observability as much as their order paths — a mislabeled stop or a swallowed fill alert is a risk-decision failure, not a cosmetic one:

- classification derives from persisted machine codes that survive system boundaries; downstream components never parse display text or subjects for semantics — a breakeven stop rendered as a "hard stop" (or the reverse) misprices incident severity during live trading;
- incident identity is a stable typed root plus dimensions — no display strings, batch counts, or time buckets; recovery fires only when all contributing producers recover, so a repeated protection failure is not silently resolved by one component's cooldown;
- alert intents are durably persisted before remote availability; a delivery failure never blocks trading, and provider `sent` is never reported or relied on as inbox delivery — a provider outage must not permanently swallow a terminal fill or protection notification;
- scheduling independence is verified both ways: bulk delivery never gates the next reconcile or market-data advance, and wake/signal coalescing is explicit — a flag set during a blocked window must not silently collapse multiple distinct events into one uncounted wakeup;
- priority capacity is reserved at the point of irreversible consumption: routine notification volume (periodic reports, debug mail) must not exhaust the budget that terminal trade and protection alerts need during an incident;
- automated action notifications carry their rule source, so during operator takeover a strategy auto-action is not mistaken for a manual instruction;
- "process healthy" verdicts derive from the trading chain's most recent progress evidence (last processed fact), not from out-of-band component liveness — a healthcheck that never touches the decision chain can stay green for hours while positions sit unmanaged.

## Severity Context

Trading systems may move real money, so ordinary software defects can have asymmetric impact. Raise severity only when the mechanism actually reaches money/exposure/protection/ownership risk; do not label every trading bug P1/P0 merely because money exists somewhere in the system.

Uncertain real-money order/position/protection state on a reachable production path is generally more serious than the same state ambiguity in a read-only analytics component.

When reading evidence and writing findings, keep these paired claims distinct — each pair has been conflated in a real incident:

- protected ≠ healthy; risk-handled ≠ trade-succeeded; proof-missing ≠ protection-missing;
- quantity reduced ≠ obligation discharged; runner shrunk ≠ runner restored;
- tighter stop ≠ compliant stop (trigger semantics, not only coverage);
- verified in-process ≠ verified durable across restart;
- notification sent ≠ delivered; access=full ≠ able to open (effective capability is the intersection of persisted access, runtime health, and writer liveness);
- incident discovered-at ≠ started-at;
- unquantified financial impact stays unknown — never conclude "no loss" from a single fill.

## Out of Scope / Core Boundary

This pack does not redefine:

- generic concurrency/idempotency/retry correctness;
- core finding priority/confidence/status;
- general security hardening;
- generic performance optimization;
- report structure or evidence bar;
- incident-remediation process discipline (stop rules, attempt budgets, release governance) — real failure sources, but process rules rather than domain truth.

It supplies trading instances of those concerns. If the target also has substantial distributed-systems, accounting, security, database, or AI-agent behavior and matching packs are available, load them alongside this pack rather than expanding trading into a catch-all.
