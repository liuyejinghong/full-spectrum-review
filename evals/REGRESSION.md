# FSR Regression Net

A recall net for the audit protocol, not a quality leaderboard.

Open reasoning (Accidental Complexity, Business) cannot be graded
deterministically, so this net asserts **must-catch recall** on seeded
defects plus **must-not-publish** discipline on one trap case. It answers
one question before every core release: *did the latest protocol change
quietly blind the auditor?*

## Procedure

For each case under `fixtures/case-*`:

1. Run a full-spectrum audit in **single-unit** mode on the fixture
   directory, loading the packs named in the case README.
2. Present `case-*/README.md`'s history situation exactly as stated
   (case-05 is a snapshot **without** git history — do not invent any).
3. Collect published findings (P0–P3 only; observations do not count
   except where the case demands their absence/presence).
4. Assert the case's `MUST-CATCH` / `MUST-NOT-PUBLISH` lines.

## Pass criteria

6/6 cases green. A red case blocks the core release until the protocol
or the case is fixed — a case may itself be wrong; fix the case, never
weaken the assertion to pass.

## Cadence

Run before every core MINOR release, and after any change to
`finding-protocol.md`, `orchestration-protocol.md`, or any Domain Pack.
Cases are derived from real incidents; when a new incident teaches a new
failure shape, add a case (see `CONTRIBUTING_PACKS.md` curation gate for
the evidence standard).

## Limits (honest)

- Assertions cover recall and discipline only, never prose quality.
- Checking is human or LLM-judge-assisted; the judge may assist
  matching but may not lower the bar to pass.
- Fixtures are minimal by design — a protocol that needs a 10k-line
  repo to catch a seeded defect is already failing.
