"""Shared reliability configuration. Operator-owned; changed 2026-08-30."""

RETRYABLE_ERRORS = (TimeoutError, ConnectionResetError)
FALLBACK_REGION = "eu-west-1"
WATCHDOG_INTERVAL = 30
