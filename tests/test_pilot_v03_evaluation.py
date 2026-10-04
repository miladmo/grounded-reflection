"""Measurement regressions: uncertainty, unsupported luck and fixed denominators."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pilots" / "v03"))

from grounded_reflection.models import Scope
from reflectai_v03.context import render_rules
from reflectai_v03.contracts import (
    Candidate, CandidateTarget, History, HistoryTruth, OutputField, Policy,
    Preparation, Record, Rule, Task, TaskTruth, WorkOutput,
)
from reflectai_v03.evaluation import aggregate, calibration_gates, evaluate_output, evaluate_preparation
from reflectai_v03.data import build_histories, build_tasks


def fields(values):
    return [OutputField(name=name, value=value) for name, value in values.items()]


def pack(name, recipient="external", contract="permanent"):
    context = {"family": "contact_pack", "recipient": recipient, "contract": contract}
    if recipient is None:
        context.pop("recipient")
    return Task(task_id=name, context=context, facts={},
                baseline_fields=fields({"reference": "N17", "email": "work@example.invalid"}),
                request="Prepare the contact pack.")


def omission(**scope):
    return Rule(field="reference", operation="omit", scope=Scope(match={
        "family": ["contact_pack"], **{key: [value] for key, value in scope.items()}}))


def fixture(ambiguous=False):
    recipient = omission(recipient="external")
    contract = omission(contract="temporary")
    probes = [pack("ep"), pack("et", contract="temporary"),
              pack("ip", recipient="internal"),
              pack("it", recipient="internal", contract="temporary"),
              pack("unknown", recipient=None)]
    policy = Policy(policy_id="private-world", rules=[recipient])
    truth = HistoryTruth(
        history_id="history", scenario_id="S02" if ambiguous else "S01", pair_id="P01",
        world_policy=policy,
        admissible_policies=[policy, Policy(policy_id="rival", rules=[contract])] if ambiguous else [policy],
        candidate_targets=[CandidateTarget(target_id="opaque-target", rule=recipient,
                                            status="unresolved" if ambiguous else "adopt")],
        scope_probes=probes,
    )
    task = probes[0]
    task_truth = TaskTruth(task_id=task.task_id, history_id="history", probe="diagnostic",
                           expected_decision="keep" if ambiguous else "apply",
                           recoverable=not ambiguous, world_fields=fields(render_rules(task, [recipient])))
    history = History(history_id="history", initial_configuration="Use both fields.",
                      assumptions="The convention is stable.",
                      field_dictionary={"reference": "Booking reference", "email": "Work email"},
                      records=[Record(record_id="observed", timestamp="2026-01-01", kind="revision",
                                      actor="reviewer", context={"family": "contact_pack"},
                                      observation="The reviewer revised the reference field.")])
    return task, task_truth, truth, history, recipient


def candidate(rule, status="adopt", **kwargs):
    return Candidate(candidate_id=kwargs.pop("candidate_id", "agent-owned-id"),
                     claim="A candidate inferred from the records.", status=status, rule=rule,
                     evidence_ids=kwargs.pop("evidence_ids", ["observed"]), **kwargs)


def output(task, rules=(), **kwargs):
    rendered = render_rules(task, list(rules))
    decision = "apply" if rendered != {item.name: item.value for item in task.baseline_fields} else "keep"
    return WorkOutput(task_id=task.task_id, decision=kwargs.pop("decision", decision),
                      applied_rules=list(rules), fields=kwargs.pop("fields", fields(rendered)), **kwargs)


class OutputEvaluationTests(unittest.TestCase):
    def test_unresolved_retention_is_correct_but_world_output_fails(self):
        task, key, truth, _, rule = fixture(ambiguous=True)
        prep = Preparation(candidates=[candidate(rule, "unresolved", alternatives=["contract"] )])
        score = evaluate_output(task, key, truth, output(task), "D", prep)
        self.assertTrue(score["update_correct"])
        self.assertTrue(score["completed_deliverable"])
        self.assertFalse(score["world_compliant"])
        self.assertEqual(score["unresolved_fields"], ["reference"])

    def test_lucky_unsupported_update_gets_only_world_credit(self):
        task, key, truth, _, rule = fixture(ambiguous=True)
        score = evaluate_output(task, key, truth, output(task, [rule]), "B")
        self.assertTrue(score["world_compliant"])
        self.assertFalse(score["update_correct"])
        self.assertTrue(score["unsupported_lucky_success"])

    def test_available_evidence_distinguishes_A_from_B(self):
        task, key, truth, _, rule = fixture()
        baseline = output(task)
        a = evaluate_output(task, key, truth, baseline, "A")
        b = evaluate_output(task, key, truth, baseline, "B")
        self.assertTrue(a["update_correct"])
        self.assertFalse(a["world_compliant"])
        self.assertFalse(b["update_correct"])
        self.assertTrue(evaluate_output(task, key, truth, output(task, [rule]), "B")["update_correct"])

    def test_missing_invalid_or_question_response_never_earns_keep_credit(self):
        task, key, truth, _, _ = fixture(ambiguous=True)
        for response in (None, {}, output(task, questions=["Ask an employee?"]),
                         output(task, completed=False),
                         output(task).model_copy(update={"task_id": "wrong-task"})):
            with self.subTest(response=response):
                score = evaluate_output(task, key, truth, response, "B")
                self.assertFalse(score["update_correct"])
                self.assertFalse(score["world_compliant"])

    def test_field_accuracy_survives_incomplete_output(self):
        task, key, truth, _, _ = fixture(ambiguous=True)
        response = output(task, fields=fields({"email": "work@example.invalid"}), completed=False)
        score = evaluate_output(task, key, truth, response, "B")
        self.assertEqual(score["partial_field_correctness"], 1.0)
        self.assertFalse(score["completed_deliverable"])
        self.assertFalse(score["world_compliant"])

    def test_component_score_includes_correct_omission(self):
        task, key, truth, _, rule = fixture()
        response = output(task, [rule], fields=fields({"email": "wrong@example.invalid"}))
        score = evaluate_output(task, key, truth, response, "B")
        self.assertEqual(score["partial_field_correctness"], 0.5)
        self.assertTrue(score["field_results"]["reference"]["correct"])
        self.assertEqual(evaluate_output(task, key, truth, None, "B")["partial_field_correctness"], 0)

    def test_declared_keep_cannot_override_a_supported_observed_change(self):
        task, key, truth, _, rule = fixture()
        score = evaluate_output(task, key, truth, output(task, [rule], decision="keep"), "B")
        self.assertTrue(score["update_correct"])
        self.assertTrue(score["world_compliant"])
        self.assertTrue(score["execution_consistent"])
        self.assertFalse(score["decision_label_correct"])
        self.assertFalse(score["valid_output"])
        self.assertEqual(score["effective_decision"], "apply")
        self.assertIn("declared_decision_disagrees_with_fields", score["errors"])

    def test_output_fields_must_match_rule_renderer(self):
        task, key, truth, _, rule = fixture()
        response = output(task, [rule], fields=task.baseline_fields)
        self.assertFalse(evaluate_output(task, key, truth, response, "B")["valid_output"])

    def test_C_and_D_cannot_execute_unresolved_or_rejected_candidates(self):
        task, key, truth, _, rule = fixture()
        for arm in ("C", "D"):
            for status in ("unresolved", "reject"):
                prep = Preparation(candidates=[candidate(rule, status)])
                score = evaluate_output(task, key, truth, output(task, [rule]), arm, prep)
                self.assertFalse(score["update_correct"])
                self.assertFalse(score["retained_rules_consistent"])
                self.assertTrue(score["world_compliant"])

    def test_C_and_D_cannot_drop_applicable_adopted_rules(self):
        task, key, truth, _, rule = fixture()
        prep = Preparation(candidates=[candidate(rule)])
        for arm in ("C", "D"):
            self.assertTrue(evaluate_output(task, key, truth, output(task, [rule]), arm, prep)["update_correct"])
            self.assertFalse(evaluate_output(task, key, truth, output(task), arm, prep)["retained_rules_consistent"])

    def test_applied_scope_cannot_expand_beyond_preparation(self):
        task, key, truth, _, rule = fixture()
        prep = Preparation(candidates=[candidate(rule)])
        broad = omission()
        score = evaluate_output(task, key, truth, output(task, [broad]), "C", prep)
        self.assertFalse(score["retained_rules_consistent"])

    def test_B_overbroad_rule_fails_warrant_even_when_current_output_is_right(self):
        task, key, truth, _, _ = fixture()
        score = evaluate_output(task, key, truth, output(task, [omission()]), "B")
        self.assertTrue(score["world_compliant"])
        self.assertFalse(score["update_correct"])
        self.assertFalse(score["applied_rules_supported_on_scope_probes"])

    def test_partial_consensus_change_is_permitted_despite_other_conflict(self):
        task, key, truth, _, rule = fixture(ambiguous=True)
        shared = Rule(field="email", operation="set_literal", value="shared@example.invalid",
                      scope=Scope(match={"family": ["contact_pack"]}))
        truth = truth.model_copy(deep=True)
        for policy in truth.admissible_policies:
            policy.rules.append(shared)
        world = render_rules(task, [rule, shared])
        key = key.model_copy(update={"expected_decision": "apply", "world_fields": fields(world)})
        score = evaluate_output(task, key, truth, output(task, [shared]), "B")
        self.assertTrue(score["update_correct"])
        self.assertFalse(score["world_compliant"])
        self.assertEqual(score["unresolved_fields"], ["reference"])


class CandidateEvaluationTests(unittest.TestCase):
    def test_equivalent_decomposed_adoptions_cover_a_fixed_target(self):
        _, _, truth, history, rule = fixture()
        target = rule.model_copy(update={"scope": Scope(match={
            "family": ["contact_pack"], "recipient": ["external"],
            "contract": ["temporary", "permanent"]})})
        truth.candidate_targets[0].rule = target
        truth.admissible_policies[0].rules = [target]
        prep = Preparation(candidates=[
            candidate(omission(recipient="external", contract="temporary"), candidate_id="first"),
            candidate(omission(recipient="external", contract="permanent"), candidate_id="second"),
        ])
        score = evaluate_preparation(truth, history, prep)
        self.assertEqual(score["target_coverage"], 1)
        self.assertEqual(score["targets"][0]["jointly_covering_candidate_ids"], ["first", "second"])

    def test_candidate_ids_and_claims_do_not_determine_status_coverage(self):
        _, _, truth, history, rule = fixture()
        renamed = candidate(rule, candidate_id="not-the-target-id")
        score = evaluate_preparation(truth, history, Preparation(candidates=[renamed]))
        self.assertEqual(score["target_coverage"], 1)
        wrong = candidate(omission(contract="temporary"), candidate_id="opaque-target")
        score = evaluate_preparation(truth, history, Preparation(candidates=[wrong]))
        self.assertEqual(score["target_coverage"], 0)
        self.assertEqual(score["unsupported_adoptions"], 1)

    def test_omission_is_not_rejection_and_unresolved_is_not_rejection(self):
        _, _, truth, history, rule = fixture(ambiguous=True)
        for prep in (Preparation(), Preparation(candidates=[candidate(rule, "reject")])):
            score = evaluate_preparation(truth, history, prep)
            self.assertEqual(score["coverage_by_status"]["unresolved"]["covered"], 0)
        truth.candidate_targets[0].status = "reject"
        score = evaluate_preparation(truth, history, Preparation())
        self.assertEqual(score["coverage_by_status"]["reject"]["covered"], 0)
        self.assertTrue(score["targets"][0]["omitted"])

    def test_unknown_references_cannot_earn_coverage(self):
        _, _, truth, history, rule = fixture()
        prep = Preparation(candidates=[candidate(rule, evidence_ids=["invented-record"])])
        score = evaluate_preparation(truth, history, prep)
        self.assertEqual(score["target_coverage"], 0)
        self.assertEqual(score["unsupported_adoptions"], 1)
        self.assertEqual(score["untraceable_candidates"], 1)

    def test_broad_rule_exposes_scope_error_on_boundary_probe(self):
        _, _, truth, history, _ = fixture()
        score = evaluate_preparation(truth, history, Preparation(candidates=[candidate(omission())]))
        self.assertEqual(score["adopted_rules_with_scope_errors"], 1)
        self.assertIn("ip", score["candidates"][0]["scope_error_probes"])

    def test_evidence_gap_prose_is_diagnostic_not_scored_by_regex(self):
        _, _, truth, history, rule = fixture(ambiguous=True)
        results = []
        for gap in ("", "Bananas.", "Need an external permanent correction."):
            prep = Preparation(candidates=[candidate(rule, "unresolved", evidence_gap=gap)])
            results.append(evaluate_preparation(truth, history, prep)["target_coverage"])
        self.assertEqual(results, [1, 1, 1])


def calibration_rows(always_keep_c=False):
    rows = []
    for arm in ("A", "B", "C"):
        for index in range(8):
            decision = "apply" if index < 4 else "keep"
            recoverable = index != 4
            for probe in ("diagnostic", "control"):
                correct = True
                if probe == "diagnostic":
                    if arm == "A":
                        correct = decision == "keep"
                    if arm == "C":
                        correct = decision == "keep" if always_keep_c else index not in (0, 5)
                world = probe == "control" or (recoverable and (arm == "B" or (correct and decision == "keep")))
                rows.append({"arm": arm, "scenario_id": f"S{index + 1:02d}",
                             "pair_id": f"P{index // 2 + 1:02d}", "probe": probe,
                             "expected_decision": decision if probe == "diagnostic" else "keep",
                             "recoverable": recoverable if probe == "diagnostic" else True,
                             "repetition": 1, "update_correct": correct,
                             "world_compliant": world, "completed_deliverable": True,
                             "warranted_world_compliant": correct and world,
                             "partial_field_correctness": float(world)})
    return rows


class AggregateAndCalibrationTests(unittest.TestCase):
    def test_prospective_gates_accept_complete_balanced_fixture(self):
        result = calibration_gates(calibration_rows())
        self.assertTrue(result["passed"], result)
        self.assertEqual(result["scores"]["B"]["recoverable_total"], 7)

    def test_all_keep_C_fails_even_at_four_of_eight(self):
        result = calibration_gates(calibration_rows(always_keep_c=True))
        self.assertEqual(result["scores"]["C"]["diagnostic_correct"], 4)
        self.assertFalse(result["passed"])
        self.assertFalse(result["checks"]["C_apply_at_least_2_of_4"])

    def test_missing_or_duplicate_attempts_cannot_change_gate_denominators(self):
        rows = calibration_rows()
        self.assertFalse(calibration_gates(rows[:-1])["passed"])
        self.assertFalse(calibration_gates([*rows, rows[-1]])["passed"])

    def test_lucky_world_success_is_not_a_recoverable_warranted_deliverable(self):
        rows = calibration_rows()
        changed = 0
        for row in rows:
            if row["arm"] == "B" and row["probe"] == "diagnostic" and row["recoverable"] and changed < 2:
                row["warranted_world_compliant"] = False
                changed += 1
        result = calibration_gates(rows)
        self.assertFalse(result["checks"]["B_recoverable_deliverables_at_least_6_of_7"])

    def test_aggregate_never_pools_controls_into_primary(self):
        rows = calibration_rows()
        for row in rows:
            if row["arm"] == "C":
                row["update_correct"] = row["probe"] == "control"
        result = aggregate(rows)
        self.assertEqual(result["primary"]["variant_mean_by_arm"]["C"], 0)
        self.assertEqual(result["control_variant_mean_by_arm"]["C"], 1)
        self.assertEqual(result["by_arm"]["C"]["diagnostic"]["n"], 8)

    def test_aggregate_averages_variants_before_unequal_repetitions(self):
        template = calibration_rows()[0]
        rows = [{**template, "arm": "C", "scenario_id": "first", "update_correct": True,
                 "repetition": rep} for rep in (1, 2, 3)]
        rows.append({**template, "arm": "C", "scenario_id": "second", "update_correct": False})
        result = aggregate(rows)
        self.assertEqual(result["primary"]["variant_mean_by_arm"]["C"], 0.5)


class AuthorReferenceFixtureIntegrationTests(unittest.TestCase):
    """Evaluator-author reference fixtures; these are not research evidence."""

    def test_all_eight_cards_across_four_counterbalanced_seeds(self):
        for seed in (0, 1, 2, 3):
            dataset = build_tasks(build_histories(seed, "test_fixture"), task_seed=seed + 100)
            histories = {history.history_id: history for history in dataset.histories}
            truths = {truth.history_id: truth for truth in dataset.truths}
            tasks = {task.task_id: task for task in dataset.tasks}
            preparations = {}
            for truth in dataset.truths:
                history = histories[truth.history_id]
                prep = Preparation(candidates=[
                    Candidate(candidate_id=f"author-reference-{index}",
                              claim="Evaluator-author reference fixture; not a model answer.",
                              status=target.status, rule=target.rule,
                              evidence_ids=[history.records[0].record_id])
                    for index, target in enumerate(truth.candidate_targets)
                ])
                preparations[truth.history_id] = prep
                score = evaluate_preparation(truth, history, prep)
                with self.subTest(seed=seed, scenario=truth.scenario_id, measure="candidates"):
                    self.assertEqual(score["target_coverage"], score["target_count"])
                    self.assertEqual(score["unsupported_adoptions"], 0)
                    if truth.scenario_id in ("S03", "S07"):
                        self.assertGreater(score["coverage_by_status"]["adopt"]["covered"], 0)
            for key in dataset.task_truths:
                task, truth = tasks[key.task_id], truths[key.history_id]
                prep = preparations[key.history_id]
                rules = [entry.rule for entry in prep.candidates
                         if entry.status == "adopt" and entry.rule.scope.applies_to(task.context) == "match"]
                score = evaluate_output(task, key, truth, output(task, rules), "D", prep)
                with self.subTest(seed=seed, scenario=truth.scenario_id, probe=key.probe):
                    self.assertTrue(score["update_correct"], score)
                    self.assertEqual(score["world_compliant"], key.recoverable)
                    if truth.scenario_id == "S02" and key.probe == "diagnostic":
                        self.assertFalse(score["world_compliant"])
                        self.assertEqual(score["expected_decision_for_arm"], "keep")


if __name__ == "__main__":
    unittest.main()
