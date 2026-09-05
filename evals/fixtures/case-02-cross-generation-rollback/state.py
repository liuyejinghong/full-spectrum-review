"""Runtime state reflecting external venue changes."""

generation = 3
positions: dict = {"ETH": 0.025}
protection = {"stop": 1787.14}


def external_progress() -> None:
    global generation
    generation += 1
    positions["ETH"] = 0.020
    protection["stop"] = 1880.61
