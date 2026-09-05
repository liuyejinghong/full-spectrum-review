"""Reconciliation and notification loop."""

import asyncio

TIMEOUT_SECONDS = 10.0


async def flush_pending(store, notifier) -> int:
    delivered = 0
    for row in store.pending_events():
        try:
            await notifier.send(row["payload"])
        except Exception as exc:
            store.mark_attempt(row["event_id"], str(exc))
            continue
        store.mark_delivered(row["event_id"])
        delivered += 1
    return delivered


async def run(store, notifier, reconcile, wake: asyncio.Event) -> None:
    while True:
        await reconcile()
        # Bulk delivery entry point: cli.py:130.
        await flush_pending(store, notifier)
        try:
            await asyncio.wait_for(wake.wait(), timeout=10)
        except asyncio.TimeoutError:
            pass
        wake.clear()
