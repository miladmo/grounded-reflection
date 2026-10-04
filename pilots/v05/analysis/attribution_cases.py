"""Case files for the v0.5 attribution review, part 1 (point 4); offline, no model calls.

(a) C in history-7b21f7009087, transfer: what each C1 chunk saw of the binding approvals,
    what each chunk returned, the retained guidance with its cited records, and the
    generation input and output.
(b) B in history-dd4c7199f572 (unidentifiable) and history-f09764e24578 (transfer): the
    outputs with declared rules and decision labels, and the binding approvals in context.

Writes pilots/v05/review/attribution-20261004/CASES.md.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
for folder in (ROOT / 'src', ROOT / 'pilots/v03', ROOT / 'pilots/v04', ROOT / 'pilots/v05', ROOT / 'pilots/v05/analysis'):
    sys.path.insert(0, str(folder))

from reflectai_v03.contracts import History  # noqa: E402
from reflectai_v05 import hclass  # noqa: E402
from reflectai_v05.oracle import configuration_bit, infer, read_frame  # noqa: E402
from reflectai_v05.storage import verify_seal  # noqa: E402

RUN = ROOT / 'pilots/v05/runs/live-main-20261003'
OUT = ROOT / 'pilots/v05/review/attribution-20261004/CASES.md'
NL = chr(10)


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def payload(path: Path) -> dict:
    return json.loads(load(path)['prompt'].split(NL + 'PAYLOAD' + NL, 1)[1])


class Case:
    def __init__(self, hid: str):
        case = next(c for c in load(RUN / 'evaluator/cases.json') if c['history']['history_id'] == hid)
        self.case, self.hid = case, hid
        self.history = History.model_validate(case['history'])
        self.frame, self.oracle = read_frame(self.history), infer(self.history)
        self.binding = set(self.oracle.binding_records)
        self.records = {r.record_id: r for r in self.history.records}
        self.candidates = self.frame.candidate_attributes
        self.pairs = load(RUN / 'evaluator/future-tasks.json')[hid]

    def cell_text(self, context: dict) -> str:
        return ', '.join(f'{a}={context.get(a)}' for a in self.candidates)

    def record_line(self, rid: str) -> str:
        record = self.records.get(rid)
        if record is None:
            return f'| `{rid}` | not in history | | | | |'
        event = json.loads(record.observation)
        bit = ''
        if rid in self.binding:
            fields, facts = event['accepted_fields'], event['facts']
            bit = 'alternative' if configuration_bit(self.frame, fields, facts) else 'baseline'
        return (f"| `{rid}` | {self.cell_text(record.context)} | {event.get('event')}/{event.get('decision', '-')} | "
                f"{record.actor} | {'binding' if rid in self.binding else 'not binding'} | {bit} |")

    def table(self, ids) -> list[str]:
        lines = ['| Record | Context (candidate attributes) | Event | Actor | Status | Binding shows |',
                 '| --- | --- | --- | --- | --- | --- |']
        return lines + [self.record_line(rid) for rid in ids]

    def task(self, task_type: str):
        return next(p for p in self.pairs if p['truth']['task_type'] == task_type)

    def header(self, task_type: str) -> list[str]:
        pair = self.task(task_type)
        task, truth = pair['task'], pair['truth']
        names = self.frame.attribute_names
        function = next(f for f in hclass.rule_class(len(names), self.frame.candidate_indices())
                        if f.table == int(self.case['world']['table']))
        compatible = [hclass.describe(f, names, list(self.frame.attributes.values())) for f in self.oracle.compatible]
        return [f"* Setting {self.case['setting']}, family {self.case['family']}, direction {self.case['direction']}, "
                f"target field `{self.frame.field_option.field}` ({self.frame.field_option.operation}).",
                f"* Candidate attributes: {', '.join(self.candidates)}. "
                f"World function: {hclass.describe(function, names, list(self.frame.attributes.values()))}.",
                f"* Oracle compatible set ({len(compatible)}): {'; '.join(compatible)}.",
                f"* Task `{task['task_id']}` ({task_type}), cell {self.cell_text(task['context'])}: "
                f"expected `{truth['expected_decision']}` (oracle status `{truth['oracle_status']}`).",
                f"* Binding approvals: {len(self.binding)}."]


def output_block(record_path: Path) -> list[str]:
    record = load(record_path)
    response = record.get('response') or {}
    lines = [f"* Call status: `{record['status']}`; decision label: `{response.get('decision')}`."]
    lines.append('* Fields: ' + ', '.join(f"{f['name']}={f['value']!r}" for f in response.get('fields', [])))
    for rule in response.get('applied_rules', []):
        lines.append(f"* Declared rule: `{json.dumps(rule, ensure_ascii=False)}`")
    if not response.get('applied_rules'):
        lines.append('* Declared rules: none.')
    if response.get('questions'):
        lines.append(f"* Questions: {response['questions']}")
    return lines


def candidates_block(prep: dict | None) -> list[str]:
    if not prep:
        return ['* No preparation.']
    lines = []
    for c in prep.get('candidates', []):
        rule = c.get('rule') or {}
        match = {k: v for k, v in rule.get('scope', {}).get('match', {}).items()
                 if k not in ('task_family', 'workflow', 'version')}
        lines.append(f"* `{c['status']}` {rule.get('operation')} when {json.dumps(match, ensure_ascii=False)}; "
                     f"evidence {len(c.get('evidence_ids', []))}, counterevidence {len(c.get('counterevidence_ids', []))}. "
                     f"Claim: {c.get('claim', '')}")
    return lines


def case_a() -> list[str]:
    c = Case('history-7b21f7009087')
    lines = ['## (a) C in `history-7b21f7009087`, transfer', ''] + c.header('transfer_change') + ['']
    folder = RUN / 'preparation' / c.hid / 'C'
    lines += ['### What each C1 chunk saw and returned', '',
              '| Chunk | Records shown | Binding approvals shown | Binding approvals (id: cell, shows) |',
              '| --- | ---: | ---: | --- |']
    seen = set()
    for chunk in sorted(folder.glob('C1-*')):
        shown = [r['record_id'] for r in payload(chunk / 'request.json')['records']]
        hits = [rid for rid in shown if rid in c.binding]
        seen |= set(hits)
        detail = '; '.join(f"`{rid}`: {c.cell_text(c.records[rid].context)}, "
                           f"{c.record_line(rid).rstrip(' |').rsplit(' | ', 1)[1]}" for rid in hits)
        lines.append(f'| {chunk.name} | {len(shown)} | {len(hits)} | {detail} |')
    lines += ['', f'Binding approvals seen by some C1 chunk: {len(seen)} of {len(c.binding)}.', '']
    for chunk in sorted(folder.glob('C1-*')) + [folder / 'C2']:
        lines += [f'**{chunk.name} returned:**', ''] + candidates_block(load(chunk / 'record.json').get('response')) + ['']
    c2 = payload(folder / 'C2' / 'request.json')
    cited_in_c2 = [r['record_id'] for r in c2['cited_records']]
    lines += [f"C2 input: {c2['records_shown']}; {len(cited_in_c2)} records, of which "
              f"{sum(r in c.binding for r in cited_in_c2)} binding.", '']
    retained = load(RUN / 'preparation/retained.json').get(f'{c.hid}|C')
    lines += ['### Retained guidance', ''] + candidates_block(retained) + ['']
    cited = sorted({i for cand in (retained or {}).get('candidates', [])
                    for i in cand.get('evidence_ids', []) + cand.get('counterevidence_ids', [])})
    lines += ['Records cited in the retained guidance:', ''] + c.table(cited) + ['']
    gen = RUN / 'generation' / f'{c.hid}-transfer_change-C'
    instructions = payload(gen / 'request.json').get('instructions', [])
    lines += ['### Generation', '', f'* Instructions passed to generation: {len(instructions)}.']
    lines += [f'  * `{json.dumps(i, ensure_ascii=False)}`' for i in instructions]
    lines += output_block(gen / 'record.json') + ['']
    return lines


def case_b(hid: str, task_type: str) -> list[str]:
    c = Case(hid)
    gen = RUN / 'generation' / f'{hid}-{task_type}-B'
    excerpt = payload(gen / 'request.json')['history_excerpt']
    ids = {r['record_id'] for key in ('registrations', 'records') for r in excerpt.get(key, [])
           if isinstance(r, dict) and 'record_id' in r}
    if not ids:
        ids = set(__import__('re').findall(r'record-[0-9a-f]{12}', json.dumps(excerpt)))
    lines = [f'## (b) B in `{hid}`, {task_type}', ''] + c.header(task_type)
    lines += [f'* Binding approvals in B\'s context: {len(c.binding & ids)} of {len(c.binding)}; '
              f'records in context: {len(ids)}.', '', '### Output', ''] + output_block(gen / 'record.json') + ['']
    lines += ['### Binding approvals', ''] + c.table(sorted(c.binding, key=lambda r: c.records[r].timestamp)) + ['']
    return lines


def main():
    seal = verify_seal(RUN, RUN / 'manifest.json')['sha256']
    lines = ['# Attribution review v0.5, part 1: case files', '',
             f'Generated by `pilots/v05/analysis/attribution_cases.py` from the sealed main run (seal `{seal}`). '
             'No model calls. "Binding shows" is the configuration a binding approval accepted.', '']
    lines += case_a()
    lines += case_b('history-dd4c7199f572', 'unidentifiable')
    lines += case_b('history-f09764e24578', 'transfer_change')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(NL.join(lines) + NL, encoding='utf-8', newline=NL)
    print(OUT.relative_to(ROOT).as_posix())


if __name__ == '__main__':
    main()
