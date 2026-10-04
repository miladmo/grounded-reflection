"""Allowlisted public payloads. No private Case object crosses this boundary."""

import json
from pathlib import Path

from reflectai_v03.context import render_rules, retained_rules
from reflectai_v03.contracts import History, Preparation, Task


def history_payload(history: History) -> dict:
    if type(history) is not History:
        raise TypeError('Only the public History contract is accepted.')
    return history.model_dump(mode='json')


def preparation_payload(history: History, previous: Preparation | None = None) -> dict:
    payload = {'history': history_payload(history)}
    if previous is not None:
        if type(previous) is not Preparation:
            raise TypeError('Expected a validated public Preparation.')
        payload['previous_preparation'] = previous.model_dump(mode='json')
    return payload


def generation_payload(task: Task, history: History, arm: str,
                       preparation: Preparation | None = None) -> dict:
    if arm not in ('A', 'B', 'C'):
        raise ValueError('v0.4 supports A, B and C only.')
    if type(task) is not Task:
        raise TypeError('Only the public Task contract is accepted.')
    public = history_payload(history)
    payload = {key: public[key] for key in (
        'initial_configuration', 'assumptions', 'field_dictionary')}
    payload['task'] = task.model_dump(mode='json')
    if arm == 'B':
        payload['history'] = public
    if arm == 'C':
        if preparation is None:
            raise ValueError('C generation requires completed preparation.')
        rules = retained_rules(preparation, history)
        applicable = [r for r in rules if r.scope.applies_to(task.context) == 'match']
        render_rules(task, applicable)
        payload['instructions'] = [r.model_dump(mode='json') for r in applicable]
    return payload


def prompt_for(stage: str, payload: dict, prompt_dir: Path) -> str:
    filenames = {'C1': 'prepare_C_v1.txt', 'C2': 'review_C_v1.txt',
                 'generate': 'generate_v1.txt'}
    if stage not in filenames:
        raise ValueError('Unknown v0.4 stage.')
    expected = {'history'} if stage == 'C1' else {'history', 'previous_preparation'}
    if stage != 'generate' and set(payload) != expected:
        raise ValueError('Preparation payload has undeclared properties.')
    if stage == 'generate':
        required = {'task', 'initial_configuration', 'assumptions', 'field_dictionary'}
        if not required <= set(payload) or set(payload) - required - {'history', 'instructions'}:
            raise ValueError('Generation payload has undeclared properties.')
        if {'history', 'instructions'} <= set(payload):
            raise ValueError('History and retained-guidance modes cannot be combined.')
    return ((prompt_dir / filenames[stage]).read_text(encoding='utf-8').strip()
            + '\n\n' + (prompt_dir / 'shared_contract_v1.txt').read_text(encoding='utf-8').strip()
            + '\nPAYLOAD\n' + json.dumps(payload, ensure_ascii=False, allow_nan=False))
