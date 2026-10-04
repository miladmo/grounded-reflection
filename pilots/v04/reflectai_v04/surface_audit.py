"""Frozen, surface-only selectors and public-convention material diagnostics.

Population membership and labels use public semantics. Predictors receive only
the seven explicitly projected surface features, never those semantic fields.
"""

from collections import defaultdict
from datetime import datetime
from fractions import Fraction
import json

from reflectai_v03.contracts import History

from .oracle import infer_policies, read_frame

FEATURES = ('date', 'day', 'hour', 'minute', 'minute_of_day', 'comment', 'position_quartile')
POPULATIONS = ('all_non_registration', 'current_accepted_reviews')
FAMILIES = ('date_equality', 'date_threshold', 'day_threshold', 'hour_threshold',
            'minute_threshold', 'clock_quarter_hour_threshold',
            'comment_equality', 'position_quartile', 'constant')


def _histories(cases):
    result = []
    for case in cases:
        if getattr(case, 'split', None) == 'final_test':
            raise ValueError('Surface fitting and review never use final-test cases.')
        history = case if isinstance(case, History) else case.history
        if not isinstance(history, History):
            raise TypeError('Surface audit requires a public History projection.')
        result.append(history)
    ids = [history.history_id for history in result]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError('Surface audit groups must be nonempty and have distinct history IDs.')
    return result


def _time(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def _project(histories):
    populations = {name: [] for name in POPULATIONS}
    structural = []
    for history in histories:
        oracle, frame = infer_policies(history), read_frame(history)
        hard = []
        for index, record in enumerate(history.records):
            event = json.loads(record.observation)
            if event.get('event') == 'register_version':
                continue
            timestamp = _time(record.timestamp)
            # This dictionary is the complete predictor input. Group identifiers,
            # labels and the semantic population selector are kept outside it.
            surface = {'date': timestamp.date().isoformat(), 'day': timestamp.day,
                       'hour': timestamp.hour,
                       'minute': timestamp.minute, 'minute_of_day': 60 * timestamp.hour + timestamp.minute,
                       'comment': event.get('comment') if isinstance(event.get('comment'), str) else None,
                       'position_quartile': min(3, 4 * index // len(history.records))}
            evidence = oracle.evidence_audit[record.record_id]
            row = {'history_id': history.history_id, 'record_id': record.record_id,
                   'timestamp': record.timestamp,
                   'label': bool(evidence['constraint_applied'] and evidence['validity'] == 'active'),
                   'surface': surface}
            populations['all_non_registration'].append(row)
            if (event.get('event') == 'review' and event.get('decision') == 'accept'
                    and record.context.get('version') == oracle.current_version):
                populations['current_accepted_reviews'].append(row)
                # Semantic annotations below are only for construction checks.
                # They are never forwarded to _predict or selector fitting.
                roster = oracle.versions[oracle.current_version]['authorised_reviewers']
                category = ('positive' if row['label'] else 'unauthorised' if record.actor not in roster
                            else 'unreviewed_target' if frame.field_option.field not in event.get('reviewed_fields', [])
                            else 'other_nonbinding')
                hard.append({**row, 'timestamp': timestamp, 'category': category,
                             'record_kind': record.kind})
        structural.append(_construction_history(history.history_id, hard))
    return populations, structural


def _construction_history(history_id, rows):
    positive = [row for row in rows if row['label']]
    negatives = [row for row in rows if not row['label']]
    groups = []
    for category in ('unauthorised', 'unreviewed_target', 'other_nonbinding'):
        negative = [row for row in negatives if row['category'] == category]
        if not negative:
            continue
        shared = {feature: sorted({row['surface'][feature] for row in positive}
                                  & {row['surface'][feature] for row in negative}, key=str)
                  for feature in ('date', 'hour', 'comment')}
        comments = [value for value in shared['comment'] if value]
        positive_joint = {(r['surface']['date'], r['surface']['hour'], r['surface']['comment']) for r in positive}
        negative_joint = {(r['surface']['date'], r['surface']['hour'], r['surface']['comment']) for r in negative}
        before = bool(positive and min(r['timestamp'] for r in negative) < min(r['timestamp'] for r in positive))
        after = bool(positive and max(r['timestamp'] for r in negative) > max(r['timestamp'] for r in positive))
        same_kind = bool(positive and {r['record_kind'] for r in negative} <= {r['record_kind'] for r in positive})
        checks = {'approved_comment_shared': 'Approved.' in comments,
                  'multiple_comments_shared': len(comments) >= 2,
                  'date_support_shared': bool(shared['date']),
                  'hour_support_shared': bool(shared['hour']),
                  'joint_time_comment_support_shared': bool(positive_joint & negative_joint),
                  'negative_before_first_positive': before,
                  'negative_after_last_positive': after,
                  'same_review_record_kind': same_kind}
        applicable = bool(positive) and category != 'other_nonbinding'
        groups.append({'category': category, 'negative_records': len(negative),
                       'shared_values': shared, 'checks': checks,
                       'applicable': applicable, 'passed': all(checks.values()) if applicable else None})
    labels = [row['label'] for row in rows]
    transitions = sum(left != right for left, right in zip(labels, labels[1:]))
    applicable_groups = [group for group in groups if group['applicable']]
    return {'history_id': history_id, 'positive_records': len(positive), 'negative_records': len(negatives),
            'negative_categories': groups, 'label_transitions_in_delivered_order': transitions,
            'mixed_delivered_order': transitions >= 2 if positive and negatives else None,
            'applicable': bool(applicable_groups),
            'passed': all(group['passed'] for group in applicable_groups) if applicable_groups else None,
            'order_check_is_descriptive': True}


def _candidates(rows):
    result = []
    specifications = [
        ('date_equality', 'date', 'eq', sorted({row['surface']['date'] for row in rows})),
        ('date_threshold', 'date', 'le', sorted({row['surface']['date'] for row in rows})),
        ('day_threshold', 'day', 'le', list(range(1, 31))),
        ('hour_threshold', 'hour', 'le', list(range(23))),
        ('minute_threshold', 'minute', 'le', list(range(59))),
        ('clock_quarter_hour_threshold', 'minute_of_day', 'le', list(range(14, 1439, 15))),
        ('comment_equality', 'comment', 'eq', sorted({row['surface']['comment'] for row in rows}, key=lambda x: json.dumps(x))),
        ('position_quartile', 'position_quartile', 'le', [0, 1, 2]),
    ]
    for family, feature, operation, values in specifications:
        for value in values:
            for polarity in (True, False):
                result.append({'family': family, 'feature': feature, 'operation': operation,
                               'value': value, 'polarity': polarity})
    result.extend({'family': 'constant', 'operation': 'constant', 'value': value}
                  for value in (False, True))
    return result


def _predict(selector, surface):
    if set(surface) != set(FEATURES):
        raise ValueError('Predictors accept only the registered public surface projection.')
    if selector['operation'] == 'constant':
        return selector['value']
    feature = selector['feature']
    if feature not in FEATURES:
        raise ValueError('A selector cannot read semantic or private fields.')
    if selector['operation'] == 'eq':
        match = surface[feature] == selector['value']
    elif selector['operation'] == 'le':
        match = surface[feature] <= selector['value']
    else:
        raise ValueError('Unregistered selector operation.')
    return match if selector['polarity'] else not match


def _counts(rows, predictions):
    result = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}
    for row, prediction in zip(rows, predictions):
        result['tp' if prediction and row['label'] else 'fp' if prediction else 'fn' if row['label'] else 'tn'] += 1
    tp, fp, tn, fn = (result[key] for key in ('tp', 'fp', 'tn', 'fn'))
    positive, negative = tp + fn, tn + fp
    recall = tp / positive if positive else None
    specificity = tn / negative if negative else None
    return {**result, 'records': len(rows), 'positive_records': positive, 'negative_records': negative,
            'precision': tp / (tp + fp) if tp + fp else None,
            'recall': recall, 'specificity': specificity,
            'balanced_accuracy': (recall + specificity) / 2 if positive and negative else None}


def _evaluate(rows, history_ids, selector=None, *, oracle_reference=False):
    predictions = ([row['label'] for row in rows] if oracle_reference else
                   [_predict(selector, row['surface']) for row in rows])
    groups = {hid: ([], []) for hid in history_ids}
    for row, prediction in zip(rows, predictions):
        groups[row['history_id']][0].append(row)
        groups[row['history_id']][1].append(prediction)
    by_history = [{'history_id': hid, **_counts(*groups[hid])} for hid in history_ids]
    defined = [row for row in by_history if row['positive_records'] and row['negative_records']]
    exact = [(Fraction(row['tp'], row['positive_records']) + Fraction(row['tn'], row['negative_records'])) / 2
             for row in defined]
    macro = sum(exact, Fraction()) / len(exact) if exact else None
    return ({**_counts(rows, predictions), 'history_count': len(history_ids),
             'history_macro_balanced_accuracy': float(macro) if macro is not None else None,
             'defined_balanced_accuracy_groups': len(defined),
             'undefined_balanced_accuracy_groups': len(history_ids) - len(defined),
             'by_history': by_history}, macro)


def _fit(rows, history_ids):
    """Only development data enters this function, including tie-breaking."""
    winners = {}
    for selector in _candidates(rows):
        metrics, score = _evaluate(rows, history_ids, selector)
        if score is None:
            continue
        previous = winners.get(selector['family'])
        # Candidate order is the registered deterministic tie-break order.
        if previous is None or score > previous[2]:
            winners[selector['family']] = (selector, metrics, score)
    ordered = [winners[family] for family in FAMILIES if family in winners]
    overall = max(ordered, key=lambda item: item[2]) if ordered else None
    return winners, overall


def _overlap(rows):
    result = {}
    both_classes = {row['label'] for row in rows} == {False, True}
    for feature in (*FEATURES, 'exact_timestamp', 'joint_signature'):
        values = defaultdict(lambda: [0, 0])
        for row in rows:
            value = ((row['timestamp'], row['surface']['comment'], row['surface']['position_quartile'])
                     if feature == 'joint_signature' else row['timestamp'] if feature == 'exact_timestamp'
                     else row['surface'][feature])
            values[value][int(row['label'])] += 1
        shared = [value for value, counts in values.items() if all(counts)]
        result[feature] = {'distinct_values': len(values), 'cross_class_shared_values': len(shared),
                           'positive_only_values': sum(not n and bool(p) for n, p in values.values()),
                           'negative_only_values': sum(bool(n) and not p for n, p in values.values()),
                           'exact_observed_separation': not shared if both_classes else None,
                           'shared_values': sorted(shared, key=str),
                           'interpretation': 'In-sample signature overlap, not held-out predictive performance.'}
    return result


def _structure_summary(rows):
    applicable = [row for row in rows if row['applicable']]
    return {'histories': rows, 'applicable_histories': len(applicable),
            'inapplicable_histories': len(rows) - len(applicable),
            'failed_history_ids': [row['history_id'] for row in applicable if not row['passed']],
            'passed': all(row['passed'] for row in applicable) if applicable else None}


def audit_surfaces(development_cases, review_cases, selected_history_ids) -> dict:
    """Fit once on development groups, then evaluate frozen selectors twice."""
    development, review = _histories(development_cases), _histories(review_cases)
    dev_ids, review_ids = ([history.history_id for history in group] for group in (development, review))
    selected_ids = list(selected_history_ids)
    if set(dev_ids) & set(review_ids):
        raise ValueError('Development and held-out review histories must be disjoint.')
    if len(set(selected_ids)) != len(selected_ids) or not set(selected_ids) <= set(review_ids):
        raise ValueError('Selected review IDs must be a unique subset of held-out review groups.')
    dev_populations, dev_structure = _project(development)
    review_populations, review_structure = _project(review)
    populations, perfect = {}, []
    for population in POPULATIONS:
        dev, heldout = dev_populations[population], review_populations[population]
        selected = [row for row in heldout if row['history_id'] in selected_ids]
        winners, overall = _fit(dev, dev_ids)

        def evaluate_winner(winner):
            if winner is None:
                return {'selector': None, 'reason': 'No development history has both classes.'}
            selector, train, _ = winner
            return {'selector': selector, 'development': train,
                    'review': _evaluate(heldout, review_ids, selector)[0],
                    'selected_review': _evaluate(selected, selected_ids, selector)[0]}

        family_rows = {family: evaluate_winner(winners.get(family)) for family in FAMILIES}
        if population == 'current_accepted_reviews':
            for family, result in family_rows.items():
                for split in ('review', 'selected_review'):
                    metrics = result.get(split, {})
                    if metrics.get('balanced_accuracy') == 1 and metrics.get('history_macro_balanced_accuracy') == 1:
                        perfect.append({'family': family, 'population': population, 'split': split,
                                        'selector': result['selector']})
        groups = {'development': (dev, dev_ids), 'review': (heldout, review_ids),
                  'selected_review': (selected, selected_ids)}
        populations[population] = {
            'family_winners': family_rows, 'overall_winner': evaluate_winner(overall),
            'constant_baselines': [{'selector': selector,
                                    **{name: _evaluate(rows, ids, selector)[0] for name, (rows, ids) in groups.items()}}
                                   for selector in ({'family': 'constant', 'operation': 'constant', 'value': False},
                                                    {'family': 'constant', 'operation': 'constant', 'value': True})],
            'source_oracle_reference': {'role': 'Defining public convention; perfect agreement is tautological, not validation.',
                                       **{name: _evaluate(rows, ids, oracle_reference=True)[0]
                                          for name, (rows, ids) in groups.items()}},
            'overlap': {name: _overlap(rows) for name, (rows, _) in groups.items()}}
    structure = {'development': _structure_summary(dev_structure), 'review': _structure_summary(review_structure),
                 'selected_review': _structure_summary([row for row in review_structure if row['history_id'] in selected_ids])}
    failures = [{'split': split, 'history_ids': summary['failed_history_ids']}
                for split, summary in structure.items() if split != 'selected_review' and summary['failed_history_ids']]
    return {'audit_version': 'surface-audit-v1',
            'target': 'Direct, currently binding target-field approval under the public convention.',
            'feature_allowlist': list(FEATURES),
            'development_history_ids': dev_ids, 'review_history_ids': review_ids,
            'selected_history_ids': selected_ids,
            'selection': {'objective': 'development history-macro balanced accuracy',
                          'tie_break': 'fixed family order, ascending threshold/comment values, positive then negative polarity',
                          'family_order': list(FAMILIES), 'review_selection_performed': False,
                          'position_definition': 'floor(4 * delivered_list_index / full_history_length), capped at 3; registry positions included',
                          'comment_definition': 'exact public comment string, or null when absent; no keyword/NLP features'},
            'signature_diagnostic': 'Exact timestamp + exact comment + delivered-position quartile; timestamp is not an additional selector input.',
            'populations': populations, 'construction_checks': structure,
            'readiness': {'requires_investigation': bool(failures or perfect or not structure['review']['applicable_histories']),
                          'construction_failures': failures, 'perfect_heldout_selectors': perfect,
                          'hardnegative_evidence_available': structure['review']['applicable_histories'] > 0,
                          'human_material_approval': 'pending'},
            'limits': ['No final-test cases or model outputs are used.',
                       'Broad-population dates can legitimately distinguish expired approvals.',
                       'Exact joint signatures can memorise small samples; separation is diagnostic, not a hard failure.',
                       'Nonperfect elevated accuracy is reported; it is not equated with chance.',
                       'Mixed list order is descriptive; chance patterns in one short list do not trigger a redraw.',
                       'Only the prespecified surface selectors are tested; other shortcuts may exist.',
                       'This material audit is separate from the inference headroom criterion.']}


def surface_audit_markdown(report):
    def number(value):
        return 'undefined' if value is None else f'{value:.3f}'

    lines = ['# Surface-only material audit', '',
             'Selectors were chosen on development histories and frozen before the disjoint review evaluation.',
             'The selected six reviews are an additional fixed subset, not a model-selection set.', '',
             f"Development / review / selected history counts: {len(report['development_history_ids'])} / "
             f"{len(report['review_history_ids'])} / {len(report['selected_history_ids'])}.",
             f"Investigation required: **{report['readiness']['requires_investigation']}**. Material approval remains pending.", '',
             'The source oracle defines the target. Its apparent perfect agreement is not independent validation.',
             'Balanced accuracy is undefined for one-class groups; they do not receive fabricated negative records.', '']
    for population, analysis in report['populations'].items():
        lines += [f'## {population}', '',
                  '| Development-selected family | Evaluation | TP / FP / TN / FN | Precision | Recall | Specificity | Pooled BA | History-macro BA | Defined / undefined groups |',
                  '| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |']
        for family, result in analysis['family_winners'].items():
            if result['selector'] is None:
                lines.append(f'| {family} | unavailable | — | — | — | — | — | — | no two-class training group |')
                continue
            for split in ('development', 'review', 'selected_review'):
                metrics = result[split]
                counts = ' / '.join(str(metrics[key]) for key in ('tp', 'fp', 'tn', 'fn'))
                values = ' | '.join(number(metrics[key]) for key in ('precision', 'recall', 'specificity', 'balanced_accuracy', 'history_macro_balanced_accuracy'))
                lines.append(f"| {family} | {split} | {counts} | {values} | "
                             f"{metrics['defined_balanced_accuracy_groups']} / {metrics['undefined_balanced_accuracy_groups']} |")
        reference = analysis['source_oracle_reference']['review']
        lines += ['', 'Source-convention reference on review groups (definitional, not validation): '
                  + ' / '.join(str(reference[key]) for key in ('tp', 'fp', 'tn', 'fn'))
                  + f" TP/FP/TN/FN; history-macro BA {number(reference['history_macro_balanced_accuracy'])}; "
                  + f"{reference['undefined_balanced_accuracy_groups']} one-class or empty groups remain undefined."]
        lines += ['', 'Frozen selectors (parameters come only from development):', '', '```json',
                  json.dumps({family: item['selector'] for family, item in analysis['family_winners'].items()}, indent=2),
                  '```', '', f"Overall development winner: `{json.dumps(analysis['overall_winner'].get('selector'))}`.", '',
                  '| Review surface | Distinct values | Cross-class shared values | Exact observed separation |',
                  '| --- | ---: | ---: | --- |']
        for feature, overlap in analysis['overlap']['review'].items():
            lines.append(f"| {feature} | {overlap['distinct_values']} | {overlap['cross_class_shared_values']} | {overlap['exact_observed_separation']} |")
        lines.append('')
    lines += ['## Construction checks and review flags', '',
              'Hard checks concern common comments, day/hour support, earlier/later hard negatives and record kind',
              'within current accepted reviews. Old-version dates in the broad population are not defects.', '',
              '```json', json.dumps(report['readiness'], indent=2), '```', '',
              'The [complete audit](surface-audit.json) contains every selected predictor, constant baseline,',
              'source-oracle reference, per-history denominator and overlap/construction result.', '']
    lines += ['- ' + limit for limit in report['limits']]
    return '\n'.join(lines) + '\n'
