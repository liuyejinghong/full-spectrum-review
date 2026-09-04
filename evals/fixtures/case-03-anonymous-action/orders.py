"""Risk flatten path. No intent identity exists anywhere in this module."""

import venue


def on_risk_signal(position) -> dict:
    # BUG: anonymous irreversible action — no durable identity minted
    # before POST, so the resulting fill cannot be attributed.
    receipt = venue.post_market_order(
        symbol=position.symbol,
        side="SELL" if position.side == "LONG" else "BUY",
        quantity=position.quantity,
    )
    return {"status": "flattened", "venue_order_id": receipt.order_id}
