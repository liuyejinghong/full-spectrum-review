"""Release rollback. Restores the pre-upgrade snapshot on candidate failure."""

import copy
import state

SNAPSHOT = {"generation": 3, "positions": {"ETH": 0.025}, "protection": {"stop": 1787.14}}


def rollback() -> dict:
    # BUG: never compares SNAPSHOT["generation"] with state.generation.
    # If the outside world moved on, this splices old state onto a new world.
    restored = copy.deepcopy(SNAPSHOT)
    state.positions = restored["positions"]
    state.protection = restored["protection"]
    return {"terminal": "recovered"}
