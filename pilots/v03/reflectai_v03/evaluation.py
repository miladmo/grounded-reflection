"""Deterministic, evaluator-only scoring for the v0.3 bounded comparison.

No claims, candidate IDs, evidence-gap prose or model judges determine a score.
Rule equivalence is behavioural over the frozen scope probes, not a claim of
equivalence over an unlimited real-world context space.
"""

from __future__ import annotations

from statistics import mean
from typing import Any

from .context import render_rules
from .contracts import History, HistoryTruth, Preparation, Rule, Task, TaskTruth, WorkOutput


def _fields(items) -> dict[str, str]:
    return {item.name: item.value for item in items}


def _consensus(task: Task, truth: HistoryTruth, *, baseline_only: bool = False):
    baseline = _fields(task.baseline_fields)
    if baseline_only:
        return baseline, []
    alternatives = [render_rules(task, policy.rules) for policy in truth.admissible_policies]
    names = set(baseline).union(*(set(item) for item in alternatives))
    expected, conflicts = dict(baseline), []
    absent = object()
    for name in sorted(names):
        values = [item.get(name, absent) for item in alternatives]
        if all(value == values[0] for value in values):
            if values[0] is absent:
                expected.pop(name, None)
            else:
                expected[name] = values[0]
        else:
            conflicts.append(name)
    return expected, conflicts


def _signature(rules: list[Rule], probes: list[Task]):
    """Preserve field effects, including omission, on frozen evaluator probes."""
    return tuple(tuple(sorted(render_rules(probe, rules).items())) for probe in probes)


def _equivalent(left: Rule, right: Rule, probes: list[Task]) -> bool:
    if left.field != right.field:
        return False
    try:
        return _signature([left], probes) == _signature([right], probes)
    except (ValueError, KeyError, TypeError):
        return False


def _rule_support(rule: Rule, truth: HistoryTruth) -> dict[str, list]:
    """An effect is warranted only where all admitted policies support it."""
    violations, scope_errors, render_errors, changed = [], [], [], []
    for probe in truth.scope_probes:
        try:
            baseline = _fields(probe.baseline_fields)
            proposed = render_rules(probe, [rule])
            consensus, conflicts = _consensus(probe, truth)
            absent = object()
            old = baseline.get(rule.field, absent)
            new = proposed.get(rule.field, absent)
            justified = consensus.get(rule.field, absent)
            if new != old:
                changed.append(probe.task_id)
                if new != justified:
                    violations.append(probe.task_id)
                    if justified == old or rule.field in conflicts:
                        scope_errors.append(probe.task_id)
        except (ValueError, KeyError, TypeError) as exc:
            render_errors.append({"probe": probe.task_id, "error": str(exc)})
    return {"violations": violations, "scope_errors": scope_errors,
            "render_errors": render_errors, "changed": changed}


def _effects_within(rule: Rule, target: Rule, probes: list[Task]) -> bool:
    """Permit multiple narrower adopted rules to cover one evaluator target."""
    if rule.field != target.field:
        return False
    try:
        for probe in probes:
            baseline = _fields(probe.baseline_fields)
            proposed = render_rules(probe, [rule])
            intended = render_rules(probe, [target])
            if proposed != baseline and proposed != intended:
                return False
        return True
    except (ValueError, KeyError, TypeError):
        return False


def evaluate_output(
    task: Task,
    truth: TaskTruth,
    history_truth: HistoryTruth,
    output: WorkOutput | None,
    arm: str,
    preparation: Preparation | None = None,
) -> dict[str, Any]:
    """Score update warrant and observed world obligations independently.

For A, epistemic warrant is relative to its current-task-only information. The
common history-based diagnostic rubric is used for B/C/D. Preparation reference
validation is a runner prerequisite because History is not an argument here.

The effective update is the observed difference from baseline. A declared
decision label is audited separately and never replaces that effect. Warrant
also requires executable, applicable and supported rules consistent with the
retained preparation. World compliance concerns the completed structured
deliverable, independently of its rule and decision metadata. Missing responses,
wrong task identities, questions and incomplete deliverables earn neither credit.
"""
    if arm not in ("A", "B", "C", "D"):
        raise ValueError(f"unknown arm: {arm}")
    if task.task_id != truth.task_id or truth.history_id != history_truth.history_id:
        raise ValueError("task/evaluator truth identity mismatch")
    baseline = _fields(task.baseline_fields)
    world = _fields(truth.world_fields)
    expected, conflicts = _consensus(task, history_truth, baseline_only=arm == "A")
    expected_decision = "apply" if expected != baseline else "keep"
    if arm != "A" and expected_decision != truth.expected_decision:
        raise ValueError("frozen expected decision disagrees with admissible policies")
    errors: list[str] = []
    present = isinstance(output, WorkOutput)
    actual = _fields(output.fields) if present else {}
    field_names = sorted(set(baseline) | set(world) | set(actual))
    field_results = {
        name: {"correct": present and (name in actual) == (name in world)
               and actual.get(name) == world.get(name),
               "expected_present": name in world, "actual_present": name in actual,
               "expected": world.get(name), "actual": actual.get(name)}
        for name in field_names
    }
    # Empty expected outputs are possible; a missing response never earns 1.0.
    partial = (sum(item["correct"] for item in field_results.values()) / len(field_results)
               if field_results else float(present))
    rendered: dict[str, str] | None = None
    identity_correct = bool(present and output.task_id == task.task_id)
    question_free = bool(present and not output.questions)
    actual_decision = ("apply" if actual != baseline else "keep") if present else None
    label_correct = bool(present and output.decision == actual_decision)
    execution_consistent = present
    if not present:
        errors.append("missing_or_invalid_output")
    else:
        if not identity_correct:
            errors.append("wrong_task_id")
        if not question_free:
            errors.append("employee_question_protocol_deviation")
        try:
            rendered = render_rules(task, output.applied_rules)
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"invalid_applied_rules: {exc}")
            execution_consistent = False
        if any(rule.scope.applies_to(task.context) != "match" for rule in output.applied_rules):
            errors.append("nonapplicable_applied_rule")
            execution_consistent = False
        if rendered is not None and actual != rendered:
            errors.append("fields_disagree_with_applied_rules")
            execution_consistent = False
        if not label_correct:
            errors.append("declared_decision_disagrees_with_fields")

    # Keep the stringent historical interface diagnostic, but do not reuse it
    # as the denominator for separate effect and deliverable measures.
    valid = bool(identity_correct and question_free and execution_consistent and label_correct)

    scope_supported = True
    applied_rule_checks = []
    if present and arm != "A":
        for rule in output.applied_rules:
            check = _rule_support(rule, history_truth)
            applied_rule_checks.append({"field": rule.field, **check})
            if check["violations"] or check["render_errors"]:
                scope_supported = False
        if not scope_supported:
            errors.append("applied_rule_has_unsupported_scope_or_effect")

    retained_consistent = True
    if arm in ("C", "D"):
        if preparation is None:
            errors.append("missing_preparation")
            retained_consistent = False
        elif present:
            adopted = [candidate.rule for candidate in preparation.candidates
                       if candidate.status == "adopt"
                       and candidate.rule.scope.applies_to(task.context) == "match"]
            try:
                probes = [*history_truth.scope_probes, task]
                retained_consistent = (
                    _signature(output.applied_rules, probes) == _signature(adopted, probes)
                    and actual == render_rules(task, adopted)
                )
            except (ValueError, KeyError, TypeError):
                retained_consistent = False
            if not retained_consistent:
                errors.append("output_disagrees_with_adopted_preparation")

    complete = bool(identity_correct and question_free and output.completed)
    if present and not output.completed:
        errors.append("incomplete_deliverable")
    supported = bool(present and actual == expected and actual_decision == expected_decision)
    if present and not supported:
        errors.append("unsupported_or_missed_update")
    update_correct = bool(complete and execution_consistent and retained_consistent
                          and supported and scope_supported)
    world_compliant = bool(complete and actual == world)
    return {
        "valid_output": bool(valid),
        "task_identity_correct": identity_correct,
        "execution_consistent": bool(execution_consistent),
        "decision_label_correct": label_correct,
        "declared_decision": output.decision if present else None,
        "effective_decision": actual_decision,
        "update_correct": update_correct,
        "warranted": update_correct,
        "world_compliant": world_compliant,
        "completed_deliverable": complete,
        "warranted_world_compliant": update_correct and world_compliant,
        "unsupported_lucky_success": world_compliant and not update_correct,
        "partial_field_correctness": partial,
        "field_results": field_results,
        "expected_decision_for_arm": expected_decision,
        "expected_warranted_fields": expected,
        "world_fields": world,
        "rendered_fields": rendered,
        "unresolved_fields": conflicts,
        "retained_rules_consistent": retained_consistent,
        "applied_rules_supported_on_scope_probes": scope_supported,
        "applied_rule_checks": applied_rule_checks,
        "errors": errors,
    }


def evaluate_preparation(
    history_truth: HistoryTruth, history: History, prep: Preparation | None,
) -> dict[str, Any]:
    """Inspect fixed candidate targets and all submitted rules on frozen probes."""
    if history_truth.history_id != history.history_id:
        raise ValueError("history/evaluator truth identity mismatch")
    probes = history_truth.scope_probes
    if not probes:
        raise ValueError("candidate evaluation requires frozen scope probes")
    candidates = prep.candidates if isinstance(prep, Preparation) else []
    known_refs = {record.record_id for record in history.records}
    candidate_rows = []
    for candidate in candidates:
        refs = candidate.evidence_ids + candidate.counterevidence_ids
        unknown = sorted(set(refs) - known_refs)
        traceable = (bool(refs) and not unknown
                     and len(candidate.evidence_ids) == len(set(candidate.evidence_ids))
                     and len(candidate.counterevidence_ids) == len(set(candidate.counterevidence_ids)))
        if candidate.status == "adopt" and not candidate.evidence_ids:
            traceable = False
        matches = [target for target in history_truth.candidate_targets
                   if _equivalent(candidate.rule, target.rule, probes)]
        support = _rule_support(candidate.rule, history_truth)
        violations, scope_errors = support["violations"], support["scope_errors"]
        render_errors, changed = support["render_errors"], support["changed"]
        adopted = candidate.status == "adopt"
        unsupported = adopted and bool(violations or render_errors or not traceable)
        candidate_rows.append({
            "candidate_id": candidate.candidate_id,
            "status": candidate.status,
            "traceable": traceable,
            "unknown_reference_ids": unknown,
            "matching_target_ids": [target.target_id for target in matches],
            "matching_expected_statuses": sorted({target.status for target in matches}),
            "status_correct": any(target.status == candidate.status for target in matches),
            "unsupported_adoption": unsupported,
            "scope_error_probes": scope_errors if adopted else [],
            "unsupported_effect_probes": violations if adopted else [],
            "changed_probes": changed,
            "render_errors": render_errors,
            "evidence_gap_present": bool(candidate.evidence_gap.strip()),
            "alternative_count": len(candidate.alternatives),
        })
    target_rows = []
    for target in history_truth.candidate_targets:
        matching = [row for row in candidate_rows if target.target_id in row["matching_target_ids"]]
        correct = [row for row in matching if row["status"] == target.status
                   and row["traceable"] and not row["render_errors"]
                   and not row["unsupported_adoption"]]
        jointly_correct = []
        if target.status == "adopt":
            eligible = [(candidate, row) for candidate, row in zip(candidates, candidate_rows)
                        if candidate.status == "adopt" and row["traceable"]
                        and not row["render_errors"] and not row["unsupported_adoption"]
                        and _effects_within(candidate.rule, target.rule, probes)]
            try:
                if eligible and _signature([candidate.rule for candidate, _ in eligible], probes) == _signature([target.rule], probes):
                    jointly_correct = [row for _, row in eligible]
            except (ValueError, KeyError, TypeError):
                pass
        correct_ids = sorted({row["candidate_id"] for row in [*correct, *jointly_correct]})
        target_rows.append({
            "target_id": target.target_id,
            "expected_status": target.status,
            "represented": bool(matching or jointly_correct),
            "status_covered": bool(correct_ids),
            "matching_candidate_ids": [row["candidate_id"] for row in matching],
            "correct_candidate_ids": correct_ids,
            "jointly_covering_candidate_ids": [row["candidate_id"] for row in jointly_correct],
            "omitted": not (matching or jointly_correct),
        })
    by_status = {}
    for status in ("adopt", "reject", "unresolved"):
        group = [row for row in target_rows if row["expected_status"] == status]
        by_status[status] = {"covered": sum(row["status_covered"] for row in group),
                             "total": len(group)}
    return {
        "preparation_present": isinstance(prep, Preparation),
        "targets": target_rows,
        "candidates": candidate_rows,
        "target_coverage": sum(row["status_covered"] for row in target_rows),
        "target_count": len(target_rows),
        "coverage_by_status": by_status,
        "missed_warranted_rules": by_status["adopt"]["total"] - by_status["adopt"]["covered"],
        "unsupported_adoptions": sum(row["unsupported_adoption"] for row in candidate_rows),
        "adopted_rules_with_scope_errors": sum(bool(row["scope_error_probes"]) for row in candidate_rows),
        "untraceable_candidates": sum(not row["traceable"] for row in candidate_rows),
        "omitted_targets": sum(row["omitted"] for row in target_rows),
    }


def _summary(rows: list[dict]) -> dict[str, Any]:
    n = len(rows)
    result = {"n": n}
    for metric in ("update_correct", "world_compliant", "completed_deliverable",
                   "warranted_world_compliant", "unsupported_lucky_success",
                   "execution_consistent", "decision_label_correct", "valid_output"):
        count = sum(bool(row.get(metric, False)) for row in rows)
        result[metric] = count
        result[f"{metric}_rate"] = count / n if n else None
    result["partial_field_correctness"] = (
        mean(row.get("partial_field_correctness", 0.0) for row in rows) if rows else None)
    return result


def _probe_summaries(rows: list[dict]) -> dict[str, Any]:
    result = {}
    for probe in ("diagnostic", "control"):
        selected = [row for row in rows if row.get("probe") == probe]
        result[probe] = _summary(selected)
        result[probe]["by_expected_decision"] = {
            decision: _summary([row for row in selected if row.get("expected_decision") == decision])
            for decision in ("apply", "keep")
        }
    return result


def aggregate(rows: list[dict]) -> dict[str, Any]:
    """Keep easy controls separate; average repetitions within each variant first."""
    by_arm = {arm: _probe_summaries([row for row in rows if row.get("arm") == arm])
              for arm in ("A", "B", "C", "D")}
    variants = sorted({row["scenario_id"] for row in rows})
    by_variant = {
        variant: {arm: _probe_summaries([row for row in rows
                                        if row.get("scenario_id") == variant and row.get("arm") == arm])
                  for arm in ("A", "B", "C", "D")}
        for variant in variants
    }
    primary_rates = {}
    control_rates = {}
    for arm in ("A", "B", "C", "D"):
        for probe, target in (("diagnostic", primary_rates), ("control", control_rates)):
            values = [by_variant[variant][arm][probe]["update_correct_rate"]
                      for variant in variants
                      if by_variant[variant][arm][probe]["n"]]
            target[arm] = mean(values) if values else None
    paired = {}
    for variant in variants:
        c = by_variant[variant]["C"]["diagnostic"]["update_correct_rate"]
        d = by_variant[variant]["D"]["diagnostic"]["update_correct_rate"]
        paired[variant] = d - c if c is not None and d is not None else None
    repetitions = sorted({row["repetition"] for row in rows})
    by_repetition = {
        str(rep): {arm: _probe_summaries([row for row in rows
                                        if row.get("repetition") == rep and row.get("arm") == arm])
                   for arm in ("A", "B", "C", "D")}
        for rep in repetitions
    }
    pairs = {}
    for pair in sorted({row["pair_id"] for row in rows}):
        selected = [row for row in rows if row.get("pair_id") == pair]
        pairs[pair] = {
            "scenario_ids": sorted({row["scenario_id"] for row in selected}),
            "by_arm": {arm: _probe_summaries([row for row in selected if row.get("arm") == arm])
                       for arm in ("A", "B", "C", "D")},
        }
    c, d = primary_rates["C"], primary_rates["D"]
    return {
        "primary": {"metric": "diagnostic_update_correct", "variant_mean_by_arm": primary_rates,
                    "D_minus_C": d - c if c is not None and d is not None else None,
                    "paired_variant_D_minus_C": paired},
        "control_variant_mean_by_arm": control_rates,
        "by_arm": by_arm, "by_variant": by_variant,
        "by_repetition": by_repetition, "pairs": pairs,
        "planned_rows_supplied": len(rows),
    }


def calibration_gates(rows: list[dict]) -> dict[str, Any]:
    """Check fixed denominators and separate warrant from observed field utility.

    B's absolute utility floor requires warranted, world-compliant deliverables.
    The B-minus-A utility gate uses actual world compliance for both arms, so a
    lucky but unwarranted A output still counts as observed output utility.
    Missing observations cannot silently lower A's comparison baseline.
    """
    design_errors = []
    if any(row.get("arm") not in ("A", "B", "C") for row in rows):
        design_errors.append("calibration_contains_non_ABC_arm")
    if len({row.get("repetition") for row in rows}) != 1:
        design_errors.append("calibration_requires_one_repetition")
    grouped = {arm: [row for row in rows if row.get("arm") == arm] for arm in ("A", "B", "C")}
    identities = {}
    for arm, selected in grouped.items():
        keys = [(row.get("scenario_id"), row.get("probe")) for row in selected]
        if len(keys) != len(set(keys)):
            design_errors.append(f"{arm}_duplicate_case")
        diagnostic = [row for row in selected if row.get("probe") == "diagnostic"]
        controls = [row for row in selected if row.get("probe") == "control"]
        if len(selected) != 16 or len(diagnostic) != 8 or len(controls) != 8:
            design_errors.append(f"{arm}_requires_eight_diagnostics_and_eight_controls")
        for decision in ("apply", "keep"):
            if sum(row.get("expected_decision") == decision for row in diagnostic) != 4:
                design_errors.append(f"{arm}_requires_four_{decision}_diagnostics")
        if sum(bool(row.get("recoverable")) for row in diagnostic) != 7:
            design_errors.append(f"{arm}_requires_seven_recoverable_diagnostics")
        recoverable = [row for row in diagnostic if row.get("recoverable")]
        for metric in ("world_compliant", "warranted_world_compliant"):
            if any(type(row.get(metric)) is not bool for row in recoverable):
                design_errors.append(f"{arm}_recoverable_{metric}_missing_or_invalid")
        if any(row.get("warranted_world_compliant") is True
               and row.get("world_compliant") is False for row in recoverable):
            design_errors.append(f"{arm}_warranted_world_compliance_without_world_compliance")
        identities[arm] = {(row.get("scenario_id"), row.get("probe"),
                            row.get("expected_decision"), bool(row.get("recoverable")))
                           for row in selected}
    if not (identities["A"] == identities["B"] == identities["C"]):
        design_errors.append("arms_do_not_share_the_same_fixed_cases")
    scores = {}
    for arm, selected in grouped.items():
        diagnostic = [row for row in selected if row.get("probe") == "diagnostic"]
        controls = [row for row in selected if row.get("probe") == "control"]
        recoverable = [row for row in diagnostic if row.get("recoverable")]
        scores[arm] = {
            "diagnostic_correct": sum(bool(row.get("update_correct")) for row in diagnostic),
            "diagnostic_total": len(diagnostic),
            "apply_correct": sum(bool(row.get("update_correct")) for row in diagnostic
                                 if row.get("expected_decision") == "apply"),
            "keep_correct": sum(bool(row.get("update_correct")) for row in diagnostic
                                if row.get("expected_decision") == "keep"),
            "control_correct": sum(bool(row.get("update_correct")) for row in controls),
            "control_total": len(controls),
            "recoverable_warranted_deliverables": sum(row.get("warranted_world_compliant") is True
                                                     for row in recoverable),
            "recoverable_world_compliant_deliverables": sum(row.get("world_compliant") is True
                                                           for row in recoverable),
            "recoverable_total": len(recoverable),
        }
    a, b, c = scores["A"], scores["B"], scores["C"]
    checks = {
        "fixed_design": not design_errors,
        "B_diagnostic_at_least_6_of_8": b["diagnostic_correct"] >= 6,
        "C_diagnostic_between_4_and_7_of_8": 4 <= c["diagnostic_correct"] <= 7,
        "C_apply_at_least_2_of_4": c["apply_correct"] >= 2,
        "C_keep_at_least_2_of_4": c["keep_correct"] >= 2,
        "B_controls_at_least_7_of_8": b["control_correct"] >= 7,
        "C_controls_at_least_7_of_8": c["control_correct"] >= 7,
        "B_recoverable_deliverables_at_least_6_of_7": b["recoverable_warranted_deliverables"] >= 6,
        "B_recoverable_world_compliant_at_least_A_plus_2": (
            b["recoverable_world_compliant_deliverables"]
            >= a["recoverable_world_compliant_deliverables"] + 2),
    }
    return {"passed": all(checks.values()), "checks": checks, "scores": scores,
            "design_errors": design_errors,
            "failed_checks": [name for name, passed in checks.items() if not passed]}
