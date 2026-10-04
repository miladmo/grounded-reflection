"""Six revised development examples for actual human review, never an approval."""

import json
from pathlib import Path

from reflectai_v03.context import render_rules

from .backend import write_json
from .config import DEVELOPMENT_HISTORY_SEED, MATERIAL_REVISION, REVIEW_FUTURE_SEED, REVIEW_HISTORY_SEED
from .data import generate_future_tasks, generate_histories
from .oracle import context_cells, infer_policies, policy_complexity, read_frame
from .storage import assert_sources, pending_approvals, seal, snapshot_sources, source_binding
from .surface_audit import audit_surfaces, surface_audit_markdown

REVIEW_FAMILIES = dict(zip(('S0', 'S1', 'S2', 'S3', 'S4', 'S5'),
                          ('sales', 'sales', 'reporting', 'hr', 'retrieval', 'retrieval')))
REVIEW_TASK_TYPES = dict(zip(('S0', 'S1', 'S2', 'S3', 'S4', 'S5'),
                            ('observed_change', 'unidentifiable', 'transfer_change',
                             'unidentifiable', 'resolved_retention_transfer', 'transfer_change')))


def _json(value):
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def _safe(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def _context_label(context):
    return ', '.join(f'{key}={value}' for key, value in context.items())


def _public_record_lines(record):
    """Readable event metadata followed by the complete original public evidence."""
    try:
        event = json.loads(record.observation)
    except ValueError:
        event = None
    lines = [f'### {record.record_id}', '',
             f'{record.timestamp} | {record.kind} | {record.actor}', '',
             'Context: ' + _context_label(record.context), '']
    if isinstance(event, dict):
        for key in ('decision', 'reviewed_fields', 'authority_ref', 'accepted_artifact',
                    'origin_ref', 'origin_record_id', 'origin_id', 'comment'):
            if key in event:
                lines.append(f'- {key}: {_safe(event[key])}')
        lines += ['', '```json', _json(event), '```', '']
    else:
        lines += [record.observation, '']
    return lines


def _oracle_proof(case, future):
    """Recompute from public history; private world and slot labels are not inputs."""
    oracle = infer_policies(case.history)
    frame = read_frame(case.history)
    cells = context_cells(frame)
    tables = []
    for version in sorted(oracle.versions):
        probes = []
        for cell in cells:
            context = {'task_family': frame.task_family, 'workflow': frame.workflow,
                       'version': version, **cell}
            probes.append(next(probe for probe in case.truth.scope_probes if probe.context == context))
        functions = set()
        for policy in oracle.policies:
            functions.add(tuple(int(render_rules(probe, policy.rules)
                                    != {field.name: field.value for field in probe.baseline_fields})
                                for probe in probes))
        tables.append({'version': version, 'cells': cells,
                       'compatible_function_count': len(functions),
                       'functions': [{'values': list(values),
                                      'complexity': policy_complexity(sum(bit << i for i, bit in enumerate(values)))}
                                     for values in sorted(functions)]})
    obligations = []
    for task, truth in future:
        baseline = {field.name: field.value for field in task.baseline_fields}
        effects = [render_rules(task, policy.rules) for policy in oracle.policies]
        unanimous = all(effect == effects[0] for effect in effects)
        warranted = effects[0] if unanimous else baseline
        decision = 'apply' if warranted != baseline else 'keep'
        if truth.expected_decision != decision:
            raise ValueError('Review task obligation differs from the public-evidence oracle.')
        witnesses = [row['record_id'] for row in oracle.constraints
                     if row['scope_context'] == task.context]
        obligations.append({'probe': truth.probe, 'context': task.context,
                            'observed_context': bool(witnesses), 'direct_witnesses': witnesses,
                            'unanimous_fields': unanimous, 'warranted_fields': warranted,
                            'expected_decision': decision,
                            'retention_basis': ('not_retention' if decision == 'apply' else
                                                'resolved' if unanimous else 'unresolved')})
    return {'source': 'Recomputed solely from the public History by the independent oracle.',
            'hypothesis_class': frame.hypothesis_class,
            'class_limit': 'H14 excludes XOR and XNOR; transfer identification depends on this supplied restriction.',
            'current_version': oracle.current_version, 'versions': oracle.versions,
            'current_compatible_function_count': next(table['compatible_function_count'] for table in tables
                                                      if table['version'] == oracle.current_version),
            'constraints': oracle.constraints, 'admissible_policy_count': len(oracle.policies),
            'compatible_functions_by_version': tables, 'task_obligations': obligations,
            'evidence_audit': oracle.evidence_audit}


def _proof_lines(proof):
    lines = ['## Oracle derivation from public evidence', '', proof['source'], '',
             proof['class_limit'], '',
             f"Distinct current-version functions: **{proof['current_compatible_function_count']}**. "
             f"Full policies across all registered versions: **{proof['admissible_policy_count']}**.", '',
             'An approval constrains one cell in its registered version. The following are the',
             'actual applied constraints, including independent repeats. Copies do not add a constraint.', '',
             '| Public record | Version | Context | Field option |', '| --- | --- | --- | --- |']
    for constraint in proof['constraints']:
        lines.append(f"| {_safe(constraint['record_id'])} | {_safe(constraint['version'])} | "
                     f"{_safe(_context_label(constraint['scope_context']))} | {constraint['option_index']} |")
    lines += ['', '### Competing requirement explanations', '',
              'Zero is the configured baseline; one is the alternative. Each row is a distinct',
              'compatible function for this version. No preference for simplicity removes a row.',
              'The private sampling plan and world policy do not filter these explanations.', '']
    for table in proof['compatible_functions_by_version']:
        cells = table['cells']
        lines += [f"Version {table['version']}: {table['compatible_function_count']} compatible functions.", '',
                  '| Function | ' + ' | '.join(_safe(_context_label(cell)) for cell in cells) + ' | Complexity |',
                  '| --- | ' + ' | '.join('---:' for _ in cells) + ' | ---: |']
        for number, function in enumerate(table['functions'], 1):
            lines.append(f"| {number} | " + ' | '.join(str(v) for v in function['values'])
                         + f" | {function['complexity']} |")
        lines.append('')
    lines += ['### Diagnostic and control derivations', '',
              '| Task | Context observed | Witnesses | Action | Retention basis |',
              '| --- | --- | --- | --- | --- |']
    for item in proof['task_obligations']:
        lines.append(f"| {item['probe']} | {item['observed_context']} | "
                     f"{', '.join(item['direct_witnesses']) or 'none'} | {item['expected_decision']} | "
                     f"{item['retention_basis']} |")
    return lines + ['']


def _review_summary(proof, audit):
    lines = ['## Review summary', '',
             f"Current compatible functions: **{proof['current_compatible_function_count']}**. "
             f"Full cross-version policies: {proof['admissible_policy_count']}.", '',
             'H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved',
             'baseline does not establish that the baseline is the true requirement.', '',
             '| Task | Public context | Previously observed | Warranted action | Retention basis |',
             '| --- | --- | --- | --- | --- |']
    for task in proof['task_obligations']:
        lines.append(f"| {task['probe']} | {_safe(_context_label(task['context']))} | "
                     f"{task['observed_context']} | {task['expected_decision']} | {task['retention_basis']} |")
    lines += ['', f"Counterfactual qualification requires **{audit['required_outcome']}** for every present type. "
              f"All present types qualify: **{audit['passed']}**.", '',
              'One qualifying example per present type is shown below. The links lead to its',
              'public evidence; all records and counts appear in the later audit and JSON sidecar.', '',
              '| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |',
              '| --- | --- | --- | --- | --- |']
    by_id = {record['record_id']: record for record in audit['records']}
    for kind, counts in sorted(audit['by_type'].items()):
        if not counts['qualifying_record_ids']:
            lines.append(f"| {kind} ({counts['record_count']}) | none | — | — | qualification failed |")
            continue
        record = by_id[counts['qualifying_record_ids'][0]]
        record_id, origin = record['record_id'], record.get('origin_record_id')
        references = f'[{record_id}](#{record_id.lower()})'
        if origin and origin != record_id:
            references += f' / [{origin}](#{origin.lower()})'
        value = (repr(record.get('selected_field_value')) if record.get('selected_field_present')
                 else 'absent')
        lines.append(f"| {kind} ({counts['record_count']}) | {references} | "
                     f"{_safe(record.get('selected_field'))} = {_safe(value)} | "
                     f"{_safe(record.get('promotion'))} Context: {_safe(_context_label(record['context']))} | "
                     f"{record['outcome']} / {record['remaining_policy_count']} |")
    return lines + ['', 'An action flip requires a nonempty compatible set and a changed diagnostic or control',
                    'action. A contradiction has no compatible policy and supplies neither task action.', '',
                    '[Complete oracle derivation](#oracle-derivation-from-public-evidence) · '
                    '[Every counterfactual record](#single-record-counterfactual-relevance)', '']


def _counterfactual_lines(audit, sidecar):
    lines = ['## Single-record counterfactual relevance', '',
             'Evaluator audit only. Exactly one visible proposed configuration is promoted to a',
             'binding current-version observation at its apparent context. Genuine observations',
             'are retained. An empty compatible set is a contradiction, never an action flip.', '',
             f"Required qualifying outcome for each present type: **{audit['required_outcome']}**. "
             f"All present types qualify: **{audit['passed']}**.", '',
             'Absent types have no fabricated denominator. Technical recovery events are counted',
             'separately in the material audit and are not approval-promotion interventions.', '',
             '| Manipulated type | Records | Strict action flip | Contradiction | Unchanged | Narrower, same actions | Retention resolved | Unassessable | Qualifying records |',
             '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
    for kind, counts in sorted(audit['by_type'].items()):
        lines.append(f"| {kind} | {counts['record_count']} | {counts['action_flip']} | "
                     f"{counts['contradiction']} | {counts['unchanged_constraints']} | "
                     f"{counts['narrower_same_actions']} | {counts['retention_resolved']} | "
                     f"{counts['unassessable']} | {', '.join(counts['qualifying_record_ids']) or 'none'} |")
    lines += ['', '### Every promoted public record', '',
              '| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |',
              '| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |']
    for record in audit['records']:
        counts = audit['by_type'][record['record_type']]
        qualifies = record['record_id'] in counts['qualifying_record_ids']
        lines.append(f"| {record['record_id']} | {record['record_type']} | "
                     f"{record.get('origin_record_id') or 'self'} | {record.get('option_index')} | "
                     f"{record['remaining_policy_count']} | {record['outcome']} | {qualifies} | "
                     f"{record['diagnostic_action']} | {record['control_action']} |")
    lines += ['', '### Exact promotions, contexts and public value provenance', '',
              f'The [complete JSON sidecar]({sidecar}) preserves every intervention under `counterfactual.records`,',
              'including selected field presence/value, effective current context, public origin,',
              'precise promotion and remaining-policy count. No intervention alters the real history.', '']
    return lines


def export_review(directory: Path, *, repo: Path, pilot: Path, protocol: Path) -> dict:
    directory, repo, pilot, protocol = map(Path, (directory, repo, pilot, protocol))
    approval_path = directory.with_name(directory.name + '-approvals.json')
    if approval_path.exists():
        raise FileExistsError('An existing approval record cannot be replaced.')
    directory.mkdir(parents=True, exist_ok=False)
    binding = source_binding(repo, pilot, protocol)
    snapshot = snapshot_sources(directory / 'sources', repo, pilot, protocol)
    if snapshot != binding:
        raise ValueError('Sources changed while creating the revised review export.')
    cases = generate_histories(REVIEW_HISTORY_SEED, split='review')
    selected = [case for case in cases if REVIEW_FAMILIES[case.setting] == case.family]
    if (len(selected) != 6 or len({case.setting for case in selected}) != 6
            or any(case.material_audit['task_type'] != REVIEW_TASK_TYPES[case.setting] for case in selected)):
        raise ValueError('Review export requires the six prospectively selected amendment-3 examples.')
    selected.sort(key=lambda case: case.setting)
    development = generate_histories(DEVELOPMENT_HISTORY_SEED, split='development')
    surface = audit_surfaces(development, cases, [case.history.history_id for case in selected])
    surface.update(material_revision=MATERIAL_REVISION, development_history_seed=DEVELOPMENT_HISTORY_SEED,
                   review_history_seed=REVIEW_HISTORY_SEED)
    write_json(directory / 'surface-audit.json', surface)
    (directory / 'surface-audit.md').write_text(surface_audit_markdown(surface), encoding='utf-8')
    surface_by_history = {row['history_id']: row for row in surface['construction_checks']['review']['histories']}
    index = ['# v0.4 amendment-3 human material review', '',
             f'Material revision: **{MATERIAL_REVISION}**.', '',
             'Synthetic development examples; these are not live scored histories.',
             'Implementation approval does not approve these materials or a model run.',
             'Material and live approval remain separate and pending.', '',
             '[Surface-only audit: fixed development selection and held-out review results](surface-audit.md)',
             '([complete JSON](surface-audit.json)). '
             f"Investigation required: **{surface['readiness']['requires_investigation']}**.", '',
             'Highlighted examples: [S1 sales: unresolved rival explanations](S1-sales.md) and',
             '[S5 retrieval: transfer in the combined setting](S5-retrieval.md).', '',
             'Review the complete public records, competing explanations, task obligations,',
             'and every manipulated record promotion. Verify the stated public conventions',
             'and whether any evaluator conclusion relies on an unstated assumption.', '',
             'Transfer here depends on the public H14 exclusion of XOR and XNOR. The sampling',
             'plan does not eliminate rival public explanations. No field validation is implied.', '',
             '| Setting | Family | Task type | Review file |', '| --- | --- | --- | --- |']
    for number, case in enumerate(selected):
        future = generate_future_tasks(case, REVIEW_FUTURE_SEED + number)
        proof = _oracle_proof(case, future)
        counterfactual = case.material_audit['counterfactual']
        stem = f'{case.setting}-{case.family}'
        write_json(directory / f'{stem}.json', {
            'material_revision': MATERIAL_REVISION,
            'synthetic_placeholder': True, 'development_only': True,
            'case': case.model_dump(mode='json'), 'oracle_proof': proof,
            'counterfactual': counterfactual,
            'surface_audit': {'report': 'surface-audit.json', 'markdown': 'surface-audit.md',
                              'history_id': case.history.history_id,
                              'construction_checks': surface_by_history[case.history.history_id]},
            'future': [{'task': task.model_dump(mode='json'), 'truth': truth.model_dump(mode='json')}
                       for task, truth in future],
            'human_review': {'status': 'pending', 'reviewer': None, 'response': None}})
        lines = [f'# {case.setting} / {case.family}', '',
                 f'Material revision: {MATERIAL_REVISION}. Synthetic development example.', '',
                 '[Frozen surface-selector audit](surface-audit.md) · [Complete audit JSON](surface-audit.json).',
                 'Its per-history results use this case’s history ID; selector choice used only separate development histories.', '',
                 f"Registered task type: **{case.material_audit['task_type']}**. "
                 f'Intended diagnostic regime: **{case.regime}**.',
                 f'Public records: {len(case.history.records)}. '
                 f"Control basis: {case.material_audit['control_basis']}.", '']
        lines += _review_summary(proof, counterfactual)
        lines += ['## Public configuration and assumptions', '', '```json',
                 _json(json.loads(case.history.initial_configuration)), '```', '',
                 case.history.assumptions, '', '## Public work records', '']
        for record in case.history.records:
            lines.extend(_public_record_lines(record))
        lines += _proof_lines(proof)
        lines += ['## Private material audit', '',
                  'These design labels, counterfactuals and world requirements are evaluator material.',
                  'They are never preparation or generation inputs. The true world is distinct from',
                  'what the public evidence identifies. Exact world fields are shown with each task.', '',
                  'Registered record counts and construction audit:', '', '```json',
                  _json({key: value for key, value in case.material_audit.items() if key != 'counterfactual'}),
                  '```', '']
        lines += _counterfactual_lines(counterfactual, f'{stem}.json')
        lines += ['## Future tasks for this development example', '']
        for task, truth in future:
            lines.extend([f'### {truth.probe}', '', 'Public task', '', '```json', task.model_dump_json(indent=2),
                          '```', '', 'Private expected obligations and actual-world fields', '', '```json',
                          truth.model_dump_json(indent=2), '```', ''])
        lines += ['## Human response', '', 'Pending. No approval is inferred from this export.', '']
        (directory / f'{stem}.md').write_text('\n'.join(lines), encoding='utf-8')
        index.append(f"| {case.setting} | {case.family} | {case.material_audit['task_type']} | [{stem}]({stem}.md) |")
    (directory / 'README.md').write_text('\n'.join(index) + '\n', encoding='utf-8')
    write_json(directory / 'index.json', {
        'material_revision': MATERIAL_REVISION, 'source_sha256': binding['sha256'],
        'history_seed': REVIEW_HISTORY_SEED, 'future_seed': REVIEW_FUTURE_SEED,
        'surface_audit': {'json': 'surface-audit.json', 'markdown': 'surface-audit.md',
                          'development_history_seed': DEVELOPMENT_HISTORY_SEED,
                          'development_histories': len(development), 'heldout_histories': len(cases),
                          'requires_investigation': surface['readiness']['requires_investigation']},
        'history_ids': [case.history.history_id for case in selected],
        'settings': [case.setting for case in selected],
        'selection': [{'setting': case.setting, 'family': case.family,
                       'task_type': case.material_audit['task_type']} for case in selected],
        'human_review': 'pending'})
    assert_sources(binding, repo, pilot, protocol)
    material = seal(directory, directory / 'manifest.json')
    # Human decisions are external to immutable materials and are never fabricated.
    approval = pending_approvals(binding['sha256'], material['sha256'])
    with approval_path.open('x', encoding='utf-8') as stream:
        stream.write(_json(approval))
    return {'directory': str(directory), 'material_revision': MATERIAL_REVISION,
            'source_sha256': binding['sha256'], 'material_sha256': material['sha256'],
            'approval_path': str(approval_path)}
