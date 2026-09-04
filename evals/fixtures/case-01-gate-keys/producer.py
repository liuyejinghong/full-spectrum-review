"""Fill producer: emits the full economic record per execution."""

from gate import apply_gate


def on_fill(fill) -> dict:
    record = {
        "trade_id": fill.id,
        "symbol": fill.symbol,
        "side": fill.side,
        "quantity": fill.qty,
        "price": fill.price,
        "fee": fill.fee,
        "fee_rebate": fill.rebate,
        "funding_adj": fill.funding,
    }
    return apply_gate(record)
