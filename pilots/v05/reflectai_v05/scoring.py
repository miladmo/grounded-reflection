"""Primary outcome: the decision implied by the executed output fields (all arms).

A task is correct when the produced fields equal the oracle's expected fields: the
consensus alternative for 'apply', the baseline for 'keep', unresolved cases and
out-of-scope controls. Declared rules and decision labels are secondary diagnostics
and never change the primary outcome (protocol, Measurement).
"""

from __future__ import annotations

from reflectai_v03.contracts import Task, WorkOutput

from .contracts import TaskTruth


def _fields(items) -> dict[str, str]:
    return {item.name: item.value for item in items}


def score_task(task: Task, truth: TaskTruth, output: WorkOutput | None) -> dict:
    if output is None:
        return {'task_id': truth.task_id, 'task_type': truth.task_type, 'correct': False,
                'reason': 'missing_or_invalid_output', 'implied_decision': None,
                'label_consistent': None, 'world_compliant': False}
    produced = _fields(output.fields)
    baseline = _fields(task.baseline_fields)
    implied = 'keep' if produced == baseline else 'apply'
    correct = output.task_id == task.task_id and produced == truth.expected_fields
    if output.task_id != task.task_id:
        reason = 'wrong_task_id'
    elif correct:
        reason = None
    elif implied != truth.expected_decision:
        reason = 'missed_change' if truth.expected_decision == 'apply' else 'unsupported_change'
    else:
        reason = 'wrong_field_values'
    return {'task_id': truth.task_id, 'task_type': truth.task_type, 'correct': correct, 'reason': reason,
            'implied_decision': implied, 'label_consistent': output.decision == implied,
            'world_compliant': produced == truth.world_fields,
            'declared_rule_count': len(output.applied_rules)}
