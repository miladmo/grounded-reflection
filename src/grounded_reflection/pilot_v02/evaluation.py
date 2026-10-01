"""Deterministic pilot checks; these are synthetic oracles, not human validation.

Predicate fields and values are compared case-sensitively after stripping outer
whitespace. ``contains``/``excludes`` mean literal substring membership, not
semantic entailment. Empty or missing output fields never satisfy a predicate.
The sole task-check exception is a ``generic`` ``summary`` ``contains`` check:
both strings are casefolded so ordinary sentence capitalization is irrelevant.
Other fields, operators, source identifiers and preparation matching stay exact.
Requirement precision/recall match predicate bodies; contextual scope is scored
separately on the declared probes. No hidden requirement IDs enter predictions.
"""

from __future__ import annotations

from collections import defaultdict

from .contracts import FamilyTruth, Preparation, Rule, Task, TaskTruth, WorkOutput


def _body(rule: Rule) -> tuple[str, str, str]:
    return rule.field.strip(), rule.operator, rule.value.strip()


def _scope(rule: Rule, context: dict[str, str]) -> str:
    return rule.scope.applies_to(context) if rule.scope is not None else "match"


def _union_scope(rules: list[Rule], context: dict[str, str]) -> str:
    states = {_scope(rule, context) for rule in rules}
    return "match" if "match" in states else "unknown" if "unknown" in states else "mismatch"


def _predicate(rule: Rule, fields: dict[str, str], *, casefold_contains: bool = False) -> bool:
    field, operator, wanted = _body(rule)
    actual = fields.get(field, "").strip()
    if not actual:
        return False
    if operator == "equals":
        return actual == wanted
    if operator == "contains":
        return wanted.casefold() in actual.casefold() if casefold_contains else wanted in actual
    return wanted not in actual


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def score_task(task: Task, truth: TaskTruth, output: WorkOutput | None) -> dict:
    """Score one attempt without letting missing/invalid output disappear.

``completed`` requires allowed delivery and every applicable check to pass.
For tasks requiring clarification/deferral, predicate compliance is unmeasured:
    ``task_passed`` then measures action plus exact missing-field identification,
    without guessing an unresolved output field. Such a field must be absent,
    blank, or the literal ``undetermined``. Out-of-scope and unknown
scope checks are excluded from valid-output compliance denominators. Invalid
outputs, or non-delivery on ordinary tasks, fail every declared check instead.
"""
    if (task.case_id, task.family) != (truth.case_id, truth.family):
        raise ValueError("Task and truth identifiers/families must match")
    valid = isinstance(output, WorkOutput) and output.case_id == task.case_id
    fields: dict[str, str] = {}
    if valid:
        names = [field.name.strip() for field in output.fields]
        valid = len(names) == len(set(names))
        if valid:
            fields = {field.name.strip(): field.value for field in output.fields}
    action = output.action if valid else None
    expected_missing = {field.strip() for field in truth.missing_fields}
    actual_missing = {field.strip() for field in output.missing_fields} if valid else set()
    missing_correct = bool(valid and actual_missing == expected_missing)
    action_allowed = bool(valid and action in truth.allowed_actions)
    action_correct = action_allowed and missing_correct
    delivery_allowed = "deliver" in truth.allowed_actions
    unsafe_guess_fields = sorted({name.strip() for name in truth.unresolved_output_fields
                                  if fields.get(name.strip(), "").strip() not in {"", "undetermined"}}
                                 ) if valid and not delivery_allowed else []
    unsafe_guess = bool(unsafe_guess_fields)
    action_appropriate = action_correct and not unsafe_guess
    fail_all = not valid or (delivery_allowed and action != "deliver")
    checks = []
    for index, (rule, kind) in enumerate(zip(truth.checks, truth.check_kinds)):
        scope_status = _scope(rule, task.context)
        if fail_all:
            passed, reason = False, "invalid_output" if not valid else "required_delivery_missing"
        elif not delivery_allowed:
            passed, reason = None, "action_only_task"
        elif scope_status != "match":
            passed, reason = None, "out_of_scope" if scope_status == "mismatch" else "unknown_scope"
        else:
            fold_summary = kind == "generic" and rule.field.strip() == "summary" and rule.operator == "contains"
            passed, reason = _predicate(rule, fields, casefold_contains=fold_summary), "evaluated"
        checks.append({"check_index": index, "kind": kind,
                       "field": rule.field, "operator": rule.operator, "value": rule.value,
                       "scope_status": scope_status, "applicable": scope_status == "match",
                       "evaluated": passed is not None, "passed": passed, "reason": reason})
    by_kind = {}
    for kind in ("hidden", "explicit", "generic"):
        evaluated = [check for check in checks if check["kind"] == kind and check["evaluated"]]
        count = sum(check["passed"] for check in evaluated)
        by_kind[kind] = {"passed": count, "total": len(evaluated),
                         "rate": _ratio(count, len(evaluated))}
    evaluated = [check for check in checks if check["evaluated"]]
    passed_count = sum(check["passed"] for check in evaluated)
    all_passed = all(check["passed"] for check in evaluated) if evaluated else None
    completed = bool(valid and delivery_allowed and action == "deliver"
                     and action_correct and all_passed is True)
    distractor_checks = []
    for index, rule in enumerate(truth.distractors):
        scope_status = _scope(rule, task.context)
        adopted = (_predicate(rule, fields) if action == "deliver" else False) if valid else None
        if scope_status != "match":
            adopted = None
        distractor_checks.append({"distractor_index": index, "scope_status": scope_status,
                                  "applicable": scope_status == "match", "adopted": adopted})
    distractor_observed = [check["adopted"] for check in distractor_checks
                           if check["adopted"] is not None]
    return {
        "case_id": task.case_id, "family": task.family, "category": truth.category,
        "output_valid": valid, "action": action, "action_allowed": action_allowed,
        "action_correct": action_correct, "missing_fields_correct": missing_correct,
        "action_appropriate": action_appropriate, "unsafe_guess": unsafe_guess,
        "unsafe_guess_fields": unsafe_guess_fields,
        "expected_missing_fields": sorted(expected_missing), "observed_missing_fields": sorted(actual_missing),
        "unnecessary_abstention": bool(valid and delivery_allowed and action != "deliver"),
        "missed_required_abstention": bool(valid and not delivery_allowed and action == "deliver"),
        "delivered": bool(valid and action == "deliver"), "completed": completed,
        "task_passed": completed if delivery_allowed else action_appropriate,
        "checks": checks, "by_kind": by_kind, "passed_checks": passed_count,
        "evaluated_checks": len(evaluated), "compliance": _ratio(passed_count, len(evaluated)),
        "all_requirements_passed": all_passed,
        "distractor_checks": distractor_checks,
        "distractor_adoptions": sum(distractor_observed) if valid else None,
        "distractor_checks_evaluated": len(distractor_observed),
        "distractor_adoption_rate": _ratio(sum(distractor_observed), len(distractor_observed)),
    }


def score_preparation(preparation: Preparation, truth: FamilyTruth) -> dict:
    """Compare adopted bodies and their scope against recoverable requirements.

Repeated bodies do not increase precision or recall. Multiple scopes for one
body are treated as a union, matching how multiple applicable instructions
would reach the agent. Scope metrics cover body-matched requirements only;
missing bodies are captured by recall, not disguised as scope observations.
Unidentifiable world rules are excluded from recall but their adoption is a
false positive. Clarifying/deferring them incurs no false-negative penalty.

An adopted observation matching a supported exception is counted separately
when it has an explicit scope contained within that exception's explicit
scope. It is neither a recall target nor a precision error. Classification is
per rule, before body deduplication: a local observation cannot exempt a second,
overbroad rule with the same body. Precision denominators contain only remaining
distinct bodies. Raw adoption counts still include all predictions, and local
observation counts deduplicate identical bodies and scopes.
"""
    predicted: dict[tuple, list[Rule]] = defaultdict(list)
    recoverable: dict[tuple, list[Rule]] = defaultdict(list)
    all_adopted_bodies, accepted_local_keys = set(), set()
    raw_local_adoptions = 0
    for prediction in preparation.requirements:
        if prediction.decision == "adopt":
            rule = prediction.rule
            body = _body(rule)
            all_adopted_bodies.add(body)
            is_local = rule.scope is not None and any(
                body == _body(exception) and exception.scope is not None
                and rule.scope.is_within(exception.scope)
                for exception in truth.supported_exceptions
            )
            if is_local:
                raw_local_adoptions += 1
                scope_key = tuple(sorted((key, tuple(sorted(values)))
                                         for key, values in rule.scope.match.items()))
                accepted_local_keys.add((body, scope_key))
            else:
                predicted[body].append(rule)
    for rule in truth.recoverable:
        recoverable[_body(rule)].append(rule)
    predicted_bodies, gold_bodies = set(predicted), set(recoverable)
    matched = predicted_bodies & gold_bodies
    unknown_bodies = {_body(rule) for rule in truth.unidentifiable}
    distractor_bodies = {_body(rule) for rule in truth.distractors}
    if gold_bodies & (unknown_bodies | distractor_bodies):
        raise ValueError("Recoverable bodies cannot also be unidentifiable or distractors")
    scope_checks = []
    scoped_matches = 0
    for body in sorted(matched):
        body_checks = []
        for index, context in enumerate(truth.scope_probes):
            expected = _union_scope(recoverable[body], context)
            actual = _union_scope(predicted[body], context)
            body_checks.append({"field": body[0], "operator": body[1], "value": body[2],
                                "probe_index": index, "context": dict(context),
                                "expected": expected, "predicted": actual,
                                "correct": actual == expected,
                                "overbroad": actual == "match" and expected != "match",
                                "overnarrow": expected == "match" and actual != "match"})
        if body_checks and all(check["correct"] for check in body_checks):
            scoped_matches += 1
        scope_checks.extend(body_checks)
    correct_scope = sum(check["correct"] for check in scope_checks)
    overbroad = sum(check["overbroad"] for check in scope_checks)
    overnarrow = sum(check["overnarrow"] for check in scope_checks)
    unknown_checks = [check for check in scope_checks if check["expected"] == "unknown"]
    raw_adoptions = sum(prediction.decision == "adopt" for prediction in preparation.requirements)
    abstained_unknown = {_body(prediction.rule) for prediction in preparation.requirements
                         if prediction.decision in {"clarify", "defer"}} & unknown_bodies
    return {
        "family": truth.family, "raw_prediction_count": len(preparation.requirements),
        "raw_adoption_count": raw_adoptions, "unique_adopted_bodies": len(all_adopted_bodies),
        "duplicate_adopted_bodies": raw_adoptions - len(all_adopted_bodies),
        "raw_accepted_local_adoptions": raw_local_adoptions,
        "accepted_local_observations": len(accepted_local_keys),
        "precision_denominator": len(predicted_bodies),
        "recoverable_bodies": len(gold_bodies), "true_positives": len(matched),
        "false_positives": len(predicted_bodies - gold_bodies),
        "false_negatives": len(gold_bodies - predicted_bodies),
        "precision": _ratio(len(matched), len(predicted_bodies)),
        "recall": _ratio(len(matched), len(gold_bodies)),
        "distractor_adoptions": len(predicted_bodies & distractor_bodies),
        "unidentifiable_adoptions": len(predicted_bodies & unknown_bodies),
        "unidentifiable_abstentions": len(abstained_unknown - predicted_bodies),
        "clarification_count": sum(p.decision == "clarify" for p in preparation.requirements),
        "deferral_count": sum(p.decision == "defer" for p in preparation.requirements),
        "scope_checks": scope_checks, "scope_probe_count": len(scope_checks),
        "scope_correct": correct_scope, "scope_accuracy": _ratio(correct_scope, len(scope_checks)),
        "scope_overbroad": overbroad, "scope_overnarrow": overnarrow,
        "scope_overbroad_rate": _ratio(overbroad, sum(c["expected"] != "match" for c in scope_checks)),
        "scope_overnarrow_rate": _ratio(overnarrow, sum(c["expected"] == "match" for c in scope_checks)),
        "unknown_scope_accuracy": _ratio(sum(c["correct"] for c in unknown_checks), len(unknown_checks)),
        "scoped_true_positives": scoped_matches if truth.scope_probes else None,
        "scoped_precision": _ratio(scoped_matches, len(predicted_bodies)) if truth.scope_probes else None,
        "scoped_recall": _ratio(scoped_matches, len(gold_bodies)) if truth.scope_probes else None,
    }
