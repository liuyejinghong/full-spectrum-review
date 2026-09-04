# Contributing a Domain Pack

A Domain Pack is distilled domain experience, not a second methodology. Read
`domains/_CONTRACT.md` first — it is the binding authoring contract. This file
is the contribution path, not a second contract.

## What earns a pack

A pack is worth adding when it contributes knowledge that a competent
domain-neutral reviewer would not reliably infer from source code alone
(venue semantics, regulatory control categories, failure patterns with
real cost behind them). Do not submit generic concurrency, retry, testing,
security, or performance advice — core already owns those.

## Submission contents

- `domains/<domain>/DOMAIN.md` with the required frontmatter (`domain`,
  `version`, `applies-when`, `extends: core`, `last-verified`) and the six
  required sections from the contract;
- a one-paragraph provenance note per non-obvious clause: which of the three
  pipelines produced it (incident postmortem, regulatory framework, reference
  convergence) and the cost evidence behind it (a real incident, a regulatory
  mandate, or independent reference convergence — at least one, or the clause
  is a preference and does not ship);
- a statement of what the pack explicitly does **not** cover (features it is
  conditional on, neighboring domains it defers to).

## Review bar

Every clause must pass the contract's shared curation gate: generality test,
no source-system vocabulary, experience-not-law framing, correct section, cost
evidence. A target with an evidenced reason to differ records its reasoning
instead of complying — pack statements are high-base-rate verify/challenge
questions, never law.

## Versioning

Packs version independently from the core Skill. Bump the pack `version` in
frontmatter on content change; core `VERSION` is untouched by pack submissions.
