# Case 03 — Anonymous irreversible action (trading pack)

Seeded defect: `orders.py` flattens the position on risk signal with no
durable identity minted before POST. Fills cannot be attributed to the
intent that caused them, and the obligation cannot be closed.

Packs to load: trading.

MUST-CATCH: a finding demanding a durable identity bound to the served
position/trade, minted before POST.
