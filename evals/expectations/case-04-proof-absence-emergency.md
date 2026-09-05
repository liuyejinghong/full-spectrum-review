# Case 04 — Emergency from missing proof (trading pack)

Seeded defect: `guard.py` creates an emergency stop whenever the local
durable proof is absent, without checking actual venue coverage. A missing
record is treated as a missing protection.

Packs to load: trading.

MUST-CATCH: a finding demanding venue-coverage verification before any
replacement order — missing proof is not missing protection.
