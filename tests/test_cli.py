"""Exercise the runnable CLI, packaged example, and disk-output boundaries.

All validation scores below are synthetic protocol fixtures, never performance
evidence. Each command runs in a fresh Python process using the current runtime.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_workflow import make_bundle, make_records, make_splits


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="grounded-reflection-test-")
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-m", "grounded_reflection", *map(str, args)],
                              text=True, encoding="utf-8", capture_output=True, check=False)

    def write_json(self, name, value):
        target = self.root / name
        target.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return target

    def selection_arguments(self, records=None):
        bundle = make_bundle()
        records = make_records() if records is None else records
        return [
            "select", "--bundle", self.write_json("bundle.json", bundle.model_dump(mode="json")),
            "--candidate", bundle.candidates[0].candidate_id,
            "--records", self.write_json("records.json", [r.model_dump(mode="json") for r in records]),
            "--splits", self.write_json("splits.json", make_splits().model_dump(mode="json")),
            "--baseline", "baseline-v1", "--output", self.root / "selection",
        ]

    def test_packaged_demo_computes_three_assessments_and_defers_without_ratings(self):
        output = self.root / "demo"
        process = self.run_cli("demo", "--output", output)
        self.assertEqual(process.returncode, 0, process.stderr)
        summary = json.loads(process.stdout)
        self.assertEqual(summary["data_origin"], "synthetic")
        self.assertEqual(summary["hypothesis_origin"], "curated_fixture")
        self.assertEqual(summary["model_calls"], 0)
        self.assertGreaterEqual(summary["episodes"], 4)
        self.assertEqual({c["candidate_id"]: c["status"] for c in summary["candidates"]}, {
            "scoped-update": "eligible_for_validation",
            "overbroad-update": "rejected",
            "ambiguous-update": "needs_clarification",
        })
        decision = summary["selection"]
        self.assertEqual(decision["status"], "deferred")
        self.assertEqual(decision["case_count"], 0)
        self.assertIsNone(decision["mean_quality_gain"])
        self.assertEqual(decision["active_version"], "unmodified-agent")
        self.assertEqual(decision["record_origins"], [])
        self.assertEqual({p.name for p in output.iterdir()},
                         {"summary.json", "evidence.json", "splits.json"})
        self.assertEqual(json.loads((output / "summary.json").read_text(encoding="utf-8")), summary)

    def test_existing_outputs_are_preserved_and_overwrite_is_rejected(self):
        output = self.root / "demo"
        self.assertEqual(self.run_cli("demo", "--output", output).returncode, 0)
        sentinel = b"user-owned existing content\n"
        (output / "summary.json").write_bytes(sentinel)
        before = {p.name: p.read_bytes() for p in output.iterdir()}
        process = self.run_cli("demo", "--output", output)
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("already exists", process.stderr)
        self.assertEqual({p.name: p.read_bytes() for p in output.iterdir()}, before)

    def test_validate_reports_broken_reference_with_nonzero_exit(self):
        bundle = make_bundle()
        bundle.hypotheses[0].support[0].quote = "Fabricated evidence absent from source"
        path = self.write_json("broken-reference.json", bundle.model_dump(mode="json"))
        process = self.run_cli("validate", path)
        self.assertEqual(process.returncode, 1, process.stderr)
        result = json.loads(process.stdout)
        self.assertFalse(result["references_valid"])
        self.assertIn("h-1", result["reference_errors"])
        self.assertEqual(result["assessments"][0]["status"], "rejected")

    def test_schema_exports_usable_typed_contracts(self):
        output = self.root / "schemas"
        process = self.run_cli("schema", "--output", output)
        self.assertEqual(process.returncode, 0, process.stderr)
        expected_names = {name + ".schema.json" for name in (
            "EvidenceBundle", "PairedEvaluation", "SplitManifest", "SelectionPolicy", "SelectionDecision")}
        self.assertEqual(set(json.loads(process.stdout)["files"]), expected_names)
        self.assertEqual({p.name for p in output.iterdir()}, expected_names)
        schemas = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in output.iterdir()}
        bundle_schema = schemas["EvidenceBundle.schema"]
        self.assertEqual(bundle_schema["type"], "object")
        self.assertFalse(bundle_schema["additionalProperties"])
        self.assertTrue({"episodes", "hypotheses", "candidates"} <= set(bundle_schema["required"]))
        self.assertIn("EvidenceReference", bundle_schema["$defs"])
        self.assertIn("Scope", bundle_schema["$defs"])
        rating_schema = schemas["PairedEvaluation.schema"]
        self.assertTrue({"candidate_digest", "baseline_critical_errors", "candidate_critical_errors"}
                        <= set(rating_schema["required"]))
        self.assertEqual(rating_schema["properties"]["candidate_score"]["minimum"], 0)
        self.assertEqual(rating_schema["properties"]["candidate_score"]["maximum"], 1)

    def test_select_fixture_ratings_records_policy_acceptance_without_export(self):
        process = self.run_cli(*self.selection_arguments())
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result["decision"]["status"], "accepted")
        self.assertEqual(result["decision"]["record_origins"], ["fixture"])
        self.assertEqual(result["written"], ["decision.json"])
        output = self.root / "selection"
        self.assertEqual({p.name for p in output.iterdir()}, {"decision.json"})
        self.assertEqual(json.loads((output / "decision.json").read_text(encoding="utf-8")),
                         result["decision"])

    def test_select_final_test_case_fails_before_writing_any_output(self):
        for split in ("validation", "final_test"):
            with self.subTest(split=split):
                records = make_records()
                records[0].case_id = "final-1"
                records[0].split = split
                process = self.run_cli(*self.selection_arguments(records))
                self.assertNotEqual(process.returncode, 0)
                self.assertIn("declared validation", process.stderr)
                self.assertFalse((self.root / "selection").exists())


if __name__ == "__main__":
    unittest.main()
