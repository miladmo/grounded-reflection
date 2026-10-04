"""Synthetic-data checks. No backend is imported and no final tasks are generated."""

import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from grounded_reflection.pilot_v02.data import (
    DEFAULT_SEED, generate_family_truth, generate_histories, generate_tasks,
    task_content_fingerprint, write_development,
)


class PilotDataTests(unittest.TestCase):
    def test_recoverable_requirements_have_repeated_accepted_evidence(self):
        histories = {history.family: history for history in generate_histories()}
        for family in generate_family_truth():
            self.assertEqual(len(histories[family.family].episodes), 8)
            for rule in family.recoverable:
                supported = [
                    episode for episode in histories[family.family].episodes
                    if rule.scope.applies_to(episode.context) == "match"
                    and any(item.kind == "human_revision"
                            and f"{rule.field}={rule.value}" in item.text
                            for item in episode.evidence)
                ]
                self.assertGreaterEqual(len(supported), 2, (family.family, rule))
            all_text = "\n".join(item.text for episode in histories[family.family].episodes
                                 for item in episode.evidence)
            for rule in family.distractors + family.unidentifiable:
                self.assertIn(f"{rule.field}={rule.value}", all_text)
            self.assertTrue(any(episode.missingness for episode in histories[family.family].episodes))
            self.assertTrue(any(item.kind == "tool_result"
                                for episode in histories[family.family].episodes for item in episode.evidence))

    def test_scoped_counterexamples_and_missing_context_are_present(self):
        for truth in generate_family_truth():
            for rule in truth.recoverable:
                applicability = {rule.scope.applies_to(context) for context in truth.scope_probes}
                self.assertIn("match", applicability)
                self.assertIn("mismatch", applicability)
                if rule.field == "emphasis":
                    self.assertIn("unknown", applicability)
            history = next(item for item in generate_histories() if item.family == truth.family)
            for distractor in truth.distractors:
                counterexamples = [
                    episode for episode in history.episodes
                    if distractor.scope.applies_to(episode.context) == "match"
                    and any(item.kind == "human_revision"
                            and any(value != distractor.value for value in
                                    re.findall(rf"\b{distractor.field}=([a-z_]+)", item.text))
                            for item in episode.evidence)
                ]
                self.assertGreaterEqual(len(counterexamples), 2)
            for rule in truth.recoverable:
                for key in ("audience", "channel"):
                    if key not in rule.scope.match:
                        continue
                    counterexamples = [
                        episode for episode in history.episodes
                        if episode.context.get(key) not in rule.scope.match[key]
                        and all(episode.context.get(other) in values
                                for other, values in rule.scope.match.items() if other != key)
                        and any(item.kind == "human_revision"
                                and any(value != rule.value for value in
                                        re.findall(rf"\b{rule.field}=([a-z_]+)", item.text))
                                for item in episode.evidence)
                    ]
                    self.assertTrue(counterexamples, (truth.family, rule.field, rule.value, key))

    def test_reviews_explain_work_without_disclosing_oracle_categories(self):
        prohibited = ("distractor", "out-of-scope", "not a shared decision", "personally prefer",
                      "neither reviewer", "unresolved disagreement", "review is still open",
                      "continue using the existing", "is correct")
        for history in generate_histories():
            for episode in history.episodes:
                for item in episode.evidence:
                    self.assertFalse(any(label in item.text.lower() for label in prohibited))
                    if item.kind == "human_feedback":
                        self.assertNotIn("emphasis=", item.text)
                        self.assertNotIn("route=", item.text)
            local = history.episodes[6]
            self.assertIn("showcase", local.task)
            self.assertTrue(any(item.kind == "human_revision" and "showcase" in item.text
                                for item in local.evidence))
            reviews = [item.text for item in local.evidence if item.kind == "human_feedback"]
            self.assertTrue(any("Ari, editor, batch 41" in text for text in reviews))
            self.assertTrue(any("Bo, editor, batch 41" in text for text in reviews))
            tool_records = history.episodes[7].evidence
            self.assertFalse(any(item.kind == "human_feedback" for item in tool_records))
            self.assertTrue(any("status=503" in item.text for item in tool_records))
            self.assertTrue(any("status=200" in item.text for item in tool_records))

    def test_supported_exceptions_are_observed_and_do_not_license_broad_rules(self):
        histories = {history.family: history for history in generate_histories()}
        for truth in generate_family_truth():
            history = histories[truth.family]
            self.assertEqual(len(truth.supported_exceptions), 3)
            self.assertEqual(history.episodes[6].context["occasion"], "showcase")
            self.assertTrue(all(episode.context["occasion"] == "routine"
                                for index, episode in enumerate(history.episodes) if index != 6))
            for exception in truth.supported_exceptions:
                self.assertIsNotNone(exception.scope)
                supporting_episodes = [
                    episode for episode in history.episodes
                    if exception.scope.applies_to(episode.context) == "match"
                    and any(item.kind == "human_revision"
                            and f"{exception.field}={exception.value}" in item.text
                            for item in episode.evidence)
                ]
                if exception.scope.match.get("occasion") == ["showcase"]:
                    self.assertEqual(len(supporting_episodes), 1)
                    self.assertEqual(exception.scope.match["audience"],
                                     [history.episodes[6].context["audience"]])
                else:
                    self.assertEqual(len(supporting_episodes), 2)
                    self.assertEqual(len({episode.context["audience"] for episode in supporting_episodes}), 2)
                self.assertFalse(any(rule.field == exception.field and rule.value == exception.value
                                     for rule in truth.recoverable))
                for distractor in truth.distractors:
                    if distractor.field == exception.field and distractor.value == exception.value:
                        self.assertFalse(distractor.scope.is_within(exception.scope))
        for split in ("calibration", "validation"):
            self.assertTrue(all(task.context["occasion"] == "routine"
                                for task in generate_tasks(split)[0]))

    def test_calibration_pairs_explicit_anchors_with_unexposed_transfer_requirements(self):
        tasks, truths = generate_tasks("calibration")
        families = {item.family: item for item in generate_family_truth()}
        self.assertEqual(len(tasks), 6)
        self.assertEqual(sum(truth.category == "transfer" for truth in truths), 3)
        self.assertEqual(sum(truth.category == "boundary" for truth in truths), 3)
        for family in families:
            self.assertEqual({truth.category for truth in truths if truth.family == family},
                             {"transfer", "boundary"})
        for task, truth in zip(tasks, truths):
            self.assertEqual(task.case_id, truth.case_id)
            self.assertEqual(task.context["family"], task.family)
            self.assertEqual(set(task.output_fields), {check.field for check in truth.checks})
            hidden = [check for check, kind in zip(truth.checks, truth.check_kinds) if kind == "hidden"]
            self.assertEqual(len(hidden), 2 if truth.category == "transfer" else 0)
            payload = json.dumps(task.public_payload())
            self.assertNotIn('"split"', payload)
            for check in hidden:
                self.assertNotIn(check.value, payload)
                self.assertTrue(any(rule.field == check.field and rule.value == check.value
                                    and rule.scope.applies_to(task.context) == "match"
                                    for rule in families[task.family].recoverable))
            if truth.category == "boundary":
                self.assertEqual(truth.allowed_actions, ["deliver"])
                self.assertFalse(truth.missing_fields)
                for check, kind in zip(truth.checks, truth.check_kinds):
                    self.assertIn(check.value, payload)
                    if check.field in ("emphasis", "route"):
                        self.assertEqual(kind, "explicit")
                        self.assertIn(f"{check.field}={check.value}", task.request)
                self.assertTrue(all(rule.scope.applies_to(task.context) == "mismatch"
                                    for rule in families[task.family].recoverable))
            for label in ("recoverable", "unidentifiable", "distractors", "allowed_actions", "check_kinds"):
                self.assertNotIn(label, payload)

    def test_ambiguity_does_not_reward_guessing_and_boundary_has_current_evidence(self):
        tasks, truths = generate_tasks("validation")
        families = {item.family: item for item in generate_family_truth()}
        for task, truth in zip(tasks, truths):
            self.assertEqual(len(truth.checks), len(truth.check_kinds))
            self.assertTrue(all(check.field in task.output_fields for check in truth.checks))
            if truth.category == "ambiguous":
                self.assertNotIn("audience", task.context)
                self.assertEqual(truth.missing_fields, ["audience"])
                self.assertEqual(truth.unresolved_output_fields, ["emphasis"])
                self.assertNotIn("deliver", truth.allowed_actions)
                self.assertEqual(next(c.value for c in truth.checks if c.field == "emphasis"), "undetermined")
                for rule in families[task.family].recoverable:
                    if rule.field == "emphasis":
                        self.assertEqual(rule.scope.applies_to(task.context), "unknown")
                        self.assertNotEqual(rule.value, "undetermined")
            else:
                self.assertEqual(truth.category, "boundary")
                self.assertTrue(all(rule.scope.applies_to(task.context) == "mismatch"
                                    for rule in families[task.family].recoverable))
                for check, kind in zip(truth.checks, truth.check_kinds):
                    if check.field in ("emphasis", "route"):
                        self.assertEqual(kind, "explicit")
                        self.assertIn(check.value, task.request)
            correct = {(check.field, check.value) for check in truth.checks}
            self.assertFalse(correct.intersection((check.field, check.value) for check in truth.distractors))

    def test_instances_are_seeded_but_world_rules_do_not_drift(self):
        self.assertEqual(generate_histories(12), generate_histories(12))
        self.assertEqual(generate_tasks("calibration", 12), generate_tasks("calibration", 12))
        self.assertEqual(generate_family_truth(12), generate_family_truth(98))
        all_tasks = []
        for split in ("calibration", "validation"):
            for seed in (12, 98):
                all_tasks.extend(generate_tasks(split, seed)[0])
        self.assertEqual(len(all_tasks), len({task.case_id for task in all_tasks}))
        self.assertEqual(len(all_tasks), len({task_content_fingerprint(task) for task in all_tasks}))
        original = all_tasks[0]
        copied = original.model_copy(update={"case_id": "relabeled", "split": "validation"})
        self.assertEqual(task_content_fingerprint(original), task_content_fingerprint(copied))
        self.assertNotEqual(generate_histories(12), generate_histories(98))
        with self.assertRaises(ValueError):
            generate_tasks("typo")

    def test_development_writer_never_generates_final_cases_or_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "data"
            with patch("grounded_reflection.pilot_v02.data.generate_tasks", wraps=generate_tasks) as generator:
                written = write_development(root, DEFAULT_SEED)
            self.assertEqual([call.args[0] for call in generator.call_args_list], ["calibration", "validation"])
            self.assertEqual(set(written), {
                "histories.json", "calibration.json", "validation.json",
                "ground_truth/families.json", "ground_truth/calibration.json", "ground_truth/validation.json",
            })
            for path in written.values():
                self.assertTrue(json.loads(path.read_text(encoding="utf-8")))
                self.assertNotIn("final_test", path.read_text(encoding="utf-8"))
            before = {name: path.read_bytes() for name, path in written.items()}
            with self.assertRaises(FileExistsError):
                write_development(root, 123)
            self.assertEqual(before, {name: path.read_bytes() for name, path in written.items()})


if __name__ == "__main__":
    unittest.main()
