"""Seeded surface variation without changing publicly warranted observations."""

import json
import random
from datetime import datetime, timedelta

from reflectai_v03.contracts import History

from .oracle import infer_policies, read_frame

PERSON_NAMES = ('Anika', 'Jonas', 'Elena', 'Robin', 'Theo', 'Daria')
REVIEW_COMMENTS = ('Approved.', 'Reviewed.', 'Checked.', 'Review complete.', 'Recorded.', 'Completed.')
NEUTRAL_COMMENTS = REVIEW_COMMENTS[1:]


def _parse(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def _stamp(value):
    return value.isoformat(timespec='seconds').replace('+00:00', 'Z')


def _date_pool(registration, as_of, issued, rng):
    start = max(_parse(registration['valid_from']), issued)
    end = min(_parse(registration['valid_until']) - timedelta(seconds=1), as_of)
    first = max(start.date() + timedelta(days=1), end.date() - timedelta(days=28))
    last = end.date() - timedelta(days=1)
    count = (last - first).days + 1
    if count < 3:
        raise ValueError('presentation requires three full days within a registered interval')
    return [first + timedelta(days=offset) for offset in rng.sample(range(count), 3)]


def present_history(history: History, seed: int) -> History:
    """Use public approval semantics to construct shared positive/negative support.

    This changes timestamps, comments, nonbinding actors and delivered order.
    Configuration, artifact values, provenance links and approved assignments stay fixed.
    """
    rng = random.Random(seed)
    before = infer_policies(history)
    frame = read_frame(history)
    result = history.model_copy(deep=True)
    records = {record.record_id: record for record in result.records}
    bodies = {key: json.loads(record.observation) for key, record in records.items()}
    as_of = _parse(frame.as_of)
    pools = {version: _date_pool(registration, as_of,
                                _parse(records[registration['registry_id']].timestamp), rng)
             for version, registration in before.versions.items()}
    current = before.current_version
    current_approvals = [record_id for record_id, item in before.evidence_audit.items()
                         if item['constraint_applied'] and item['validity'] == 'active']
    if len(current_approvals) != 3:
        raise ValueError('the registered presentation expects three current approvals')
    comments = ['Approved.', *rng.sample(NEUTRAL_COMMENTS, 2)]
    rng.shuffle(comments)
    times = {}
    for index, record_id in enumerate(current_approvals):
        date = pools[current][index]
        hour_start = datetime(date.year, date.month, date.day, rng.randrange(8, 18), tzinfo=as_of.tzinfo)
        # Exclude only exact hour endpoints so both surrounding examples fit in the hour.
        times[record_id] = hour_start + timedelta(seconds=rng.randrange(1, 3599))
        bodies[record_id]['comment'] = comments[index]

    def ordinary_time(version):
        date = rng.choice(pools[version])
        return datetime(date.year, date.month, date.day, rng.randrange(8, 18),
                        rng.randrange(60), rng.randrange(60), tzinfo=as_of.tzinfo)

    hard_negatives = {'unauthorised': [], 'unreviewed': []}
    forwards = []
    for record_id, record in records.items():
        body = bodies[record_id]
        event = body.get('event')
        if event == 'register_version' or record_id in current_approvals:
            continue
        if event == 'forward':
            forwards.append(record_id)
            continue
        version = record.context.get('version')
        if version not in pools:
            raise ValueError('work record has no public version interval')
        times[record_id] = ordinary_time(version)
        if event == 'review':
            record.kind = 'review'
            roster = before.versions[version]['authorised_reviewers']
            if body.get('decision') == 'accept':
                bodies[record_id]['comment'] = rng.choice(REVIEW_COMMENTS)
                if record.actor not in roster:
                    names = [name for name in PERSON_NAMES if name not in roster]
                    record.actor = rng.choice(names)
                    if version == current:
                        hard_negatives['unauthorised'].append(record_id)
                elif frame.field_option.field not in body.get('reviewed_fields', []):
                    if version == current:
                        hard_negatives['unreviewed'].append(record_id)
            else:
                body['comment'] = rng.choice(NEUTRAL_COMMENTS)
                body['rejection_reason'] = rng.choice([
                    'The signature block is missing. Field-level review was not completed.',
                    'Missing signature block; the artifact was returned before field review.',
                    'Review stopped at the missing signature block. Target-field checks remain open.',
                ])
        elif event == 'preference':
            record.actor = rng.choice(PERSON_NAMES)
            fields = body['proposed_fields']
            field = frame.field_option.field
            proposed = f'{field} set to {fields[field]!r}' if field in fields else f'{field} omitted'
            body['message'] = rng.choice([
                f'I would prefer {proposed} for this item.',
                f'My personal choice here would be {proposed}.',
                f'For my version I would use {proposed}.',
            ])
        elif event == 'execution':
            body['log'] = rng.choice([
                'The request completed on retry.', 'Retry completed successfully.',
                'The first attempt failed; the next attempt completed.',
            ])

    # Paired examples guarantee shared date, hour and comment support for both hard-negative kinds.
    for group in hard_negatives.values():
        rng.shuffle(group)
        for index, record_id in enumerate(group):
            if index < 6:
                anchor_index = index // 2
                anchor = times[current_approvals[anchor_index]]
                hour_start = anchor.replace(minute=0, second=0)
                anchor_second = int((anchor - hour_start).total_seconds())
                offset = (rng.randrange(anchor_second) if index % 2 == 0
                          else rng.randrange(anchor_second + 1, 3600))
                times[record_id] = hour_start + timedelta(seconds=offset)
                bodies[record_id]['comment'] = comments[anchor_index]
            else:
                times[record_id] = ordinary_time(current)
                bodies[record_id]['comment'] = rng.choice(REVIEW_COMMENTS)

    # A forward may be listed anywhere, but its timestamp remains after its visible source.
    pending = list(forwards)
    while pending:
        assigned = False
        for record_id in list(pending):
            body, record = bodies[record_id], records[record_id]
            origin = body.get('origin_ref')
            if origin not in records:
                raise ValueError('presentation cannot timestamp a forward with missing origin')
            if origin in pending:
                continue
            source_time = times.get(origin, _parse(records[origin].timestamp))
            registration = before.versions[record.context['version']]
            start = max(source_time + timedelta(seconds=1), _parse(registration['valid_from']),
                        _parse(records[registration['registry_id']].timestamp))
            end = min(as_of, _parse(registration['valid_until']) - timedelta(seconds=1))
            candidate = ordinary_time(record.context['version'])
            if candidate < start:
                candidate = start + timedelta(seconds=rng.randrange(1, 301))
            if candidate > end:
                raise ValueError('no valid time after the forward origin')
            times[record_id] = candidate
            body['message'] = rng.choice([
                'Forwarded artifact for the next work item.',
                'Sharing the linked artifact with the working group.',
                'Attached by reference from the earlier review.',
            ])
            pending.remove(record_id)
            assigned = True
        if not assigned:
            raise ValueError('cyclic forward provenance')

    for record_id, record in records.items():
        body = bodies[record_id]
        if record_id in times:
            record.timestamp = _stamp(times[record_id])
            if 'facts' in body:
                body['facts']['date'] = record.timestamp[:10]
            field_maps = [body.get(key) for key in ('accepted_fields', 'rejected_fields', 'proposed_fields')]
            field_maps += [artifact.get('fields') for artifact in body.get('artifacts', {}).values()]
            for fields in field_maps:
                if isinstance(fields, dict) and 'delivery_timestamp' in fields:
                    fields['delivery_timestamp'] = record.timestamp
        record.observation = json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    rng.shuffle(result.records)
    after = infer_policies(result)
    if before.policies != after.policies or before.constraints != after.constraints:
        # Record order is irrelevant to the constraint set.
        signature = lambda rows: sorted(json.dumps(row, sort_keys=True) for row in rows)
        if before.policies != after.policies or signature(before.constraints) != signature(after.constraints):
            raise ValueError('presentation changed the publicly supported requirement policies')
    return result
