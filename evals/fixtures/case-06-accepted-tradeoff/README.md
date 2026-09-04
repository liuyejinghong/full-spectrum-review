# Case 06 — Accepted tradeoff guard (stated-rationale check)

Trap case, inverted direction. `LIMITATIONS.md` documents that the dual
interpreter gap below is a deliberate cost tradeoff. `engines.py` shows two
interpreters (sync candle loop vs async polled rate) sharing decision code.

Packs to load: none (core only).

MUST-NOT-PUBLISH: a fresh Defect/Business finding demanding a shared-tape
parity contract. The correct output is ACCEPTED-with-rationale (citing
`LIMITATIONS.md`) or an Open Question — never a finding that pretends the
tradeoff was never considered.
MUST-CATCH (discipline): the report must cite the stated rationale and
decline the fresh finding. An auditor that publishes the parity demand
without mentioning `LIMITATIONS.md` fails this case.
