# Compact Audit Example

This is an illustrative source snapshot and report, not a finding about this
repository or a deployed system. Ordinary audits need not load this example.

## Example target

The adapter's public configuration specifies `timeout_ms` in milliseconds;
the transport interface accepts `timeout_seconds` in seconds.

```python
# adapter.py

def send(config, transport, payload):
    return transport.send(payload, timeout_seconds=config.timeout_ms)
```

The following is the complete compact report for that supplied snapshot.

---

# Transport Adapter Audit

## Audit metadata

- Target: transport-adapter source snapshot
- Target revision: unavailable — supplied snippet without git metadata
- Date: 2026-09-05
- Core: 0.13.0; revision unavailable — copied skill without git metadata
- Mode: single-unit
- Packs: none; trading and deploy do not apply to this adapter
- Prior audit: none supplied
- Limitation: transport implementation and deployed configuration not supplied

## Coverage

| Area / flow | Depth | Status | Evidence |
|---|---|---|---|
| Config → transport timeout | deep | COMPLETE | Traced `adapter.send` and the supplied unit contracts |
| Transport internals | none | NOT_COVERED | Outside the supplied snapshot |

## Assessment

The adapter passes a millisecond value to a seconds-based interface. Correct
the conversion before relying on the configured timeout. There is one active
P2 finding and no P0, P1, or P3 findings. Deployed incident frequency is unknown.

| ID | Priority | Confidence | Status | Type | Finding |
|---|---|---|---|---|---|
| FSR-001 | P2 | High | OPEN | Defect | Timeout uses the wrong unit |

Execution order: correct the conversion, then verify the value received by
the transport for a nonzero millisecond timeout.

## FSR-001 — Timeout uses the wrong unit

ID: FSR-001
Priority: P2
Confidence: High
Status: OPEN
Type: Defect
Area: Transport adapter
Evidence: `adapter.send`, supplied configuration and transport contracts
Frequency: inferred

`send()` forwards `config.timeout_ms` unchanged as `timeout_seconds`. A
configured value of 500 therefore supplies 500 seconds rather than 0.5 seconds.
Requests awaiting a response may wait far longer than the configured duration.
The supplied contracts establish the mismatch; deployed failure counts and
application-wide availability consequences are not established by this snippet.

Convert milliseconds to seconds at this boundary, preserving fractional values.
Verify that a configuration of 500 ms reaches the transport as 0.5 seconds.

## Keep as-is

Keep the unit conversion at the adapter boundary so callers retain the public
millisecond configuration contract and the transport retains its seconds API.

## Evidence gaps

Transport internals and deployed workload were not supplied. No production
incident count or system-wide availability claim follows from this audit.

---

## Saved files

With audit-artifact writes authorized, the report can live at
`fsr-reports/transport-adapter/2026-09-05-snapshot-full-spectrum-review.md`.
Use a distinct name for a later snapshot. The authoritative `INDEX.json` is:

```json
[
  {
    "id": "FSR-001",
    "title": "Timeout uses the wrong unit",
    "firstSeen": "2026-09-05",
    "priority": "P2",
    "status": "OPEN",
    "latestAudit": "2026-09-05-snapshot-full-spectrum-review.md"
  }
]
```

Render `INDEX.md` from those records:

| ID | Title | First Seen | Current Priority | Status | Latest Audit |
|---|---|---|---|---|---|
| FSR-001 | Timeout uses the wrong unit | 2026-09-05 | P2 | OPEN | 2026-09-05-snapshot-full-spectrum-review.md |
