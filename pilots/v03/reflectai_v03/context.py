"""One execution interface for every arm; uncertainty never becomes a task blocker."""

from .contracts import History, Preparation, Rule, Task


def render_rules(task: Task, rules: list[Rule]) -> dict[str, str]:
    """Apply conjunction-scoped rules to the immutable baseline.

    Unknown context does not match. Rules are order-independent; two different
    assignments to the same field are an invalid configuration, not last-wins.
    Appended values always use the original title, never another rule's output.
    """
    baseline = {field.name: field.value for field in task.baseline_fields}
    changes: dict[str, str | None] = {}
    for rule in rules:
        if rule.scope.applies_to(task.context) != 'match':
            continue
        if rule.operation == 'omit':
            value = None
        elif rule.operation == 'set_literal':
            value = rule.value
        else:
            if rule.value not in task.facts:
                raise ValueError(f'unknown fact key: {rule.value}')
            value = task.facts[rule.value]
            if rule.operation == 'append_fact':
                if rule.field not in baseline:
                    raise ValueError(f'append requires baseline field: {rule.field}')
                value = baseline[rule.field] + rule.separator + value
        if rule.field in changes and changes[rule.field] != value:
            raise ValueError(f'conflicting applicable rules for {rule.field}')
        changes[rule.field] = value
    result = dict(baseline)
    for field, value in changes.items():
        if value is None:
            result.pop(field, None)
        else:
            result[field] = value
    return result


def retained_rules(preparation: Preparation, history: History) -> list[Rule]:
    """Symmetric traceability validation, not a semantic truth filter."""
    known = {record.record_id for record in history.records}
    result = []
    for candidate in preparation.candidates:
        refs = candidate.evidence_ids + candidate.counterevidence_ids
        if any(reference not in known for reference in refs):
            raise ValueError(f'unknown evidence reference in {candidate.candidate_id}')
        if len(candidate.evidence_ids) != len(set(candidate.evidence_ids)):
            raise ValueError('duplicate supporting evidence reference')
        if len(candidate.counterevidence_ids) != len(set(candidate.counterevidence_ids)):
            raise ValueError('duplicate counterevidence reference')
        if candidate.status == 'adopt':
            if not candidate.evidence_ids:
                raise ValueError('adopted candidates require an observed evidence reference')
            result.append(candidate.rule)
    return result


def generation_payload(task: Task, history: History, arm: str,
                       preparation: Preparation | None = None) -> dict:
    if arm not in ('A', 'B', 'C', 'D'):
        raise ValueError('unknown arm')
    payload = {
        'task': task.model_dump(mode='json'),
        'initial_configuration': history.initial_configuration,
        'assumptions': history.assumptions,
        'field_dictionary': history.field_dictionary,
    }
    if arm == 'B':
        payload['history'] = history.model_dump(mode='json')
    if arm in ('C', 'D'):
        if preparation is None:
            raise ValueError('adaptation arms require complete preparation')
        rules = retained_rules(preparation, history)
        applicable = [rule for rule in rules if rule.scope.applies_to(task.context) == 'match']
        render_rules(task, applicable)  # Detect contradictory executable guidance.
        payload['instructions'] = [rule.model_dump(mode='json') for rule in applicable]
    return payload
