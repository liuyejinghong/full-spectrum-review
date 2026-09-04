"""Settlement gate: only allowlisted fields reach the ledger."""

ALLOWED_FIELDS = {
    "trade_id",
    "symbol",
    "side",
    "quantity",
    "price",
    "fee",
}


def apply_gate(record: dict) -> dict:
    return {k: v for k, v in record.items() if k in ALLOWED_FIELDS}
