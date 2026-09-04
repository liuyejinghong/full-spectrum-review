"""Versioned runtime state. Generation bumps on every externally visible change."""

generation = 3
positions: dict = {"ETH": 0.020}
protection = {"stop": 1880.61}


def external_progress() -> None:
    global generation
    generation += 1
