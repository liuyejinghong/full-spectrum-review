"""Dual interpreters sharing decision code (see LIMITATIONS.md before proposing changes)."""


def should_exit(position, signal, stop_hit):
    if signal == "exit":
        return "exit_signal"
    if stop_hit:
        return "stoploss"
    return None


def backtest_loop(candles, position):
    # sync: evaluates against candle low/high bounds
    for candle in candles:
        yield should_exit(position, candle.signal, candle.low_hit_stop)


def live_loop(poll_rate, position):
    # async: evaluates against a single polled rate, no bounds
    return should_exit(position, poll_rate.signal, poll_rate.stop_hit)
