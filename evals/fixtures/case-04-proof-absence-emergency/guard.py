"""Protection guard. Local proof store plus venue read API."""

import venue

_proofs: dict = {}


def has_proof(position_id: str) -> bool:
    return position_id in _proofs


def ensure_protected(position) -> dict:
    # BUG: proof absence is equated with protection absence.
    # No venue coverage check before the emergency POST.
    if not has_proof(position.id):
        receipt = venue.post_stop_order(
            symbol=position.symbol,
            quantity=position.quantity,
        )
        return {"status": "emergency_placed", "order_id": receipt.order_id}
    return {"status": "already_protected"}
