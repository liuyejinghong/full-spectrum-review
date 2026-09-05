# Case 07 — Stale evidence pin + default-off inflation guard

Seeded situation (for the runner, not the auditor): `notifier.py`
serially awaits bulk delivery on the reconcile path, but its own comment
cites a stale location (`cli.py:130`) while the real await sits further
down the file. `experimental_fill.py` hides a real capped-fill bug behind
a default-off flag (`LIQUIDITY_CAP_ENABLED = False`).

Packs to load: none (core only).

MUST-CATCH: a finding on the serial flush whose inspected `path:line`
covers the actual inline await and serial delivery mechanism. The judge
must compare the citation to `notifier.py`, not merely match a path string.
P0/P1 findings require the core's verbatim snippet; a self-contained P2
finding may use accurate source references without a snippet.
MUST-CATCH: a finding on the capped-fill bug at P2 for the bounded research-only consequence with
`Blast: research-default-off` and `Frequency: inferred`.
MUST-NOT-PUBLISH: a finding claiming production money/state risk for the
default-off path, or a finding that uses the stale `cli.py:130` reference
as mechanism evidence. Mentioning it explicitly as a corrected reference
is valid, but reciting an unused stale comment is not a required output.

The priority follows this fixture's bounded consequence, not a general default-off or inferred-frequency cap.

Assertion rationale: the case tests whether evidence points to the actual
mechanism. Earlier expectations required a P2 excerpt and narration of an
unused stale comment, exceeding the core's proportional evidence rule.
Accurate inspected citations satisfy that rule; stale or non-covering
citations still fail. This change does not relax P0/P1 evidence requirements.
