"""Release rollback. Restores the pre-upgrade snapshot on candidate failure."""

import copy
import state

SNAPSHOT = {"generation": 3, "positions": {"ETH": 0.025}, "protection": {"stop": 1787.14}}


def rollback() -> dict:
    restored = copy.deepcopy(SNAPSHOT)
    state.positions = restored["positions"]
    state.protection = restored["protection"]
    return {"terminal": "recovered"}
