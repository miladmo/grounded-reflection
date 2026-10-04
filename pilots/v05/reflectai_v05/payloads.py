"""Allowlisted public payloads for A, B, C and D, with the per-call input budget.

Every call's input (system message with schema plus user prompt with payload) must
stay within CALL_INPUT_TOKENS, counted with the v0.4 contract-test ratio of 3.10
characters per token. Variable record lists are filled up to that limit.
"""

from __future__ import annotations

import json
from pathlib import Path

from reflectai_v03.context import render_rules, retained_rules
from reflectai_v03.contracts import History, Preparation, Record, Task, WorkOutput
from reflectai_v03.wire import strict_response_schema

from .contracts import PublicFrame
from .dcontracts import Register
from .retrieval import record_chars, select_records

CALL_INPUT_TOKENS = 24_000
CHARS_PER_TOKEN = 3.10
CALL_INPUT_CHARS = int(CALL_INPUT_TOKENS * CHARS_PER_TOKEN)
SAFETY_CHARS = 1_500
# Same system-message prefix as reflectai_v04.fhgenie_transport; a test keeps them in sync.
SYSTEM_PREFIX = ('Return one JSON object conforming to the JSON schema below. '
                 'Return only the JSON object, without markdown fences or extra text. '
                 'Do not use tools. JSON schema: ')
PROMPT_DIR = Path(__file__).resolve().parents[1] / 'prompts'
PROMPTS = {'generate': 'generate_v1.txt', 'C1': 'prepare_chunk_C_v1.txt', 'C2': 'consolidate_C_v1.txt',
           'D-index': 'd_index_v1.txt', 'D-round': 'd_round_v1.txt', 'D-final': 'd_final_v1.txt'}
CONTRACTS = {'generate': WorkOutput, 'C1': Preparation, 'C2': Preparation,
             'D-index': Register, 'D-round': Register, 'D-final': Preparation}
B_SELECTION = ('Registrations first, then accepted reviews that list the target field, then all other '
               'records; within the last two groups by the number of context attributes shared with the '
               'task and then by recency; added in this order until the call input budget was full.')


class BudgetExceeded(ValueError):
    pass


def schema_for(stage: str) -> dict:
    return strict_response_schema(CONTRACTS[stage])


def prompt_for(stage: str, payload: dict, prompt_dir: Path = PROMPT_DIR) -> str:
    return ((prompt_dir / PROMPTS[stage]).read_text(encoding='utf-8').strip() + '\n\n'
            + (prompt_dir / 'shared_contract_v1.txt').read_text(encoding='utf-8').strip()
            + '\nPAYLOAD\n' + json.dumps(payload, ensure_ascii=False, allow_nan=False))


def input_chars(stage: str, prompt: str) -> int:
    schema = json.dumps(schema_for(stage), ensure_ascii=False, allow_nan=False, separators=(',', ':'))
    return len(SYSTEM_PREFIX) + len(schema) + len(prompt)


def _public(history: History) -> dict:
    return {'initial_configuration': history.initial_configuration, 'assumptions': history.assumptions,
            'field_dictionary': history.field_dictionary}


def registrations(history: History) -> list[dict]:
    return [r.model_dump(mode='json') for r in history.records
            if json.loads(r.observation).get('event') == 'register_version']


def _fit(stage: str, payload: dict, key: str, records: list[Record]) -> tuple[str, int]:
    """Fill payload[key] with the longest prefix of records that keeps the call in budget."""
    payload[key] = []
    empty = input_chars(stage, prompt_for(stage, payload))
    if empty + SAFETY_CHARS > CALL_INPUT_CHARS:
        raise BudgetExceeded(f'{stage} payload exceeds the call budget before records are added')
    room, chosen, used = CALL_INPUT_CHARS - SAFETY_CHARS - empty, [], 0
    for record in records:
        size = record_chars(record)
        if used + size > room:
            break
        chosen.append(record.model_dump(mode='json'))
        used += size
    payload[key] = chosen
    prompt = prompt_for(stage, payload)
    if input_chars(stage, prompt) > CALL_INPUT_CHARS:
        raise BudgetExceeded(f'{stage} prompt exceeds the call budget')
    return prompt, len(chosen)


def generation_prompt(arm: str, task: Task, history: History, frame: PublicFrame,
                      preparation: Preparation | None = None) -> tuple[str, dict]:
    payload = {**_public(history), 'task': task.model_dump(mode='json')}
    info = {}
    if arm == 'B':
        payload['history_excerpt'] = {'selection': B_SELECTION, 'records_total': len(history.records), 'records': []}
        base = input_chars('generate', prompt_for('generate', payload))
        room = CALL_INPUT_CHARS - SAFETY_CHARS - base
        selected = select_records(history, task, frame, room)
        payload['history_excerpt']['records'] = [r.model_dump(mode='json') for r in selected]
        info['selected_record_ids'] = [r.record_id for r in selected]
    elif arm in ('C', 'D'):
        if preparation is None:
            raise ValueError('C and D generation require a completed preparation')
        rules = retained_rules(preparation, history)
        applicable = [r for r in rules if r.scope.applies_to(task.context) == 'match']
        render_rules(task, applicable)
        payload['instructions'] = [r.model_dump(mode='json') for r in applicable]
    elif arm != 'A':
        raise ValueError('unknown arm')
    prompt = prompt_for('generate', payload)
    if input_chars('generate', prompt) > CALL_INPUT_CHARS:
        raise BudgetExceeded('generation prompt exceeds the call budget')
    return prompt, info


def chunk_prompt(history: History, remaining: list[Record], previous: Preparation | None, index: int):
    payload = {**_public(history), 'chunk_index': index, 'records_not_yet_shown': 0,
               'registrations': registrations(history),
               'previous_preparation': previous.model_dump(mode='json') if previous else None}
    prompt, count = _fit('C1', payload, 'records', remaining)
    if count == 0:
        raise BudgetExceeded('no record fits into a chunk')
    payload['records_not_yet_shown'] = len(remaining) - count
    prompt = prompt_for('C1', payload)
    return prompt, count


def cited(history: History, ids: list[str]) -> list[Record]:
    wanted = set(ids)
    return [r for r in history.records if r.record_id in wanted]


def consolidation_prompt(history: History, previous: Preparation) -> tuple[str, dict]:
    ids = [i for c in previous.candidates for i in c.evidence_ids + c.counterevidence_ids]
    payload = {**_public(history), 'registrations': registrations(history),
               'previous_preparation': previous.model_dump(mode='json'), 'records_shown': ''}
    everything = [r for r in history.records if json.loads(r.observation).get('event') != 'register_version']
    payload['records_shown'] = 'complete history'
    prompt, count = _fit('C2', payload, 'cited_records', everything)
    if count < len(everything):
        payload['records_shown'] = 'records cited by previous_preparation, up to the call budget'
        prompt, count = _fit('C2', payload, 'cited_records', cited(history, ids))
    return prompt, {'records_shown': payload['records_shown'], 'records_included': count}


def d_index_prompt(history: History, index: dict) -> str:
    payload = {**_public(history), 'registrations': registrations(history), 'index': index}
    prompt = prompt_for('D-index', payload)
    if input_chars('D-index', prompt) > CALL_INPUT_CHARS:
        raise BudgetExceeded('D index prompt exceeds the call budget')
    return prompt


def d_round_room(history: History, register: Register, round_number: int, rounds_remaining: int) -> int:
    payload = {**_public(history), 'registrations': registrations(history),
               'register': register.model_dump(mode='json'), 'round': round_number,
               'rounds_remaining': rounds_remaining, 'results': []}
    return CALL_INPUT_CHARS - SAFETY_CHARS - input_chars('D-round', prompt_for('D-round', payload))


def d_round_prompt(history: History, register: Register, round_number: int, rounds_remaining: int,
                   results: list[dict]) -> str:
    payload = {**_public(history), 'registrations': registrations(history),
               'register': register.model_dump(mode='json'), 'round': round_number,
               'rounds_remaining': rounds_remaining, 'results': results}
    prompt = prompt_for('D-round', payload)
    if input_chars('D-round', prompt) > CALL_INPUT_CHARS:
        raise BudgetExceeded('D round prompt exceeds the call budget')
    return prompt


def d_final_prompt(history: History, register: Register) -> tuple[str, int]:
    ids = [i for h in register.hypotheses for i in h.evidence_ids + h.counterevidence_ids]
    payload = {**_public(history), 'registrations': registrations(history),
               'register': register.model_dump(mode='json')}
    return _fit('D-final', payload, 'cited_records', cited(history, ids))
