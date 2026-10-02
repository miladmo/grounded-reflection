"""Export four v0.5 review examples (one per setting) from the separate review seeds."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

from . import hclass
from .backend import write_json
from .config import SEEDS
from .data import generate_future_tasks, generate_histories
from .oracle import configuration_bit, infer
from .storage import seal, source_binding

# One example per setting: four families, both directions, each hard type twice.
SELECTION = {'K-S': ('transfer_change', 'omit'), 'K-L': ('unidentifiable', 'omit'),
             'U-S': ('unidentifiable', 'add'), 'U-L': ('transfer_change', 'add')}


def _cell_text(frame, cell):
    context = frame.context_of(cell)
    return ', '.join(f'{name}={context[name]}' for name in frame.attributes)


def _example_markdown(case, tasks) -> str:
    oracle = infer(case.history)
    frame = oracle.frame
    names = frame.attribute_names
    option = frame.field_option
    baseline_has_field = option.field in frame.baseline_template
    lines = [f'# {case.setting} {case.family}: {case.hard_type.replace("_", " ")}', '',
             f'History `{case.history.history_id}`, {len(case.history.records)} records. Synthetic review example; '
             'not a scored case.', '',
             '## Public configuration', '',
             f'* Attributes (predicate tests the second listed value): '
             + '; '.join(f'`{n}` {v[0]} / **{v[1]}**' for n, v in frame.attributes.items()),
             f'* Candidate attributes ({frame.hypothesis_class}): ' + ', '.join(f'`{n}`' for n in frame.candidate_attributes),
             f"* Target field `{option.field}`: baseline {'includes' if baseline_has_field else 'does not include'} it; "
             f"the alternative is `{option.operation}`" + (f' with `{option.value}`' if option.value else '') + '.', '',
             '## Binding approvals (oracle input)', '',
             '| Record | Reviewer | Context | Configuration |', '| --- | --- | --- | --- |']
    records = {r.record_id: r for r in case.history.records}
    for record_id in oracle.binding_records:
        record = records[record_id]
        event = json.loads(record.observation)
        bit = configuration_bit(frame, event['accepted_fields'], event['facts'])
        lines.append(f"| `{record_id}` | {record.actor} | {_cell_text(frame, frame.cell_of(record.context))} | "
                     f"{'alternative' if bit else 'baseline'} |")
    kinds = Counter()
    for record in case.history.records:
        event = json.loads(record.observation)
        if record.record_id in oracle.binding_records or event.get('event') == 'register_version':
            continue
        if event.get('event') == 'review' and event.get('decision') == 'accept':
            kind = ('accepted review without the target field' if option.field not in event.get('reviewed_fields', [])
                    else f'accepted review by {record.actor} (outside the roster)')
            kinds['accepted review without the target field' if 'without' in kind else 'review outside the roster'] += 1
        else:
            kinds[{'review': 'rejected artifact', 'preference': 'personal preference',
                   'execution': 'technical failure log'}.get(event.get('event'), event.get('event'))] += 1
    lines += ['', '## Non-binding records', '', ', '.join(f'{k}: {v}' for k, v in sorted(kinds.items())) + '.', '',
              '## Oracle derivation', '',
              f'{len(oracle.compatible)} function(s) of the declared class fit every binding approval:', '']
    for function in oracle.compatible:
        lines.append(f'* {hclass.describe(function, names, list(frame.attributes.values()))}')
    lines += ['', '## Future tasks and warranted actions', '',
              '| Task type | Context | Status | Expected |', '| --- | --- | --- | --- |']
    for task, truth in tasks:
        context = 'other workflow (control)' if truth.cell is None else _cell_text(frame, truth.cell)
        lines.append(f'| {truth.task_type} | {context} | {truth.oracle_status} | {truth.expected_decision} |')
    world = case.world
    lines += ['', '## Evaluator-only construction note', '',
              f"Relevant attributes: {', '.join('`' + names[i] + '`' for i in world['relevant'])}"
              + (f"; confusable attribute `{names[world['confusable']]}` copies `{names[world['anchor']]}` "
                 'in every binding approval' if world.get('confusable') is not None else '') + '.',
              'The oracle above does not read this note.']
    return '\n'.join(lines) + '\n'


def export_review(directory: Path) -> dict:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    history_seed, future_seed, _ = SEEDS['review']
    cases = generate_histories(history_seed, 'review')
    index = []
    for position, case in enumerate(cases):
        if SELECTION.get(case.setting) != (case.hard_type, case.direction):
            continue
        tasks = generate_future_tasks(case, future_seed + position)
        name = f'{case.setting}-{case.family}'
        (directory / f'{name}.md').write_text(_example_markdown(case, tasks), encoding='utf-8')
        write_json(directory / f'{name}.json', {'case': case.model_dump(mode='json'),
                                                'tasks': [{'task': t.model_dump(mode='json'),
                                                           'truth': tr.model_dump(mode='json')} for t, tr in tasks]})
        index.append({'setting': case.setting, 'family': case.family, 'hard_type': case.hard_type,
                      'direction': case.direction, 'file': f'{name}.md', 'history_id': case.history.history_id})
    if len(index) != 4:
        raise ValueError('the review export requires one example per setting')
    lines = ['# v0.5 material review', '', 'Four synthetic examples from the review seeds (45031/45032), one per '
             'setting. They are not scored cases. Material approval is pending.', '',
             '| Setting | Family | Hard task | Alternative | File |', '| --- | --- | --- | --- | --- |']
    lines += [f"| {e['setting']} | {e['family']} | {e['hard_type']} | {e['direction']} | [{e['file']}]({e['file']}) |"
              for e in index]
    lines += ['', 'Please check that each expected action follows from the binding approvals and the declared class, '
              'that non-binding records are recognisable only through the public convention, and that the known-2 '
              'and unknown-6 examples differ only in the declared candidate attributes.']
    (directory / 'README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    binding = source_binding()
    write_json(directory / 'index.json', {'examples': index, 'source_sha256': binding['sha256']})
    manifest = seal(directory, directory / 'manifest.json')
    approvals = directory.with_name(directory.name + '-approvals.json')
    if approvals.exists():
        raise FileExistsError('an existing approval record cannot be replaced')
    write_json(approvals, {'material_sha256': manifest['sha256'], 'source_sha256': binding['sha256'],
                           'materials': {'approved': None, 'reviewer': None, 'date': None, 'response': None}})
    return {'directory': str(directory.name), 'material_sha256': manifest['sha256'], 'examples': index}
