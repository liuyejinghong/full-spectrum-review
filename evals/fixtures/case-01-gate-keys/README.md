# Case 01 — Gate key table (enumerable-set completeness)

Seeded defect (for the runner, not the auditor): `producer.py` emits 8
economic fields; `gate.py` governs only 6. Two fields (`fee_rebate`,
`funding_adj`) flow to settlement ungoverned.

Packs to load: none (core only).

MUST-CATCH: a finding that enumerates members from the consuming code
(`producer.py`, 8 fields), classifies per-member coverage, and names the
2 uncovered fields with member counts on both sides.
MUST-NOT-PUBLISH: a `sampled` Coverage Ledger row marked COMPLETE for the
gate set.
