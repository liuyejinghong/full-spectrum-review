"""Optional fill model, default off (seeded bug inside the gated path)."""

LIQUIDITY_CAP_ENABLED = False


def capped_qty(requested: float, allowance: float) -> float:
    if not LIQUIDITY_CAP_ENABLED:
        return requested
    if allowance <= 0:
        return 0.0
    return min(requested, allowance)


class Position:
    def __init__(self, qty: float) -> None:
        self.qty = qty
        self.tp1_done = False


def take_profit(position: Position, requested: float, allowance: float) -> bool:
    qty = capped_qty(requested, allowance)
    if LIQUIDITY_CAP_ENABLED and qty <= 0 and requested > 0:
        return False
    # Seeded bug: partial capped fill still flips the completion flag.
    position.qty -= qty
    position.tp1_done = True
    return True
