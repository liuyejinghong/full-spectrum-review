#!/usr/bin/env python3
"""FSR repository self-check (stdlib only).

Checks:
  1. Version consistency: VERSION == latest ## [x.y.z] in CHANGELOG.md
     == vX.Y.Z strings in README.md / README.en.md.
  2. Markdown fence balance (``` count even) in every .md file.
  3. Required skill files exist.
  4. Any fsr-reports/**/INDEX.json satisfies the index schema's string fields,
     required/exact keys, enums, patterns, and minimum lengths; IDs are unique.
     This is an index-specific check, not a general JSON Schema validator.
  5. Every domains/*/DOMAIN.md frontmatter carries version + last-verified.
  6. evals fixture case count matches the N/N expectation in REGRESSION.md.

Usage: python3 scripts/validate_fsr.py [--root <repo>]
Exit 0 when clean, 1 otherwise.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else Path(__file__).resolve().parent.parent

REQUIRED = [
    "SKILL.md", "VERSION", "CHANGELOG.md", "README.md", "README.en.md",
    "domains/_CONTRACT.md",
    "references/orchestration-protocol.md",
    "references/first-principles-review.md",
    "references/engineering-review.md",
    "references/business-logic-review.md",
    "references/optimization-review.md",
    "references/finding-protocol.md",
    "references/reporting-protocol.md",
    "schemas/finding.schema.json",
    "schemas/index.schema.json",
]

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"FAIL: {msg}")


def index_errors(entries, schema) -> list[str]:
    """Validate ledger records using the constraints owned by the index schema."""
    if not isinstance(entries, list):
        return ["top level must be an array"]
    problems = []
    item = schema["items"]
    fields = item["properties"]
    required = set(item["required"])
    seen = set()
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            problems.append(f"[{i}]: entry must be an object")
            continue
        if required - entry.keys() or (not item["additionalProperties"] and entry.keys() - fields.keys()):
            problems.append(f"[{i}]: keys must be exactly {sorted(fields)}")
            continue
        for name, rule in fields.items():
            if name not in entry:
                continue
            value = entry[name]
            where = f"[{i}].{name}"
            if not isinstance(value, str):
                problems.append(f"{where}: must be a string")
                continue
            if len(value) < rule.get("minLength", 0):
                problems.append(f"{where}: minimum length is {rule['minLength']}")
            if "enum" in rule and value not in rule["enum"]:
                problems.append(f"{where}: invalid value {value!r}")
            if "pattern" in rule and not re.search(rule["pattern"], value):
                problems.append(f"{where}: invalid format {value!r}")
        identity = entry.get("id")
        if isinstance(identity, str):
            if identity in seen:
                problems.append(f"[{i}]: duplicate id {identity}")
            seen.add(identity)
    return problems


def main() -> int:
    # 1. required files
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            fail(f"missing required file: {rel}")
    if errors:
        return 1

    # 2. version consistency
    version = (ROOT / "VERSION").read_text().strip()
    changelog = (ROOT / "CHANGELOG.md").read_text()
    m = re.search(r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\]", changelog, re.M)
    if not m:
        fail("CHANGELOG.md has no ## [x.y.z] entry")
    elif m.group(1) != version:
        fail(f"VERSION ({version}) != CHANGELOG latest ({m.group(1)})")
    for readme in ("README.md", "README.en.md"):
        text = (ROOT / readme).read_text()
        if f"`v{version}`" not in text:
            fail(f"{readme} does not reference `v{version}`")

    # 3. fence balance
    for md in sorted(ROOT.rglob("*.md")):
        if ".git/" in str(md):
            continue
        n = sum(1 for line in md.read_text().splitlines() if line.startswith("```"))
        if n % 2:
            fail(f"unbalanced fences in {md.relative_to(ROOT)} ({n})")

    # 4. INDEX.json validation
    index_schema = json.loads((ROOT / "schemas/index.schema.json").read_text())
    for idx in sorted((ROOT / "fsr-reports").rglob("INDEX.json")) if (ROOT / "fsr-reports").is_dir() else []:
        try:
            entries = json.loads(idx.read_text())
        except json.JSONDecodeError as e:
            fail(f"{idx.relative_to(ROOT)}: invalid JSON ({e})")
            continue
        for problem in index_errors(entries, index_schema):
            fail(f"{idx.relative_to(ROOT)}{problem}")

    # 5. DOMAIN.md frontmatter: version + last-verified
    for domain_md in sorted((ROOT / "domains").glob("*/DOMAIN.md")) if (ROOT / "domains").is_dir() else []:
        text = domain_md.read_text()
        if not re.search(r"^version:\s*\d+", text, re.M):
            fail(f"{domain_md.relative_to(ROOT)}: frontmatter missing version")
        if not re.search(r"^last-verified:\s*\d{4}-\d{2}-\d{2}", text, re.M):
            fail(f"{domain_md.relative_to(ROOT)}: frontmatter missing last-verified (YYYY-MM-DD)")

    # 6. evals case count matches REGRESSION.md expectation
    reg = ROOT / "evals" / "REGRESSION.md"
    fixtures = ROOT / "evals" / "fixtures"
    if reg.is_file() and fixtures.is_dir():
        m = re.search(r"(\d+)/(\d+) cases green", reg.read_text())
        cases = sorted(p for p in fixtures.iterdir() if p.is_dir() and p.name.startswith("case-"))
        if not m:
            fail("evals/REGRESSION.md has no N/N cases-green expectation")
        elif int(m.group(1)) != int(m.group(2)):
            fail(f"evals/REGRESSION.md expects {m.group(1)}/{m.group(2)} (unbalanced)")
        elif int(m.group(1)) != len(cases):
            fail(f"evals/REGRESSION.md expects {m.group(1)} cases but found {len(cases)} fixtures")

    if errors:
        print(f"\n{len(errors)} problem(s).")
        return 1
    print("OK: versions consistent, fences balanced, required files present, INDEX.json valid, packs versioned, evals count matches.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
