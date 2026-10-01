"""Common context rendering; reflection-only checks establish traceability."""

from ..workflow import verify_references
from .contracts import History, Preparation


def retained_preparation(preparation: Preparation, history: History, grounded: bool):
    retained, rejected = [], []
    for index, item in enumerate(preparation.requirements):
        issues = []
        if grounded and item.decision == 'adopt':
            if item.hypothesis is None:
                issues.append('Adoption requires a grounded hypothesis')
            else:
                issues.extend(verify_references(item.hypothesis, history.episodes))
                if item.rule.scope is None or not item.rule.scope.is_within(item.hypothesis.scope):
                    issues.append('Rule scope exceeds its hypothesis scope')
        if issues:
            rejected.append({'index': index, 'reasons': issues})
        else:
            retained.append(item)
    return Preparation(requirements=retained, notes=preparation.notes), rejected


def render_context(preparation: Preparation, context: dict[str, str]):
    rules, questions = [], set()
    for item in preparation.requirements:
        scope = item.rule.scope
        match = scope.applies_to(context) if scope else 'match'
        if match == 'mismatch':
            continue
        if match == 'unknown':
            questions.update(k for k in scope.match if k not in context)
        elif item.decision == 'adopt':
            rules.append({'field': item.rule.field, 'operator': item.rule.operator,
                          'value': item.rule.value})
        else:
            questions.update(item.missing_fields)
    return {'rules': rules, 'unresolved_context_fields': sorted(questions)}
