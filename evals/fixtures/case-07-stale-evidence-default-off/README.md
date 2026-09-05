# Reconciliation and research execution

`notifier.py` runs periodic reconciliation for an active operational tool;
bulk notification delivery may take longer than the reconciliation interval.
Source comments may refer to locations from an earlier layout.

`experimental_fill.py` is a research-only model, disabled by default. Research
callers may enable `LIQUIDITY_CAP_ENABLED`; it is not connected to production.
A take-profit request is complete only after the requested reduction has
executed. A partial fill must leave the outstanding reduction eligible.

No field latency measurements or production-loss evidence are provided.
Domain Packs: none. This is a source snapshot without git history.
