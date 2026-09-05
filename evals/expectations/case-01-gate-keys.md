# Case 01 — Gate key table (enumerable-set completeness)

Seeded defect (for the runner, not the auditor): `producer.py` emits 8
economic fields; `gate.py` governs only 6. Two fields (`fee_rebate`,
`funding_adj`) are silently dropped by the allowlist before settlement.

Packs to load: none (core only).

MUST-CATCH: a finding that enumerates members from the consuming code
(`producer.py`, 8 fields), checks per-member preservation, and names the
2 dropped fields with member counts on both sides.
MUST-NOT-PUBLISH: a `sampled` Coverage Ledger row marked COMPLETE for the
gate set.
