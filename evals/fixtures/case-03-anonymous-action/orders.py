"""Risk-triggered position close."""

import venue


def on_risk_signal(position) -> dict:
    receipt = venue.post_market_order(
        symbol=position.symbol,
        side="SELL" if position.side == "LONG" else "BUY",
        quantity=position.quantity,
    )
    return {"status": "flattened", "venue_order_id": receipt.order_id}
