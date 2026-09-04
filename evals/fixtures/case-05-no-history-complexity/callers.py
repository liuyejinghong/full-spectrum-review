"""Two production callers depend on submit()'s retry+fallback contract."""

from service import submit


def nightly_bulk(entries: list) -> None:
    for e in entries:
        submit(e)  # relies on fallback_region routing outside office hours


def manual_single(entry: dict) -> dict:
    return submit(entry)  # relies on retry before surfacing errors to ops
