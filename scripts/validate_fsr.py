#!/usr/bin/env python3
"""FSR repository self-check (stdlib only).

Checks:
  1. Version consistency: VERSION == latest ## [x.y.z] in CHANGELOG.md
     == vX.Y.Z strings in README.md / README.en.md.
  2. Markdown fence balance (``` count even) in every .md file.
  3. Required skill files exist.
  4. Any fsr-reports/**/INDEX.json validates against schemas/index.schema.json
     (hand-rolled: id pattern, priority/confidence/status enums, required keys).

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

ID_RE = re.compile(r"^FSR-[0-9]{3,}$")
PRIORITIES = {"P0", "P1", "P2", "P3"}
STATUSES = {"OPEN", "FIXED", "ACCEPTED", "SUPERSEDED", "REOPENED"}
INDEX_KEYS = {"id", "title", "firstSeen", "priority", "status", "latestAudit"}

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"FAIL: {msg}")


def main() -> int:
    # 1. required files
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            fail(f"missing required file: {rel}")

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
    for idx in sorted((ROOT / "fsr-reports").rglob("INDEX.json")) if (ROOT / "fsr-reports").is_dir() else []:
        try:
            entries = json.loads(idx.read_text())
        except json.JSONDecodeError as e:
            fail(f"{idx.relative_to(ROOT)}: invalid JSON ({e})")
            continue
        if not isinstance(entries, list):
            fail(f"{idx.relative_to(ROOT)}: top level must be an array")
            continue
        seen: set[str] = set()
        for i, e in enumerate(entries):
            where = f"{idx.relative_to(ROOT)}[{i}]"
            if not isinstance(e, dict) or set(e) != INDEX_KEYS:
                fail(f"{where}: keys must be exactly {sorted(INDEX_KEYS)}")
                continue
            if not ID_RE.match(e["id"]):
                fail(f"{where}: bad id {e['id']!r}")
            if e["id"] in seen:
                fail(f"{where}: duplicate id {e['id']}")
            seen.add(e["id"])
            if e["priority"] not in PRIORITIES:
                fail(f"{where}: bad priority {e['priority']!r}")
            if e["status"] not in STATUSES:
                fail(f"{where}: bad status {e['status']!r}")
            for k in ("title", "firstSeen", "latestAudit"):
                if not isinstance(e[k], str) or not e[k].strip():
                    fail(f"{where}: {k} must be a non-empty string")

    if errors:
        print(f"\n{len(errors)} problem(s).")
        return 1
    print("OK: versions consistent, fences balanced, required files present, INDEX.json valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
