"""Submission pipeline; helper implementations omitted from this excerpt."""

from config import RETRYABLE_ERRORS, FALLBACK_REGION, WATCHDOG_INTERVAL
from transport import submit_entry


def submit(payload: dict) -> dict:
    attempt = retry_with_backoff(lambda: submit_entry(payload), errors=RETRYABLE_ERRORS)
    if attempt.failed:
        attempt = fallback_submit(payload, region=FALLBACK_REGION)
    watchdog.register(attempt.id, interval=WATCHDOG_INTERVAL)
    return attempt


def retry_with_backoff(fn, errors):
    ...


def fallback_submit(payload, region):
    ...


class watchdog:
    @staticmethod
    def register(attempt_id, interval):
        ...
