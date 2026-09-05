# Stateful release recovery

A failed software upgrade can request restoration of a saved runtime snapshot.
Positions and protection track an external venue that continues to operate
during the upgrade. `external_progress()` models a venue change reflected in
runtime state. Local restore does not undo that external change.

Domain Packs: deploy. This is a source snapshot without git history.
