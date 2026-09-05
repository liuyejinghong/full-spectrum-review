"""Regression checks for supported ledger inputs and schema-owned constraints."""

import json
import unittest
from pathlib import Path

from validate_fsr import index_errors


class IndexValidationTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(
            (Path(__file__).resolve().parent.parent / "schemas/index.schema.json").read_text()
        )
        self.entry = dict(
            id="FSR-001", title="Lost rebate", firstSeen="2026-09-05",
            priority="P2", status="OPEN", latestAudit="audit.md",
        )

    def test_valid_ledger_and_empty_ledger(self):
        self.assertEqual(index_errors([self.entry], self.schema), [])
        self.assertEqual(index_errors([], self.schema), [])

    def test_title_length_comes_from_schema(self):
        self.entry["title"] = "x"
        self.assertTrue(index_errors([self.entry], self.schema))
        self.schema["items"]["properties"]["title"]["minLength"] = 1
        self.assertEqual(index_errors([self.entry], self.schema), [])

    def test_wrong_field_types_return_diagnostics(self):
        for field in self.entry:
            for value in (None, 1, [], {}):
                with self.subTest(field=field, value=value):
                    self.assertTrue(index_errors([dict(self.entry, **{field: value})], self.schema))

    def test_enum_and_id_constraints(self):
        for field, value in (("priority", "P9"), ("status", "DONE"), ("id", "001")):
            with self.subTest(field=field):
                self.assertTrue(index_errors([dict(self.entry, **{field: value})], self.schema))

    def test_required_fields_and_unknown_fields(self):
        for field in self.entry:
            entry = dict(self.entry)
            del entry[field]
            self.assertTrue(index_errors([entry], self.schema))
        self.assertTrue(index_errors([dict(self.entry, extra="unexpected")], self.schema))

    def test_empty_provenance(self):
        for field in ("firstSeen", "latestAudit"):
            self.assertTrue(index_errors([dict(self.entry, **{field: ""})], self.schema))

    def test_duplicate_ids(self):
        self.assertTrue(index_errors([self.entry, dict(self.entry)], self.schema))

    def test_wrong_container_shapes(self):
        self.assertTrue(index_errors({}, self.schema))
        self.assertTrue(index_errors([None], self.schema))


if __name__ == "__main__":
    unittest.main()
