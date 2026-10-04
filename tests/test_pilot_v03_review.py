"""Regressions for scientific-review repairs; no model or human evidence.

The author reference preparations below exercise the evaluator and renderer.
They are not samples of learned behavior or evidence of method efficacy.
"""

import re
import sys
import unittest
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pilots" / "v03"))

from pydantic import ValidationError

from reflectai_v03.context import generation_payload, render_rules, retained_rules
from reflectai_v03.contracts import Candidate, OutputField, Preparation, Rule, WorkOutput
from reflectai_v03.data import build_histories, build_tasks
from reflectai_v03.evaluation import evaluate_output, evaluate_preparation


def _reference_preparation(history, truth):
    return Preparation(candidates=[
        Candidate(candidate_id=f"reference-{index}",
                  claim="Author reference fixture only.", status=target.status,
                  rule=target.rule, evidence_ids=[history.records[0].record_id])
        for index, target in enumerate(truth.candidate_targets)
    ])


def _approved_state(record):
    """Read the explicit observed field state, not a linguistic gold label."""
    state = re.search(r"approved annual_total state=(present|absent)", record.observation, re.IGNORECASE)
    if state:
        return state.group(1)
    change = re.search(r"annual_total state:\s*(?:present|absent)\s*->\s*(present|absent)",
                       record.observation)
    if change:
        return change.group(1)
    raise AssertionError(f"revision lacks an explicit annual_total outcome: {record.record_id}")


class MatchedSalesReviewTests(unittest.TestCase):
    def test_reviewer_contrast_holds_within_each_of_two_identical_cases(self):
        for seed in (0, 1, 2, 3):
            dataset = build_histories(seed, "test_fixture")
            by_history = {history.history_id: history for history in dataset.histories}
            for truth in dataset.truths:
                if truth.scenario_id not in ("S03", "S04"):
                    continue
                history = by_history[truth.history_id]
                cases = defaultdict(list)
                for record in history.records:
                    if record.kind == "revision":
                        self.assertIn("case_id", record.context)
                        cases[record.context["case_id"]].append(record)
                with self.subTest(seed=seed, scenario=truth.scenario_id):
                    self.assertGreaterEqual(len(cases), 2)
                    observed_by_actor = defaultdict(set)
                    for reviews in cases.values():
                        self.assertGreaterEqual(len({record.actor for record in reviews}), 2)
                        # Within each case, only the reviewing person may vary.
                        contexts = [{key: value for key, value in record.context.items()
                                     if key != "reviewer"} for record in reviews]
                        self.assertTrue(all(context == contexts[0] for context in contexts))
                        states = {_approved_state(record) for record in reviews}
                        self.assertEqual(len(states), 2 if truth.scenario_id == "S03" else 1)
                        for record in reviews:
                            self.assertEqual(record.context["reviewer"], record.actor)
                            observed_by_actor[record.actor].add(_approved_state(record))
                            observed_case = truth.scope_probes[0].model_copy(update={"context": record.context})
                            predicted = render_rules(observed_case, truth.world_policy.rules)
                            self.assertEqual("present" if "annual_total" in predicted else "absent",
                                             _approved_state(record))
                    self.assertTrue(all(len(states) == 1 for states in observed_by_actor.values()))
                    self.assertFalse(any("case_id" in target.rule.scope.match
                                         for target in truth.candidate_targets))

    def test_every_sales_scope_probe_has_a_coherent_annual_calculation(self):
        totals = set()
        for seed in (0, 1, 2, 3):
            dataset = build_tasks(build_histories(seed, "test_fixture"), seed + 901)
            probes = [probe for truth in dataset.truths if truth.scenario_id in ("S03", "S04")
                      for probe in truth.scope_probes]
            probes += [task for task in dataset.tasks if task.context["task_family"] == "renewal_preview"]
            for probe in probes:
                with self.subTest(seed=seed, task=probe.task_id):
                    expected = Decimal(probe.facts["monthly_unit_price"]) * Decimal(probe.facts["seat_count"]) * 12
                    self.assertEqual(Decimal(probe.facts["annual_total"]), expected)
                    totals.add(expected)
                    baseline = {field.name: field.value for field in probe.baseline_fields}
                    for name in ("monthly_unit_price", "seat_count", "annual_total"):
                        if name in baseline:
                            self.assertEqual(baseline[name], probe.facts[name])
        self.assertGreaterEqual(len(totals), 3)


class RetrievalUncertaintyReviewTests(unittest.TestCase):
    def setUp(self):
        self.dataset = build_tasks(build_histories(3301, "test_fixture"), 7741)
        self.histories = {history.history_id: history for history in self.dataset.histories}
        self.truths = {truth.scenario_id: truth for truth in self.dataset.truths}
        self.tasks = {task.task_id: task for task in self.dataset.tasks}

    def test_unobserved_route_alternatives_remain_unresolved_not_rejected(self):
        for scenario, scope in (("S05", "active"), ("S06", "global")):
            truth = self.truths[scenario]
            unresolved = [target for target in truth.candidate_targets if target.status == "unresolved"]
            self.assertEqual(len(unresolved), 1)
            self.assertFalse(any(target.status == "reject" for target in truth.candidate_targets))
            if scope == "active":
                self.assertEqual(unresolved[0].rule.scope.match["collection"], ["active"])
            else:
                self.assertNotIn("collection", unresolved[0].rule.scope.match)
                adopted = [target for target in truth.candidate_targets if target.status == "adopt"]
                self.assertEqual(len(adopted), 1)
                self.assertEqual(adopted[0].rule.scope.match["collection"], ["active"])

    def test_unresolved_reference_status_earns_coverage_but_reject_does_not(self):
        for scenario in ("S05", "S06"):
            truth = self.truths[scenario]
            history = self.histories[truth.history_id]
            prep = _reference_preparation(history, truth)
            score = evaluate_preparation(truth, history, prep)
            self.assertEqual(score["target_coverage"], score["target_count"])
            self.assertEqual(score["coverage_by_status"]["unresolved"]["covered"], 1)
            altered = prep.model_copy(deep=True)
            for candidate in altered.candidates:
                if candidate.status == "unresolved":
                    candidate.status = "reject"
            rescored = evaluate_preparation(truth, history, altered)
            self.assertEqual(rescored["coverage_by_status"]["unresolved"]["covered"], 0)

    def test_admissible_policies_preserve_the_specific_unresolved_route_difference(self):
        for scenario in ("S05", "S06"):
            truth = self.truths[scenario]
            self.assertEqual(len(truth.admissible_policies), 2)
            for key in self.dataset.task_truths:
                if key.history_id != truth.history_id:
                    continue
                task = self.tasks[key.task_id]
                possible_endpoints = {render_rules(task, policy.rules)["endpoint"]
                                      for policy in truth.admissible_policies}
                unresolved_context = ((scenario == "S05" and key.probe == "diagnostic")
                                      or (scenario == "S06" and key.probe == "control"))
                self.assertEqual(len(possible_endpoints), 2 if unresolved_context else 1)
                if unresolved_context:
                    self.assertEqual(key.expected_decision, "keep")

    def test_unresolved_routes_never_enter_either_adaptation_arms_runtime(self):
        for scenario in ("S05", "S06"):
            truth = self.truths[scenario]
            history = self.histories[truth.history_id]
            prep = _reference_preparation(history, truth)
            adopted = retained_rules(prep, history)
            self.assertEqual(len(adopted), 0 if scenario == "S05" else 1)
            for key in self.dataset.task_truths:
                if key.history_id != truth.history_id:
                    continue
                task = self.tasks[key.task_id]
                for arm in ("C", "D"):
                    payload = generation_payload(task, history, arm, prep)
                    rules = [Rule.model_validate(rule) for rule in payload["instructions"]]
                    expected_count = int(scenario == "S06" and key.probe == "diagnostic")
                    self.assertEqual(len(rules), expected_count)
                    rendered = render_rules(task, rules)
                    response = WorkOutput(
                        task_id=task.task_id, decision="apply" if expected_count else "keep",
                        applied_rules=rules,
                        fields=[OutputField(name=name, value=value) for name, value in rendered.items()],
                    )
                    result = evaluate_output(task, key, truth, response, arm, prep)
                    self.assertTrue(result["update_correct"], result)
                    self.assertTrue(result["world_compliant"], result)

    def test_new_record_requests_known_current_release_instead_of_unseen_release(self):
        for scenario in ("S05", "S06"):
            truth = self.truths[scenario]
            history = self.histories[truth.history_id]
            evidence = "\n".join(record.observation for record in history.records)
            key = next(key for key in self.dataset.task_truths
                       if key.history_id == truth.history_id and key.probe == "diagnostic")
            task = self.tasks[key.task_id]
            self.assertEqual(task.facts["release_id"], "REL-42")
            self.assertIn("REL-41", evidence)
            self.assertIn(task.facts["release_id"], evidence)
            requested_record = re.search(r"new record (I\d+)", task.request)
            self.assertIsNotNone(requested_record)
            self.assertNotIn(requested_record.group(1), evidence)


class ReportingProbeReviewTests(unittest.TestCase):
    def test_narrative_scope_probes_obey_the_actual_narrative_output_contract(self):
        for seed in (0, 1, 2, 3):
            dataset = build_tasks(build_histories(seed, "test_fixture"), seed + 718)
            for truth in dataset.truths:
                if truth.scenario_id not in ("S07", "S08"):
                    continue
                narrative = [probe for probe in truth.scope_probes
                             if probe.context.get("artifact") == "narrative"]
                self.assertTrue(narrative)
                for probe in narrative:
                    baseline = {field.name: field.value for field in probe.baseline_fields}
                    self.assertEqual(set(baseline), {"paragraph", "source_footnote"})
                    self.assertNotIn("title", render_rules(probe, truth.world_policy.rules))


class ProvisionalReflectionReviewTests(unittest.TestCase):
    def test_D1_schema_cannot_make_a_final_adopt_or_reject_decision(self):
        from reflectai_v03.contracts import ReflectionDraft

        dataset = build_histories(3301, "test_fixture")
        truth = next(truth for truth in dataset.truths if truth.scenario_id == "S06")
        history = next(history for history in dataset.histories if history.history_id == truth.history_id)
        prep = _reference_preparation(history, truth)
        raw = prep.model_dump(mode="json")
        for candidate in raw["candidates"]:
            candidate["status"] = "unresolved"
        draft = ReflectionDraft.model_validate(raw)
        self.assertTrue(all(candidate.status == "unresolved" for candidate in draft.candidates))
        converted = Preparation.model_validate(draft.model_dump(mode="json"))
        self.assertEqual(converted.model_dump(mode="json"), raw)
        for forbidden_status in ("adopt", "reject"):
            invalid = draft.model_dump(mode="json")
            invalid["candidates"][0]["status"] = forbidden_status
            with self.subTest(status=forbidden_status), self.assertRaises(ValidationError):
                ReflectionDraft.model_validate(invalid)


if __name__ == "__main__":
    unittest.main()
