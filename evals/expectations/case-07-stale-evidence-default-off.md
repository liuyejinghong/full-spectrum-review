# Case 07 — Stale evidence pin + default-off inflation guard

Seeded situation (for the runner, not the auditor): `notifier.py`
serially awaits bulk delivery on the reconcile path, but its own comment
cites a stale location (`cli.py:130`) while the real await sits further
down the file. `experimental_fill.py` hides a real capped-fill bug behind
a default-off flag (`LIQUIDITY_CAP_ENABLED = False`).

Packs to load: none (core only).

MUST-CATCH: a finding on the serial flush that cites the reopened
`path:line` with a verbatim snippet, and explicitly notes the stale
comment drift instead of repeating it.
MUST-CATCH: a finding on the capped-fill bug at P2 for the bounded research-only consequence with
`Blast: research-default-off` and `Frequency: inferred`.
MUST-NOT-PUBLISH: a finding claiming production money/state risk for the
default-off path, or any finding that repeats the stale `cli.py:130`
reference without reopening the source.

The priority follows this fixture's bounded consequence, not a general default-off or inferred-frequency cap.
