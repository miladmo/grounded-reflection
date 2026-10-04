"""Finite, evaluator-only v0.4 measurements; never a model-input builder.

Output semantics are the frozen v0.3 semantics. Candidate checks establish a
lower bound on content errors over the registered probes, not semantic approval
of free-text reasoning. No author-written candidate wording determines a score.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from fractions import Fraction
import json
from math import ceil
from statistics import mean
from typing import Any

from reflectai_v03.context import render_rules, retained_rules
from reflectai_v03.contracts import History, HistoryTruth, Preparation, Task, TaskTruth, WorkOutput
from reflectai_v03.evaluation import evaluate_output

ARMS = ('A', 'B', 'C')
SETTINGS = tuple(f'S{i}' for i in range(6))
PROBES = ('diagnostic', 'control')
REGIMES = {'change': 2, 'resolved_keep': 1, 'unidentifiable': 1}
TASK_TYPES = {'transfer_change': 'change', 'observed_change': 'change',
              'resolved_retention_transfer': 'resolved_keep', 'unidentifiable': 'unidentifiable'}
DIRECTION_TAGS = ('unsupported_transfer', 'missed_warranted_transfer', 'observed_contradiction')
CONFLICT_METHODS = ('majority', 'recency')
CATEGORIES = ('content', 'technical', 'mixed', 'unresolved')
METRICS = ('update_correct', 'world_compliant', 'warranted_world_compliant',
           'unsupported_lucky_success', 'completed_deliverable',
           'execution_consistent', 'decision_label_correct', 'valid_output')


def _fields(items):
    return {item.name: item.value for item in items}


def _current_scope(history: History, truth: HistoryTruth) -> dict:
    """Public observations and four frozen probes; no latent world input."""
    from .oracle import context_cells, infer_policies, option_rule, read_frame
    if history.history_id != truth.history_id:
        raise ValueError('history/truth identity mismatch')
    frame, oracle = read_frame(history), infer_policies(history)
    cells, masks = [], set()
    for index, cell in enumerate(context_cells(frame)):
        context = {'task_family': frame.task_family, 'workflow': frame.workflow,
                   'version': oracle.current_version, **cell}
        matches = [probe for probe in truth.scope_probes if probe.context == context]
        if len(matches) != 1:
            raise ValueError('exactly one frozen probe per current context cell is required')
        probe = matches[0]
        baseline = _fields(probe.baseline_fields)
        alternative = render_rules(probe, [option_rule(frame, context)])
        if alternative == baseline:
            raise ValueError('scope probe does not distinguish the two configurations')
        observed_ids = [item['record_id'] for item in oracle.constraints
                        if item['scope_context'] == context]
        possible = set()
        for policy in oracle.policies:
            result = render_rules(probe, policy.rules)
            if result not in (baseline, alternative):
                raise ValueError('oracle policy is outside the public binary configuration class')
            possible.add(int(result == alternative))
        cells.append({'index': index, 'context': context, 'probe': probe,
                      'baseline': baseline, 'alternative': alternative,
                      'observed_record_ids': observed_ids, 'observed': bool(observed_ids),
                      'admissible_values': sorted(possible)})
    def policy_mask(policy):
        value = 0
        for cell in cells:
            actual = render_rules(cell['probe'], policy.rules)
            if actual not in (cell['baseline'], cell['alternative']):
                raise ValueError('policy consequence is outside the public binary configuration class')
            value |= int(actual == cell['alternative']) << cell['index']
        return value
    masks = {policy_mask(policy) for policy in oracle.policies}
    frozen_masks = {policy_mask(policy) for policy in truth.admissible_policies}
    if masks != frozen_masks:
        raise ValueError('frozen and public current-policy consequences disagree')
    return {'frame': frame, 'oracle': oracle, 'cells': cells, 'compatible_masks': sorted(masks)}


def _direction(cell: dict, actual: dict | None) -> dict:
    """Describe field effects, without claiming an inference strategy or cause."""
    bit = (int(actual == cell['alternative']) if actual is not None
           and actual in (cell['baseline'], cell['alternative']) else None)
    possible, observed = cell['admissible_values'], cell['observed']
    tags = []
    if bit is not None:
        if observed and possible != [bit]:
            tags.append('observed_contradiction')
        elif not observed:
            if bit == 1 and possible != [1]:
                tags.append('unsupported_transfer')
            elif bit == 0 and possible == [1]:
                tags.append('missed_warranted_transfer')
    return {'assessable': bit is not None, 'context': cell['context'],
            'observed': observed, 'observed_record_ids': cell['observed_record_ids'],
            'admissible_values': possible, 'effective_option': bit,
            'warranted_option': int(possible == [1]),
            'retention_basis': 'resolved' if possible == [0] else 'unresolved' if len(possible) > 1 else None,
            'tags': tags, **{tag: tag in tags if bit is not None else None for tag in DIRECTION_TAGS}}


def score_scope(history: History, truth: HistoryTruth,
                preparation: Preparation | None) -> dict:
    """Combine adopted effects on four cells; absence is never zero errors.

    The minimum-complexity marker describes an association only. The complete
    retained effect table must match a tied minimum of the *current* compatible
    functions, and an unsupported extension must occur. Historical version
    alternatives do not create spurious multiplicity or ties.
    """
    present = isinstance(preparation, Preparation)
    result = {'preparation_present': present, 'available': False, 'planned_cells': 4,
              'assessed_cells': 0, 'unassessable_cells': 4, 'cells': [],
              **{tag: None for tag in DIRECTION_TAGS},
              'warranted_change_cells': None, 'covered_warranted_change_cells': None,
              'warranted_change_coverage': None, 'observed_cells': None, 'unobserved_cells': None,
              'simplicity_association': {'assessable': False, 'flag': None,
                  'interpretation': 'Observable association, not evidence of a causal strategy.'}}
    try:
        from .oracle import policy_complexity
        scope = _current_scope(history, truth)
    except (ImportError, ValueError, KeyError, TypeError, AttributeError) as exc:
        result['error'] = f'{type(exc).__name__}: {exc}'
        return result
    adopted, preparation_error = [], None
    if present:
        try:
            adopted = retained_rules(preparation, history)
        except (ValueError, KeyError, TypeError) as exc:
            preparation_error = f'{type(exc).__name__}: {exc}'
    result['preparation_error'] = preparation_error
    rows = []
    for cell in scope['cells']:
        actual, error = None, preparation_error
        if present and preparation_error is None:
            try:
                actual = render_rules(cell['probe'], adopted)
            except (ValueError, KeyError, TypeError) as exc:
                error = f'{type(exc).__name__}: {exc}'
        row = _direction(cell, actual)
        row['error'] = error or (None if row['assessable'] else
                                'missing_preparation' if not present else 'effect_outside_binary_field_contract')
        rows.append(row)
    assessed = [row for row in rows if row['assessable']]
    warranted = [row for row in rows if row['admissible_values'] == [1]]
    covered = sum(row['effective_option'] == 1 for row in warranted)
    result.update(available=True, cells=rows, assessed_cells=len(assessed),
                  unassessable_cells=4 - len(assessed),
                  **{tag: sum(row[tag] is True for row in assessed) if assessed else None for tag in DIRECTION_TAGS},
                  observed_cells=sum(row['observed'] for row in rows),
                  unobserved_cells=sum(not row['observed'] for row in rows),
                  warranted_change_cells=len(warranted),
                  covered_warranted_change_cells=covered if any(r['assessable'] for r in warranted) else None,
                  warranted_change_coverage=(covered / len(warranted) if warranted
                      and all(row['assessable'] for row in warranted) else None))
    masks = scope['compatible_masks']
    complexities = {mask: policy_complexity(mask) for mask in masks}
    minimum = min(complexities.values())
    minima = sorted(mask for mask, value in complexities.items() if value == minimum)
    complete = len(assessed) == 4
    adopted_mask = sum(row['effective_option'] << index for index, row in enumerate(rows)) if complete else None
    association = bool(len(masks) > 1 and adopted_mask in minima
                       and any(row['unsupported_transfer'] is True for row in rows)) if complete else None
    result['simplicity_association'].update(
        assessable=complete, flag=association, compatible_function_count=len(masks),
        compatible_masks=masks, minimum_complexity=minimum, tied_minimum_masks=minima,
        tied_minimum_count=len(minima), retained_effect_mask=adopted_mask,
        matches_minimum=adopted_mask in minima if complete else None)
    return result


def _task_direction(history, truth, task, output, complete):
    if history is None:
        return {'assessable': False, 'tags': [], 'reason': 'missing_history',
                **{tag: None for tag in DIRECTION_TAGS}}
    try:
        from .oracle import option_rule
        scope = _current_scope(history, truth)
        cell = next((item for item in scope['cells'] if item['context'] == task.context), None)
        if cell is None:
            raise ValueError('task does not match a registered current context cell')
        # Use the actual task facts; witness document values are not task values.
        cell = {**cell, 'baseline': _fields(task.baseline_fields),
                'alternative': render_rules(task, [option_rule(scope['frame'], task.context)])}
        return {**_direction(cell, _fields(output.fields) if complete else None),
                'reason': None if complete else 'incomplete_or_missing_output',
                'source': 'completed_output_fields',
                'reference': 'history-informed warrant; distinct from A information-relative warrant'}
    except (ImportError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return {'assessable': False, 'tags': [], 'reason': f'{type(exc).__name__}: {exc}',
                **{tag: None for tag in DIRECTION_TAGS}}


def _conflict_signals(history, scope):
    """Recover votes publicly; counterfactual *outcomes* never select votes.

    Genuine current approvals and all six promotion types each contribute one
    visible record. Forwards retain destination context and arrival timestamp,
    while origin ID/date remain in the audit. Registrations and technical logs
    have no recoverable target configuration and do not supply votes.
    """
    from .counterfactual import audit_counterfactuals
    records = {record.record_id: record for record in history.records}
    cells, oracle = scope['cells'], scope['oracle']
    promoted = audit_counterfactuals(history, cells[0]['context'], cells[1]['context'])['records']
    observations = [{'record_id': item['record_id'], 'origin_record_id': item['record_id'],
                     'record_type': 'current_target_approval', 'context': item['scope_context'],
                     'option_index': item['option_index']} for item in oracle.constraints
                    if item['version'] == oracle.current_version]
    observations.extend(promoted)
    signals, seen = [], set()
    for item in observations:
        record_id, origin_id = item['record_id'], item.get('origin_record_id')
        if record_id in seen:
            raise ValueError('a visible record cannot supply two votes')
        seen.add(record_id)
        record, origin = records[record_id], records.get(origin_id)
        signals.append({'record_id': record_id, 'origin_record_id': origin_id,
                        'record_type': item['record_type'], 'context': item['context'],
                        'option_index': item.get('option_index'), 'timestamp': record.timestamp,
                        'origin_timestamp': origin.timestamp if origin else None,
                        'unusable_reason': item.get('reason') if item.get('option_index') not in (0, 1) else None})
    return signals, sorted(set(records) - seen)


def _conflict_predictions(signals):
    usable = [item for item in signals if item.get('option_index') in (0, 1)]
    unusable = [item['record_id'] for item in signals if item.get('option_index') not in (0, 1)]
    counts = Counter(item['option_index'] for item in usable)
    conflict = bool(counts[0] and counts[1])
    predictions = {method: {'prediction': None, 'status': 'insufficient_evidence'} for method in CONFLICT_METHODS}
    if unusable:
        for item in predictions.values():
            item['status'] = 'unusable_target_configuration'
    elif conflict:
        predictions['majority'] = {'prediction': (int(counts[1] > counts[0]) if counts[0] != counts[1] else None),
                                   'status': 'defined' if counts[0] != counts[1] else 'tie'}
        try:
            times = []
            for item in usable:
                timestamp = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
                if timestamp.tzinfo is None:
                    raise ValueError('recency requires an explicit timezone')
                times.append((timestamp, item))
            maximum = max(stamp for stamp, _ in times)
            latest = [item for stamp, item in times if stamp == maximum]
            values = {item['option_index'] for item in latest}
            predictions['recency'] = {'prediction': next(iter(values)) if len(values) == 1 else None,
                'status': 'defined' if len(values) == 1 else 'tie',
                'latest_record_ids': sorted(item['record_id'] for item in latest),
                'latest_timestamp': maximum.isoformat(), 'latest_record_count': len(latest)}
        except (ValueError, TypeError, KeyError) as exc:
            predictions['recency'] = {'prediction': None, 'status': 'unusable_timestamp', 'reason': str(exc)}
    return {'apparent_conflict': conflict, 'visible_configuration_counts': {'0': counts[0], '1': counts[1]},
            'unusable_record_ids': unusable, 'heuristics': predictions}


def score_conflict_resolution(history: History | None, truth: HistoryTruth, *,
                              task_type: str | None, preparation: Preparation | None = None,
                              task: Task | None = None, output: WorkOutput | None = None,
                              completed_output: bool = False) -> dict:
    """Observable wrong-effect association, never a confirmed reasoning motive.

    Only the three decided registered task types are eligible. Within them a
    context must have a unanimous oracle value and both visible configurations.
    A unique majority/latest prediction must be wrong and match the actual
    binary effect. Cross-context logical contradictions alone do not qualify.
    """
    eligible = task_type != 'unidentifiable' if task_type in TASK_TYPES else None
    result = {'task_type': task_type, 'eligible_task_type': eligible, 'available': False,
              'planned_contexts': 1 if task is not None else 4, 'cells': [],
              'source': 'completed_output_fields' if task is not None else 'retained_adopted_guidance',
              'attribution_status': 'observable_association_only', 'human_rationale_review': None,
              'interpretation': 'A matching wrong effect is compatible with the heuristic; it does not establish its use or motivation.'}
    if history is None:
        result['reason'] = 'missing_public_history'
        return result
    if eligible is None:
        result['reason'] = 'missing_or_unknown_registered_task_type'
        return result
    try:
        from .oracle import option_rule
        scope = _current_scope(history, truth)
        signals, excluded = _conflict_signals(history, scope)
        cells = scope['cells'] if task is None else [cell for cell in scope['cells'] if cell['context'] == task.context]
        if task is not None and len(cells) != 1:
            raise ValueError('task is outside the four current registered contexts')
        retained, preparation_error = [], None
        if task is None:
            if preparation is None:
                preparation_error = 'missing_preparation'
            else:
                try:
                    retained = retained_rules(preparation, history)
                except (ValueError, TypeError, KeyError) as exc:
                    preparation_error = str(exc)
        for cell in cells:
            relevant = [signal for signal in signals if signal['context'] == cell['context']]
            prediction = _conflict_predictions(relevant)
            actual, effect_error = None, preparation_error
            if task is not None:
                cell = {**cell, 'baseline': _fields(task.baseline_fields),
                        'alternative': render_rules(task, [option_rule(scope['frame'], task.context)])}
                actual = _fields(output.fields) if completed_output and isinstance(output, WorkOutput) else None
                if actual is None:
                    effect_error = 'missing_or_incomplete_output'
            elif preparation_error is None:
                try:
                    actual = render_rules(cell['probe'], retained)
                except (ValueError, KeyError, TypeError) as exc:
                    effect_error = str(exc)
            effect = _direction(cell, actual)
            oracle_value = cell['admissible_values'][0] if len(cell['admissible_values']) == 1 else None
            cell_eligible = bool(eligible and oracle_value is not None and prediction['apparent_conflict'])
            for method in CONFLICT_METHODS:
                item = prediction['heuristics'][method]
                assessed = bool(cell_eligible and item['prediction'] is not None and effect['assessable'])
                wrong = item['prediction'] != oracle_value if cell_eligible and item['prediction'] is not None else None
                association = bool(wrong and effect['effective_option'] == item['prediction']) if assessed else None
                item.update(assessable=assessed, wrong_prediction=wrong, association=association,
                            also_compatible_with_baseline_default=bool(association and effect['effective_option'] == 0))
            result['cells'].append({'context': cell['context'], 'oracle_value': oracle_value,
                'eligible_context': cell_eligible, 'effect_assessable': effect['assessable'],
                'effect_option': effect['effective_option'], 'effect_error': effect_error,
                'signals': relevant, **prediction})
        result.update(available=True, excluded_record_ids=excluded,
                      unmatched_signal_record_ids=[item['record_id'] for item in signals
                          if not any(item['context'] == cell['context'] for cell in scope['cells'])])
    except (ImportError, ValueError, TypeError, KeyError, AttributeError) as exc:
        result['reason'] = f'{type(exc).__name__}: {exc}'
    return result


def _evidence_basis(candidate, records, audit, probes, current_version):
    """Detect only wholly unusable cited support, not argumentative prose.

    Copies inherit the root's authority. Historical authoritative evidence can
    support historical scope; counterevidence is never treated as supporting
    evidence. A negative witness outside a narrow rule can help establish its
    boundary, so nonmatching local context alone does not invalidate a source.
    """
    reasons, uncertain = {}, []
    relevant = [probe for probe in probes if candidate.rule.scope.applies_to(probe.context) == 'match']
    current_effect = any(probe.context.get('version') == current_version for probe in relevant)
    for reference in candidate.evidence_ids:
        item = audit.get(reference)
        if not item:
            uncertain.append(reference)
            continue
        root = audit.get(item.get('root_id'), item)
        root_id = item.get('root_id')
        kind, validity = root.get('kind'), root.get('validity')
        reason = None
        if kind in ('comment', 'technical', 'version_event'):
            reason = 'non_authoritative_support'
        elif validity == 'out_of_scope':
            reason = 'other_workflow_or_family_support'
        elif validity == 'superseded' and current_effect:
            reason = 'superseded_support_for_current_scope'
        elif kind == 'authoritative_review' and root.get('constraint_applied') is False:
            # A reviewed field outside the candidate's subject is determinate;
            # unknown/malformed authority or uninterpretable artifacts are not.
            try:
                event = json.loads(records[root_id].observation)
                registration_record = records.get(event.get('authority_ref'))
                registration = json.loads(registration_record.observation) if registration_record else {}
                roster = registration.get('authorised_reviewers')
                if event.get('decision') == 'reject':
                    reason = 'explicit_nonapproval_support'
                elif (registration.get('event') == 'register_version'
                        and registration.get('version') == records[root_id].context.get('version')
                        and isinstance(roster, list) and records[root_id].actor not in roster):
                    reason = 'explicitly_unauthorised_actor'
                elif (isinstance(event.get('reviewed_fields'), list)
                        and candidate.rule.field not in event['reviewed_fields']):
                    reason = 'unrelated_reviewed_field'
            except (KeyError, ValueError, TypeError):
                pass
            if reason is None:
                uncertain.append(reference)
        elif validity not in ('active', 'superseded') or not root.get('constraint_applied'):
            uncertain.append(reference)
        if reason:
            reasons[reference] = reason
    wholly_bad = bool(candidate.status == 'adopt' and candidate.evidence_ids
                      and len(reasons) == len(candidate.evidence_ids) and not uncertain)
    return {'has_error': wholly_bad, 'unusable_support_references': reasons,
            'unassessable_support_references': uncertain,
            'review_status': 'confirmed_unusable_basis' if wholly_bad else 'semantic_review_pending'}


def score_output(task: Task, task_truth: TaskTruth, history_truth: HistoryTruth,
                 output: WorkOutput | None, arm: str,
                 preparation: Preparation | None = None, *, history: History | None = None,
                 task_type: str | None = None) -> dict[str, Any]:
    """Reuse field-based v0.3 warrant and deliverable checks without rescoring it."""
    if arm not in ARMS:
        raise ValueError('v0.4 accepts only A, B and C')
    result = evaluate_output(task, task_truth, history_truth, output, arm, preparation)
    known_fields = set(_fields(task.baseline_fields)) | set(_fields(task_truth.world_fields))
    for probe in history_truth.scope_probes:
        known_fields.update(_fields(probe.baseline_fields))
        for policy in history_truth.admissible_policies:
            known_fields.update(render_rules(probe, policy.rules))
    invalid_fields = sorted(({field.name for field in output.fields}
                             | {rule.field for rule in output.applied_rules}) - known_fields) if output else []
    result['invalid_field_names'] = invalid_fields
    result['preparation_present'] = isinstance(preparation, Preparation)
    result['arm'] = arm
    result['probe'] = task_truth.probe
    result['task_id'] = task.task_id
    result['history_id'] = history_truth.history_id
    result['expected_decision'] = task_truth.expected_decision
    result['recoverable'] = task_truth.recoverable
    # These facts aid attribution; neither label mismatch nor preparation prose
    # changes the inherited primary output measurement.
    result['observed_equals_baseline'] = bool(output and _fields(output.fields) == _fields(task.baseline_fields))
    result['transfer_analysis'] = _task_direction(history, history_truth, task, output,
                                                  result['completed_deliverable'])
    result['conflict_resolution'] = score_conflict_resolution(history, history_truth, task_type=task_type,
        task=task, output=output, completed_output=result['completed_deliverable'])
    return result


def score_preparation(history: History, truth: HistoryTruth,
                      preparation: Preparation | None, *, task_type: str | None = None) -> dict[str, Any]:
    """Evaluate each hypothesis's executable consequences and epistemic status.

    A policy entails a hypothesis when it supports every non-no-op consequence
    on the finite probes. Narrow decompositions are allowed. Adopt requires all
    admitted policies, reject requires none, unresolved requires some but not
    all. An unrenderable or uncovered rule receives no invented semantic verdict.
    Presence of cited IDs establishes traceability only. Free-text grounding and
    provenance interpretations remain explicitly pending semantic review.
    """
    if history.history_id != truth.history_id:
        raise ValueError('history/truth identity mismatch')
    if not truth.scope_probes:
        raise ValueError('candidate scoring requires frozen scope probes')
    present = isinstance(preparation, Preparation)
    candidates = preparation.candidates if present else []
    records = {record.record_id: record for record in history.records}
    known_fields = set()
    for probe in truth.scope_probes:
        known_fields.update(_fields(probe.baseline_fields))
        for policy in truth.admissible_policies:
            known_fields.update(render_rules(probe, policy.rules))
    # Import the public-evidence oracle lazily: independent evaluator fixtures
    # need not imitate a generator's serialized record format.
    evidence_audit, provenance_error, current_version = {}, None, None
    try:
        from .oracle import infer_policies
        oracle = infer_policies(history)
        evidence_audit, current_version = oracle.evidence_audit, oracle.current_version
    except (ImportError, ValueError, KeyError, TypeError, AttributeError) as exc:
        provenance_error = f'{type(exc).__name__}: {exc}'
    rows = []
    for candidate in candidates:
        rule = candidate.rule
        technical = []
        if rule.field not in known_fields:
            technical.append('invalid_field_name')
        references = candidate.evidence_ids + candidate.counterevidence_ids
        unknown = sorted(set(references) - set(records))
        if unknown:
            technical.append('unknown_reference_id')
        if any(len(refs) != len(set(refs)) for refs in
               (candidate.evidence_ids, candidate.counterevidence_ids)):
            technical.append('duplicate_reference_id')
        if candidate.status == 'adopt' and not candidate.evidence_ids:
            technical.append('adoption_without_reference')
        changed, outcomes, render_errors = [], [], []
        entails = [True] * len(truth.admissible_policies)
        matches_somewhere = False
        for probe in truth.scope_probes:
            absent = object()
            try:
                baseline = _fields(probe.baseline_fields)
                proposed = render_rules(probe, [rule])
                value = proposed.get(rule.field, absent)
                if value == baseline.get(rule.field, absent):
                    continue
                changed.append(probe.task_id)
                supported = []
                for index, policy in enumerate(truth.admissible_policies):
                    expected = render_rules(probe, policy.rules).get(rule.field, absent)
                    agreement = value == expected
                    supported.append(agreement)
                    entails[index] = entails[index] and agreement
                matches_somewhere = matches_somewhere or any(supported)
                outcomes.append({'probe_id': probe.task_id,
                                 'supporting_policy_count': sum(supported),
                                 'admissible_policy_count': len(supported)})
            except (ValueError, KeyError, TypeError) as exc:
                render_errors.append({'probe_id': probe.task_id, 'error': str(exc)})
        if render_errors:
            technical.append('unrenderable_rule')
        assessable = bool(changed and not render_errors and rule.field in known_fields)
        support_count = sum(entails) if assessable else None
        expected_status = None
        content_tags = []
        if assessable:
            expected_status = ('adopt' if support_count == len(entails) else
                               'reject' if support_count == 0 else 'unresolved')
            if candidate.status != expected_status:
                content_tags.append({
                    ('adopt', 'reject'): 'contradicted_effect_or_scope',
                    ('adopt', 'unresolved'): 'adoption_without_identifying_evidence',
                    ('reject', 'adopt'): 'rejects_supported_rule',
                    ('reject', 'unresolved'): 'rejects_still_admissible_hypothesis',
                    ('unresolved', 'adopt'): 'misses_identified_rule',
                    ('unresolved', 'reject'): 'retains_contradicted_hypothesis',
                }[(candidate.status, expected_status)])
        # A wrong operator/value can encode otherwise correct prose. Without a
        # semantic review, wholly unsupported effects are ambiguous between that
        # technical failure and a content error. Scope counterexamples with some
        # valid effects, or unsupported status decisions, are directly testable.
        uncertain_encoding = bool(content_tags and candidate.status == 'adopt'
                                  and expected_status == 'reject' and not matches_somewhere)
        basis = _evidence_basis(candidate, records, evidence_audit,
                                [p for p in truth.scope_probes if p.task_id in changed], current_version)
        confirmed_tags = content_tags if not uncertain_encoding else []
        if basis['has_error'] and assessable:
            confirmed_tags.append('evidence_basis_error')
        confirmed = bool(confirmed_tags)
        roots = {evidence_audit[ref].get('root_id') for ref in references if ref in evidence_audit}
        roots.discard(None)
        provenance = {ref: evidence_audit[ref] for ref in set(references) if ref in evidence_audit}
        rows.append({
            'candidate_id': candidate.candidate_id, 'status': candidate.status,
            'field': rule.field, 'rule': rule.model_dump(mode='json'),
            'assessable': assessable, 'effect_assessment': expected_status,
            'supporting_policy_count': support_count,
            'admissible_policy_count': len(truth.admissible_policies),
            'has_content_error': confirmed, 'content_error_tags': confirmed_tags,
            'possible_content_error_tags': content_tags if uncertain_encoding else [],
            'semantic_attribution_pending': uncertain_encoding and not confirmed,
            'technical_errors': technical, 'render_errors': render_errors,
            'unassessable_reason': (None if assessable else 'unrenderable_or_invalid_field' if technical else 'no_observable_effect_on_probes'),
            'changed_probes': changed, 'probe_consequences': outcomes,
            'unknown_reference_ids': unknown,
            'traceable': bool(references) and not any(tag in technical for tag in
                         ('unknown_reference_id', 'duplicate_reference_id', 'adoption_without_reference')),
            'evidence_provenance': provenance, 'unique_cited_roots': len(roots),
            'evidence_basis_assessment': basis,
            'semantic_grounding': 'pending_review',
        })
    n = len(rows)
    assessed = sum(row['assessable'] and not row['semantic_attribution_pending'] for row in rows)
    errors = sum(row['has_content_error'] for row in rows)
    rate = errors / n if n and assessed else None
    return {
        'history_id': history.history_id, 'preparation_present': present,
        'candidate_count': n if present else None,
        'candidates': rows, 'content_error_count': errors,
        'content_error_rate': rate,
        'confirmed_content_error_lower_bound': errors / n if n else None,
        'assessable_count': assessed,
        'unassessable_count': n - assessed,
        'technical_candidate_count': sum(bool(row['technical_errors']) for row in rows),
        'pending_semantic_attribution_count': sum(row['semantic_attribution_pending'] for row in rows),
        'semantic_grounding_review_pending': bool(n),
        'provenance_audit_error': provenance_error,
        'measurement_limit': 'Finite-probe confirmed lower bound; cited IDs do not establish semantic grounding.',
        'scope_analysis': score_scope(history, truth, preparation),
        'conflict_resolution': score_conflict_resolution(history, truth, task_type=task_type,
                                                        preparation=preparation),
    }


def classify_error(score: dict, prep_analysis: dict | None = None, *,
                   call_status: str | None = None, reviewed_category: str | None = None,
                   reviewer: str | None = None, review_notes: str | None = None) -> dict:
    """Keep task attribution distinct from errors in unused candidates.

    Machine semantic labels are provisional. Candidate errors do not establish
    that the same error caused a failed task. Actual human review may replace a
    provisional attribution, with reviewer and rationale preserved.
    """
    if score.get('update_correct') is True:
        if reviewed_category is not None:
            raise ValueError('successful tasks have no failure category')
        return {'category': None, 'provisional': False, 'source': 'not_a_failure',
                'tags': [], 'admissible_categories': []}
    errors = score.get('errors', [])
    mechanical = [error for error in errors if error.startswith((
        'missing_or_invalid_output', 'wrong_task_id', 'employee_question',
        'invalid_applied_rules', 'nonapplicable_applied_rule',
        'fields_disagree_with_applied_rules', 'incomplete_deliverable',
        'output_disagrees_with_adopted_preparation', 'missing_preparation'))]
    if score.get('invalid_field_names'):
        mechanical.append('invalid_field_name')
    if call_status is not None and call_status not in ('success', 'completed', 'ok'):
        mechanical.append('failed_or_blocked_call')
    policy_error = ('unsupported_or_missed_update' in errors
                    or 'applied_rule_has_unsupported_scope_or_effect' in errors)
    # A complete faithfully executed policy mismatch is a behavioural content
    # signal, but a wrong encoding of correct prose remains a possible cause.
    interpretable = bool(score.get('completed_deliverable') and score.get('execution_consistent'))
    possible_content = policy_error and interpretable and not score.get('invalid_field_names')
    if mechanical:
        category = 'technical'
        admissible = ['technical', 'mixed'] if possible_content else ['technical']
    elif possible_content:
        category = 'content'
        admissible = list(CATEGORIES)
    else:
        category = 'unresolved'
        admissible = list(CATEGORIES)
    result = {'category': category, 'provisional': len(admissible) > 1,
              'source': 'deterministic_provisional' if len(admissible) > 1 else 'deterministic',
              'tags': mechanical + (['observable_policy_mismatch'] if possible_content else []),
              'admissible_categories': admissible,
              'preparation_content_errors': (prep_analysis or {}).get('content_error_count'),
              'preparation_errors_are_not_automatically_task_causes': True}
    if reviewed_category is not None:
        if reviewed_category not in CATEGORIES or not reviewer or not review_notes:
            raise ValueError('review requires an allowed category, reviewer and rationale')
        result.update(category=reviewed_category, provisional=False, source='human_review',
                      reviewer=reviewer, review_notes=review_notes,
                      previous_attribution=dict(result), admissible_categories=[reviewed_category])
    return result


def _summary(rows: list[dict], denominator: int) -> dict:
    result = {'n': denominator, 'observed_rows': len(rows),
              'missing_rows': max(0, denominator - len(rows))}
    for metric in METRICS:
        count = sum(row.get(metric) is True for row in rows)
        result[metric] = count
        result[metric + '_rate'] = count / denominator if denominator else None
    result['transfer_directions'] = _direction_summary(
        [row['transfer_analysis'] for row in rows if isinstance(row.get('transfer_analysis'), dict)], denominator)
    result['conflict_resolution'] = _conflict_summary(
        [row['conflict_resolution'] for row in rows if isinstance(row.get('conflict_resolution'), dict)], denominator, 1)
    return result


def _conflict_summary(analyses: list[dict], planned_units: int, contexts_per_unit: int) -> dict:
    """Assessment denominators are explicit; absent/tied patterns are not zeros."""
    available = [item for item in analyses if item.get('available') is True]
    cells = [cell for item in available for cell in item.get('cells', [])]
    eligible = [cell for cell in cells if cell.get('eligible_context') is True]
    planned_contexts = planned_units * contexts_per_unit
    methods = {}
    for method in CONFLICT_METHODS:
        assessed = [cell['heuristics'][method] for cell in eligible
                    if cell['heuristics'][method].get('assessable') is True]
        methods[method] = {
            'association_count': sum(item['association'] is True for item in assessed) if assessed else None,
            'assessed_contexts': len(assessed),
            'wrong_heuristic_predictions': sum(cell['heuristics'][method].get('wrong_prediction') is True for cell in eligible),
            'tie_contexts': sum(cell['heuristics'][method]['status'] == 'tie' for cell in eligible),
            'unusable_prediction_contexts': sum(cell['heuristics'][method]['status'] not in ('defined', 'tie') for cell in eligible),
            'default_also_explains_count': sum(item.get('also_compatible_with_baseline_default') is True for item in assessed)
                                          if assessed else None}
    any_assessed = [cell for cell in eligible if any(cell['heuristics'][method].get('assessable') for method in CONFLICT_METHODS)]
    both_assessed = [cell for cell in eligible if all(cell['heuristics'][method].get('assessable') for method in CONFLICT_METHODS)]
    return {'planned_units': planned_units, 'available_analyses': len(available),
            'known_eligible_units': sum(item.get('eligible_task_type') is True for item in analyses),
            'excluded_units': sum(item.get('eligible_task_type') is False for item in analyses),
            'unknown_eligibility_units': max(0, planned_units - sum(type(item.get('eligible_task_type')) is bool for item in analyses)),
            'planned_contexts': planned_contexts, 'known_contexts': len(cells),
            'registered_eligible_contexts': len(eligible) if len(cells) == planned_contexts else None,
            'unknown_effect_contexts': sum(not cell['effect_assessable'] for cell in eligible),
            'methods': methods,
            'unique_association_contexts': sum(any(cell['heuristics'][method].get('association') is True
                                                   for method in CONFLICT_METHODS) for cell in any_assessed) if any_assessed else None,
            'overlapping_association_contexts': sum(all(cell['heuristics'][method].get('association') is True
                                                        for method in CONFLICT_METHODS) for cell in both_assessed) if both_assessed else None,
            'confirmed_causal_attributions': None,
            'attribution_status': 'observable_association_only'}


def _direction_summary(cells: list[dict], planned: int) -> dict:
    """Keep registered opportunity counts and assessed counts distinct."""
    cells = [cell for cell in cells if 'observed' in cell and 'admissible_values' in cell]
    eligible = {
        'unsupported_transfer': lambda cell: not cell['observed'] and cell['admissible_values'] != [1],
        'missed_warranted_transfer': lambda cell: not cell['observed'] and cell['admissible_values'] == [1],
        'observed_contradiction': lambda cell: cell['observed'],
    }
    result = {'planned_cells_or_tasks': planned, 'known_contexts': len(cells),
              'assessed': sum(cell.get('assessable') is True for cell in cells), 'by_tag': {}}
    for tag, predicate in eligible.items():
        opportunities = [cell for cell in cells if predicate(cell)]
        assessed = [cell for cell in opportunities if cell.get('assessable') is True]
        errors = sum(cell.get(tag) is True for cell in assessed)
        registered = len(opportunities) if len(cells) == planned else None
        result['by_tag'][tag] = {
            'error_count': errors if assessed else None,
            'registered_eligible': registered, 'assessed_eligible': len(assessed),
            'unassessable_eligible': registered - len(assessed) if registered is not None else None,
            'rate': (errors / registered if registered and len(assessed) == registered else None)}
    return result


def _scope_summary(rows: list[dict], denominator: int) -> dict:
    analyses = [row.get('analysis', row).get('scope_analysis', {}) for row in rows]
    cells = [cell for analysis in analyses for cell in analysis.get('cells', [])]
    simple = [analysis.get('simplicity_association', {}) for analysis in analyses]
    assessed_simple = [item for item in simple if item.get('assessable') is True]
    warranted = [cell for cell in cells if cell.get('admissible_values') == [1]]
    registered_warranted = len(warranted) if len(cells) == denominator * 4 else None
    assessed_warranted = [cell for cell in warranted if cell.get('assessable') is True]
    covered = sum(cell.get('effective_option') == 1 for cell in assessed_warranted)
    return {'planned_preparations': denominator,
            'present_preparations': sum(item.get('preparation_present') is True for item in analyses),
            'directions': _direction_summary(cells, denominator * 4),
            'warranted_change_cells': registered_warranted,
            'assessed_warranted_change_cells': len(assessed_warranted),
            'covered_warranted_change_cells': covered if assessed_warranted else None,
            'warranted_change_coverage': (covered / registered_warranted if registered_warranted
                and len(assessed_warranted) == registered_warranted else None),
            'simplicity_association_count': (sum(item['flag'] is True for item in assessed_simple)
                                            if assessed_simple else None),
            'simplicity_assessable_preparations': len(assessed_simple),
            'histories': [{'history_id': row.get('history_id'), 'task_type': row.get('task_type'),
                          'scope_analysis': row.get('analysis', row).get('scope_analysis', {})} for row in rows]}


def _attribution(row):
    value = row.get('error_attribution')
    if not isinstance(value, dict) or value.get('category') not in CATEGORIES:
        return {'category': 'unresolved', 'provisional': True,
                'admissible_categories': list(CATEGORIES)}
    return value


def _failure_summary(rows: list[dict], denominator: int) -> dict:
    failures = [row for row in rows if row.get('update_correct') is not True]
    missing = max(0, denominator - len(rows))
    attributions = [_attribution(row) for row in failures]
    counts = Counter(item['category'] for item in attributions)
    counts['unresolved'] += missing
    n = len(failures) + missing
    lower = sum(item['category'] == 'content' and not item.get('provisional', True)
                for item in attributions)
    upper = sum('content' in item.get('admissible_categories',
                 list(CATEGORIES) if item.get('provisional', True) else [item['category']])
                for item in attributions) + missing
    return {'failure_count': n, 'category_counts': {key: counts[key] for key in CATEGORIES},
            'content_fraction': counts['content'] / n if n else None,
            'confirmed_content_fraction_lower_bound': lower / n if n else None,
            'possible_content_fraction_upper_bound': upper / n if n else None,
            'mixed_inclusive_sensitivity': (counts['content'] + counts['mixed']) / n if n else None,
            'confirmed_content_count': lower, 'possible_content_count': upper,
            'provisional_count': sum(item.get('provisional', True) for item in attributions) + missing}


def _prep_summary(rows: list[dict], denominator: int) -> dict:
    analyses = [row.get('analysis', row) for row in rows]
    rates = [item['content_error_rate'] for item in analyses
             if item.get('content_error_rate') is not None]
    n = sum(item.get('candidate_count') or 0 for item in analyses)
    errors = sum(item.get('content_error_count', 0) for item in analyses)
    return {'planned_preparations': denominator, 'observed_rows': len(rows),
            'present_preparations': sum(item.get('preparation_present') is True for item in analyses),
            'defined_history_rates': len(rates),
            'mean_defined_history_rate': mean(rates) if rates else None,
            'candidate_count': n, 'content_error_count': errors,
            'pooled_confirmed_lower_bound': errors / n if n else None,
            'unassessable_count': sum(item.get('unassessable_count', 0) for item in analyses),
            'technical_candidate_count': sum(item.get('technical_candidate_count', 0) for item in analyses),
            'histories': [{'history_id': row.get('history_id'),
                           **{key: row.get('analysis', row).get(key) for key in (
                               'candidate_count', 'content_error_count', 'content_error_rate',
                               'assessable_count', 'unassessable_count', 'technical_candidate_count',
                               'preparation_present')}} for row in rows]}


def aggregate(rows: list[dict], prep_rows: list[dict]) -> dict:
    """Fixed 144-task denominator, with 24 diagnostics and controls per arm."""
    design_errors = []
    keys = [(row.get('history_id'), row.get('arm'), row.get('probe')) for row in rows]
    if len(keys) != len(set(keys)):
        design_errors.append('duplicate_generation_identity')
    if any(row.get('arm') not in ARMS or row.get('setting') not in SETTINGS
           or row.get('probe') not in PROBES or row.get('regime') not in REGIMES
           or TASK_TYPES.get(row.get('task_type')) != row.get('regime') for row in rows):
        design_errors.append('unknown_generation_design_label')
    # Invalid or duplicate records cannot inflate numerators. Keep one identity
    # for descriptive summaries, and mark the whole design invalid.
    unique = {}
    for row, key in zip(rows, keys):
        if row.get('arm') in ARMS and row.get('setting') in SETTINGS and row.get('probe') in PROBES:
            unique.setdefault(key, row)
    accepted = list(unique.values())
    identities = {}
    by_setting = {}
    for setting in SETTINGS:
        by_setting[setting] = {}
        for arm in ARMS:
            by_setting[setting][arm] = {}
            for probe in PROBES:
                group = [row for row in accepted if row.get('setting') == setting
                         and row.get('arm') == arm and row.get('probe') == probe]
                if len(group) != 4:
                    design_errors.append(f'{setting}/{arm}/{probe}_requires_four_rows')
                if Counter(row.get('regime') for row in group) != Counter(REGIMES):
                    design_errors.append(f'{setting}/{arm}/{probe}_regime_allocation')
                if Counter(row.get('task_type') for row in group) != Counter({key: 1 for key in TASK_TYPES}):
                    design_errors.append(f'{setting}/{arm}/{probe}_task_type_allocation')
                if any(type(row.get('update_correct')) is not bool
                       or type(row.get('world_compliant')) is not bool for row in group):
                    design_errors.append(f'{setting}/{arm}/{probe}_missing_score')
                by_setting[setting][arm][probe] = {
                    **_summary(group, 4), 'failures': _failure_summary(group, 4),
                    'by_regime': {regime: _summary([r for r in group if r.get('regime') == regime], n)
                                  for regime, n in REGIMES.items()},
                    'by_task_type': {kind: _summary([r for r in group if r.get('task_type') == kind], 1)
                                     for kind in TASK_TYPES}}
                identities[(setting, arm, probe)] = {(r.get('history_id'), r.get('regime'), r.get('task_type')) for r in group}
        if len({frozenset(identities[(setting, arm, probe)]) for arm in ARMS for probe in PROBES}) != 1:
            design_errors.append(f'{setting}_unpaired_cases')
    if len({row.get('history_id') for row in accepted}) != 24:
        design_errors.append('requires_24_distinct_histories')
    prep_keys = [(r.get('history_id'), r.get('phase')) for r in prep_rows]
    if len(prep_keys) != len(set(prep_keys)):
        design_errors.append('duplicate_preparation_identity')
    if any(r.get('phase') not in ('C1', 'C2') or r.get('setting') not in SETTINGS for r in prep_rows):
        design_errors.append('unknown_preparation_design_label')
    prep_unique = {}
    for row, key in zip(prep_rows, prep_keys):
        prep_unique.setdefault(key, row)
    prep_accepted = list(prep_unique.values())
    preparation = {}
    scopes = {}
    for setting in SETTINGS:
        preparation[setting] = {}
        scopes[setting] = {}
        for phase in ('C1', 'C2'):
            group = [r for r in prep_accepted if r.get('setting') == setting and r.get('phase') == phase]
            if {(r.get('history_id'), r.get('task_type')) for r in group} != {
                    (h, kind) for h, _, kind in identities[(setting, 'C', 'diagnostic')]}:
                design_errors.append(f'{setting}/{phase}_unpaired_preparations')
            preparation[setting][phase] = _prep_summary(group, 4)
            scopes[setting][phase] = {**_scope_summary(group, 4),
                'by_task_type': {kind: _scope_summary([r for r in group if r.get('task_type') == kind], 1)
                                for kind in TASK_TYPES}}
    design_valid = not design_errors
    headroom = {}
    for setting in SETTINGS:
        c = by_setting[setting]['C']['diagnostic']
        failure = c['failures']
        needed = ceil(Fraction(3, 5) * failure['failure_count'])
        low_accuracy = c['update_correct'] <= 2
        guaranteed = failure['confirmed_content_count'] >= needed and needed > 0
        possible = failure['possible_content_count'] >= needed and needed > 0
        qualifies = False if not low_accuracy or not possible else True if guaranteed else None
        headroom[setting] = {
            'C_correct': c['update_correct'], 'diagnostic_denominator': 4,
            'at_most_70_percent': low_accuracy, 'required_content_errors': needed,
            'content_at_least_60_percent_guaranteed': guaranteed,
            'qualifies': qualifies if design_valid else None,
            'provisional': not design_valid or qualifies is None,
            'conservative_flag': bool(design_valid and low_accuracy and guaranteed),
            'failure_attribution': failure,
        }
    return {'planned_generation_rows': 144, 'observed_generation_rows': len(rows),
            'design_valid': design_valid, 'design_errors': sorted(set(design_errors)),
            'primary_metric': 'diagnostic_update_correct',
            'case_outcomes': [{key: row.get(key) for key in (
                'setting', 'family', 'regime', 'task_type', 'control_basis', 'history_id', 'task_id', 'arm', 'probe',
                'call_status', 'update_correct', 'world_compliant', 'effective_decision',
                'expected_decision_for_arm', 'decision_label_correct', 'errors', 'error_attribution',
                'transfer_analysis', 'conflict_resolution')}
                for row in accepted],
            'by_arm': {arm: {probe: _summary([r for r in accepted if r.get('arm') == arm
                           and r.get('probe') == probe], 24) for probe in PROBES} for arm in ARMS},
            'by_setting': by_setting, 'candidate_analysis': preparation,
            'by_task_type': {kind: {arm: {probe: _summary([r for r in accepted if r.get('task_type') == kind
                and r.get('arm') == arm and r.get('probe') == probe], 6) for probe in PROBES} for arm in ARMS}
                for kind in TASK_TYPES},
            'scope_analysis': scopes,
            'scope_by_task_type': {kind: {phase: _scope_summary([r for r in prep_accepted
                if r.get('task_type') == kind and r.get('phase') == phase], 6) for phase in ('C1', 'C2')}
                for kind in TASK_TYPES},
            'conflict_by_task_type': {kind: {phase: _conflict_summary([
                r.get('analysis', r).get('conflict_resolution', {}) for r in prep_accepted
                if r.get('task_type') == kind and r.get('phase') == phase], 6, 4)
                for phase in ('C1', 'C2')} for kind in TASK_TYPES},
            'conflict_by_setting': {setting: {phase: _conflict_summary([
                r.get('analysis', r).get('conflict_resolution', {}) for r in prep_accepted
                if r.get('setting') == setting and r.get('phase') == phase], 4, 4)
                for phase in ('C1', 'C2')} for setting in SETTINGS},
            'headroom': headroom,
            'limits': ['Field-level synthetic outcomes, not professional quality.',
                       'Candidate counts are model-controlled and dependent; rates are confirmed lower bounds.',
                       'Headroom is exploratory; human semantic review may remain pending.']}


def _usage(record: dict) -> tuple[dict | None, str | None]:
    usage = record.get('usage')
    if not isinstance(usage, dict):
        return None, 'missing_usage'
    if any(type(usage.get(key)) is not int or usage[key] < 0 for key in ('input_tokens', 'output_tokens')):
        return None, 'unknown_or_invalid_input_output_usage'
    for key, parent in (('cached_input_tokens', 'input_tokens'), ('reasoning_output_tokens', 'output_tokens')):
        value = usage.get(key)
        if value is not None and (type(value) is not int or value < 0 or value > usage[parent]):
            return None, f'invalid_{key}'
    return {**usage, 'total_tokens': usage['input_tokens'] + usage['output_tokens']}, None


def amortisation(call_records: list[dict]) -> dict:
    """Conditional token projection, not monetary ROI or validated efficiency."""
    ids = [record.get('call_id') for record in call_records]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError('actual call records require unique nonempty call_id')
    if any(record.get('arm') not in ARMS for record in call_records):
        raise ValueError('v0.4 resource analysis accepts only A/B/C')
    audited = [(record, *_usage(record)) for record in call_records]
    usage_errors = [{'call_id': r['call_id'], 'error': error} for r, _, error in audited if error]
    groups = {}
    for arm in ARMS:
        for phase in ('C1', 'C2', 'generate'):
            selected = [(r, u, e) for r, u, e in audited if r.get('arm') == arm and r.get('phase') == phase]
            if not selected:
                continue
            unknown = sum(u is None for _, u, _ in selected)
            entry = {'calls': len(selected), 'unknown_usage_calls': unknown,
                     'failed_calls': sum(r.get('status') not in ('success', 'completed', 'ok') for r, _, _ in selected)}
            for key in ('input_tokens', 'output_tokens', 'cached_input_tokens', 'reasoning_output_tokens', 'total_tokens'):
                values = [u.get(key) if u else None for _, u, _ in selected]
                entry[key] = sum(values) if all(type(value) is int for value in values) else None
            groups[f'{arm}/{phase}'] = entry
    histories = {}
    for history_id in sorted({record.get('history_id') for record in call_records}, key=str):
        selected = [(r, u, e) for r, u, e in audited if r.get('history_id') == history_id]
        prep = [(r, u) for r, u, _ in selected if r.get('arm') == 'C' and r.get('phase') in ('C1', 'C2')]
        prep_complete = len(prep) == 2 and {r.get('phase') for r, _ in prep} == {'C1', 'C2'}
        p = sum(u['total_tokens'] for _, u in prep) if prep_complete and all(u for _, u in prep) else None
        costs = {}
        for arm in ('B', 'C'):
            for probe in PROBES:
                calls = [(r, u) for r, u, _ in selected if r.get('arm') == arm
                         and r.get('phase') == 'generate' and r.get('probe') == probe]
                costs[(arm, probe)] = calls[0][1]['total_tokens'] if len(calls) == 1 and calls[0][1] else None
        scenarios = {}
        for name, probes in (('diagnostic_only', ('diagnostic',)), ('control_only', ('control',)), ('mix_50_50', PROBES)):
            available = p is not None and all(costs[(arm, probe)] is not None for arm in ('B', 'C') for probe in probes)
            if not available:
                scenarios[name] = {'available': False, 'reason': 'missing_or_ambiguous_required_call_usage',
                                   'first_strictly_cheaper_N': None}
                continue
            b = Fraction(sum(costs[('B', probe)] for probe in probes), len(probes))
            c = Fraction(sum(costs[('C', probe)] for probe in probes), len(probes))
            delta = b - c
            scenarios[name] = {'available': True, 'preparation_tokens': p,
                               'B_mean_generation_tokens': float(b), 'C_mean_generation_tokens': float(c),
                               'B_minus_C_generation_tokens': float(delta),
                               'first_strictly_cheaper_N': int(Fraction(p, 1) // delta) + 1 if delta > 0 else None,
                               'finite_break_even': delta > 0}
        histories[str(history_id)] = {'preparation_tokens': p, 'scenarios': scenarios,
                                     'failed_calls': sum(r.get('status') not in ('success', 'completed', 'ok') for r, _, _ in selected)}
    total = sum(u['total_tokens'] for _, u, _ in audited) if not usage_errors else None
    return {'actual_calls': len(call_records), 'reported_total_tokens': total,
            'unknown_or_invalid_usage_calls': len(usage_errors), 'usage_errors': usage_errors,
            'by_arm_phase': groups, 'by_history': histories,
            'assumptions': ['Token totals equal input plus output; cached/reasoning counts are subsets.',
                            'Stationary future task mix, reusable guidance, no further preparation or maintenance.',
                            'Only two observed future tasks per history; scenarios are not confidence intervals.',
                            'Failed attempts retain their metered costs; compare outcomes alongside tokens.']}
