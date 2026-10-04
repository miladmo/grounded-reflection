"""Public-contract regressions for the prospective second calibration round.

These checks assemble prompts and exercise deterministic contract semantics.
They make no model calls and contain no scenario-specific answer instructions.
"""

import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pilots" / "v03"))

from grounded_reflection.models import Scope
from reflectai_v03.context import generation_payload, render_rules
from reflectai_v03.contracts import (
    Candidate, History, HistoryTruth, OutputField, Policy, Preparation, Record,
    Rule, Task, TaskTruth, WorkOutput,
)
from reflectai_v03.evaluation import evaluate_output
from reflectai_v03.runner import (
    DESIGN_REVISION, GENERATION_PROMPT, PREPARATION_PROMPTS, SHARED_CONTRACT, _prompt,
)
from reflectai_v03.storage import source_manifest


REPO = Path(__file__).resolve().parents[1]
PROMPTS = REPO / "pilots" / "v03" / "prompts"


class SharedPromptAssemblyTests(unittest.TestCase):
    def test_runner_selects_the_new_versions_and_explicit_revision(self):
        self.assertEqual(PREPARATION_PROMPTS, {
            "C": {1: "prepare_C_v2.txt", 2: "review_C_v2.txt"},
            "D": {1: "prepare_D_v3.txt", 2: "review_D_v3.txt"},
        })
        self.assertEqual(GENERATION_PROMPT, "generate_v2.txt")
        self.assertEqual(SHARED_CONTRACT, "shared_contract_v2.txt")
        self.assertEqual(DESIGN_REVISION, "v03-calibration-r2")
        for prior in ("prepare_C_v1.txt", "review_C_v1.txt", "prepare_D_v1.txt",
                      "review_D_v1.txt", "prepare_D_v2.txt", "review_D_v2.txt", "generate_v1.txt"):
            self.assertTrue((PROMPTS / prior).is_file(), prior)

    def test_exact_same_contract_is_appended_once_to_every_stage(self):
        shared = (PROMPTS / SHARED_CONTRACT).read_text(encoding="utf-8").rstrip()
        payload = {"history": {"records": [{"observation": "Neutral public evidence"}]}}
        names = [name for stages in PREPARATION_PROMPTS.values() for name in stages.values()]
        names.append(GENERATION_PROMPT)
        for name in names:
            with self.subTest(prompt=name):
                assembled = _prompt(REPO, name, payload)
                instructions, serialized = assembled.split("\nPAYLOAD\n", 1)
                self.assertEqual(instructions.count(shared), 1)
                self.assertTrue(instructions.endswith(shared))
                self.assertEqual(json.loads(serialized), payload)
                self.assertNotIn("A keep decision has applied_rules=[]", instructions)

    def test_shared_contract_is_in_the_source_freeze(self):
        relative = f"pilots/v03/prompts/{SHARED_CONTRACT}"
        manifest = source_manifest(REPO)
        self.assertEqual(manifest[relative], hashlib.sha256((REPO / relative).read_bytes()).hexdigest())

    def test_prompt_reads_the_supplied_snapshot_not_a_later_source_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            snapshot = Path(directory) / "snapshot"
            source_prompts = source / "pilots" / "v03" / "prompts"
            source_prompts.mkdir(parents=True)
            (source_prompts / GENERATION_PROMPT).write_text("Generic generation stage", encoding="utf-8")
            (source_prompts / SHARED_CONTRACT).write_text("Frozen public operator contract", encoding="utf-8")
            shutil.copytree(source, snapshot)
            (source_prompts / SHARED_CONTRACT).write_text("Later source contract", encoding="utf-8")
            frozen_prompt = _prompt(snapshot, GENERATION_PROMPT, {})
            self.assertIn("Frozen public operator contract", frozen_prompt)
            self.assertNotIn("Later source contract", frozen_prompt)

    def test_missing_shared_contract_stops_prompt_construction(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / "pilots" / "v03" / "prompts"
            folder.mkdir(parents=True)
            (folder / GENERATION_PROMPT).write_text("Generic stage", encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                _prompt(Path(directory), GENERATION_PROMPT, {})

    def test_public_contract_contains_no_scenario_answers(self):
        shared = (PROMPTS / SHARED_CONTRACT).read_text(encoding="utf-8")
        for secret in ("S05", "S07", "ep-98141", "V92501", "numeric_table", "checksum_check"):
            self.assertNotIn(secret, shared)
        self.assertIn("baseline[field] + separator + facts[value]", shared)


class PublicOperatorMeaningTests(unittest.TestCase):
    def test_append_reads_the_complete_baseline_and_never_deduplicates(self):
        rule = Rule(field="heading", operation="append_fact", value="suffix", separator=" | ",
                    scope=Scope(match={"kind": ["memo"]}))
        task = Task(task_id="neutral-append", context={"kind": "memo"}, facts={"suffix": "Z9"},
                    baseline_fields=[OutputField(name="heading", value="Alpha")], request="Prepare the memo.")
        self.assertEqual(render_rules(task, [rule]), {"heading": "Alpha | Z9"})
        already_formatted = task.model_copy(update={"baseline_fields": [
            OutputField(name="heading", value="Alpha | Z9")]})
        self.assertEqual(render_rules(already_formatted, []), {"heading": "Alpha | Z9"})
        self.assertEqual(render_rules(already_formatted, [rule]), {"heading": "Alpha | Z9 | Z9"})
        # Two identical assignments read the same baseline, not one another's output.
        self.assertEqual(render_rules(task, [rule, rule]), {"heading": "Alpha | Z9"})

    def test_faithful_noop_instructions_allow_keep_in_both_adaptation_arms(self):
        task = Task(task_id="neutral-noop", context={"kind": "memo"}, facts={"flag": "ready"},
                    baseline_fields=[OutputField(name="flag", value="ready")], request="Prepare the memo.")
        rule = Rule(field="flag", operation="set_fact", value="flag", scope=Scope(match={"kind": ["memo"]}))
        history = History(history_id="neutral-history", initial_configuration="The flag is already ready.",
                          assumptions="The local configuration is stable.", field_dictionary={"flag": "Exact text marker."},
                          records=[Record(record_id="neutral-record", timestamp="2026-01-01", kind="review",
                                          actor="reviewer", context={"kind": "memo"},
                                          observation="The configured flag was retained.")])
        prep = Preparation(candidates=[Candidate(candidate_id="neutral-confirmation",
                            claim="Retain the supplied marker.", status="adopt", rule=rule,
                            evidence_ids=["neutral-record"])])
        policy = Policy(policy_id="neutral-policy", rules=[])
        history_truth = HistoryTruth(history_id=history.history_id, scenario_id="neutral", pair_id="neutral",
                                     world_policy=policy, admissible_policies=[policy],
                                     candidate_targets=[], scope_probes=[task])
        truth = TaskTruth(task_id=task.task_id, history_id=history.history_id, probe="control",
                          expected_decision="keep", recoverable=True, world_fields=task.baseline_fields)
        for arm in ("C", "D"):
            payload = generation_payload(task, history, arm, prep)
            self.assertEqual(len(payload["instructions"]), 1)
            response = WorkOutput(task_id=task.task_id, decision="keep", applied_rules=[rule],
                                  fields=task.baseline_fields)
            score = evaluate_output(task, truth, history_truth, response, arm, prep)
            self.assertTrue(score["update_correct"], score)
            self.assertTrue(score["retained_rules_consistent"], score)
            self.assertTrue(score["world_compliant"], score)


if __name__ == "__main__":
    unittest.main()
