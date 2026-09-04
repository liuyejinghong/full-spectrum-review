# Known limitations (maintainer-stated, binding on reviewers)

- The backtest engine (sync candle loop) and the live engine (async polled
  rate) share decision code but interpret it differently. A shared-tape
  parity contract was proposed in issue #1042 and declined: recording
  trade-level tapes for 50 pairs over a year costs hundreds of GB of memory,
  and the team accepts documented divergence instead. Do not re-propose it
  as a fresh defect.
