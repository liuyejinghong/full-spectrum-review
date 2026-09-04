# Case 02 — Cross-generation rollback (deploy pack)

Seeded defect: `rollback.py` restores the pre-upgrade snapshot
unconditionally. `state.py` tracks a `generation` counter bumped by every
externally visible change, but nothing reads it on the restore path. After
any external progress, rollback splices old state onto a new world.

Packs to load: deploy.

MUST-CATCH: a finding demanding generation-paired restore — prior state
may return only while external facts are unchanged, otherwise reconcile
forward.
