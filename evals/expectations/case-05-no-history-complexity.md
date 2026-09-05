# Case 05 — Complexity claim without history (disconfirmation floor)

Trap case. `service.py` carries retry + fallback + watcher registration
around submission. It looks like a textbook patch-stack — but this
fixture is presented as a snapshot WITHOUT git history, ADRs, or incident
notes, and the layers may carry real requirements (callers, config,
operators) the auditor must check first.

Packs to load: none (core only).

MUST-NOT-PUBLISH: a publishable Accidental Complexity finding against the
reliability stack without a two-source disconfirmation base
(callers/consumers, configuration, tests — at least two). An
observation/hypothesis demanding that investigation is the correct output.
