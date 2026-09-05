# FSR Regression Net

A recall net for the audit protocol, not a quality leaderboard.

Open reasoning (Accidental Complexity, Business) cannot be graded
deterministically, so this net asserts **must-catch recall** on seeded
defects plus **must-not-publish** discipline on trap cases. It answers
one question before every core release: *did the latest protocol change
quietly blind the auditor?*

## Procedure

Auditor inputs live in `fixtures/case-*`; runner/judge answers live in
`expectations/<case>.md`. Never expose expectations or this runner document
to the auditor. Fixture READMEs contain only target context and pack selection.

1. Prepare a clean workspace outside this repository. Copy only `SKILL.md`,
   `VERSION`, `references/`, and `domains/` as the skill, and the contents of
   each fixture into a neutrally named target directory. Do not copy git
   history, expectations, or prior audit reports. Some fixtures are explicit
   source excerpts with omitted dependencies; respect their stated scope.
2. Start an auditor in a fresh context that has not seen the answers or this
   change's design discussion. Run a **single-unit** audit of each target,
   loading the packs named in its README. Multiple cases may share that fresh
   run, but each target gets its own coverage and report. Record whether cases
   shared context; do not present such a run as independent per-case trials.
3. Save the auditor's reports before opening expectations. Collect published
   findings (P0–P3 only; observations count only where the expectation says so).
4. The runner compares each report with its separate expectation. Judge the
   mechanism and consequence, not keyword repetition or finding count. Record
   case results, auditor/model when available, protocol revision or working-tree
   state, and evidence references. A reread by an auditor already exposed to
   answers is a consistency check, not a blind recall run.

## Pass criteria

7/7 cases green. A red case blocks the core release until the protocol
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
- The repository self-check checks fixture counts, not audit outcomes. Its
  success does not establish that these cases passed.
