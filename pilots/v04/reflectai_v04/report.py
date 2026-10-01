"""Transparent v0.4 difficulty mapping and conditional resource report."""

from pathlib import Path

from .evaluation import ARMS, CONFLICT_METHODS, DIRECTION_TAGS, PROBES, SETTINGS, TASK_TYPES


def _percent(value):
    return 'undefined' if value is None else f'{100 * value:.1f}%'


def _safe(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def _count(value):
    return 'undefined' if value is None else str(value)


def _direction_count(item):
    return (f"{_count(item['error_count'])}/{_count(item['registered_eligible'])} "
            f"(assessed {item['assessed_eligible']})")


def _scope_tables(lines, summary):
    lines += ['', '## Transfer direction and combined preparation coverage', '',
              'Directions describe actual completed output fields or combined adopted guidance. '
              'They do not prove a causal inference strategy and do not promote provisional '
              'attribution into confirmed content error. Counts below use eligible contexts '
              'for each direction, with assessed counts explicit; missing and unrenderable '
              'results are undefined, not zero errors. C1 and C2 are separate.', '',
              '| Task type | Stage | Unsupported transfer | Missed warranted transfer | Observed contradiction | Warranted change coverage | Simplest-pattern association / assessed preparations |',
              '| --- | --- | --- | --- | --- | --- | --- |']
    for kind in TASK_TYPES:
        for phase in ('C1', 'C2'):
            item = summary['scope_by_task_type'][kind][phase]
            counts = ' | '.join(_direction_count(item['directions']['by_tag'][tag]) for tag in DIRECTION_TAGS)
            lines.append(f"| {kind} | {phase} | {counts} | {_percent(item['warranted_change_coverage'])} "
                         f"({_count(item['covered_warranted_change_cells'])}/{_count(item['warranted_change_cells'])}) | "
                         f"{_count(item['simplicity_association_count'])}/{item['simplicity_assessable_preparations']} "
                         f"(6 planned) |")
    lines += ['', '| Setting | Stage | Unsupported transfer | Missed warranted transfer | Observed contradiction | Assessed cells / planned |',
              '| --- | --- | --- | --- | --- | ---: |']
    for setting in SETTINGS:
        for phase in ('C1', 'C2'):
            item = summary['scope_analysis'][setting][phase]
            counts = ' | '.join(_direction_count(item['directions']['by_tag'][tag]) for tag in DIRECTION_TAGS)
            lines.append(f"| {setting} | {phase} | {counts} | {item['directions']['assessed']}/16 |")
    lines += ['', '| History | Type | Stage | Assessed cells | Unsupported / missed / observed contradiction | Retained mask | All tied minimum masks | Association |',
              '| --- | --- | --- | ---: | --- | --- | --- | --- |']
    for setting in SETTINGS:
        for phase in ('C1', 'C2'):
            for item in summary['scope_analysis'][setting][phase]['histories']:
                scope = item['scope_analysis']
                simple = scope.get('simplicity_association', {})
                counts = ' / '.join(_count(scope.get(tag)) for tag in DIRECTION_TAGS)
                lines.append(f"| {_safe(item['history_id'])} | {item['task_type']} | {phase} | "
                             f"{scope.get('assessed_cells', 0)}/4 | {counts} | "
                             f"{_count(simple.get('retained_effect_mask'))} | "
                             f"{simple.get('tied_minimum_masks', 'undefined')} | {_count(simple.get('flag'))} |")
    lines += ['', 'Masks encode the four public context cells in order, with bit 0 first. '
              'Complexity is a property of the Boolean function: constants 0, one literal 1, '
              'remaining H14 conjunctions/disjunctions 2. All tied minima remain visible. '
              'The marker requires multiple disagreeing compatible functions, a complete '
              'retained-effect match to a minimum, and an unsupported extension. It overlaps '
              'unsupported transfer and is never an additional independent error. Unresolved '
              'or rejected hypotheses do not become adopted effects.', '',
              '| Task type | C probe | Unsupported transfer | Missed warranted transfer | Observed contradiction | Assessed outputs / planned |',
              '| --- | --- | --- | --- | --- | ---: |']
    for kind in TASK_TYPES:
        for probe in PROBES:
            item = summary['by_task_type'][kind]['C'][probe]['transfer_directions']
            counts = ' | '.join(_direction_count(item['by_tag'][tag]) for tag in DIRECTION_TAGS)
            lines.append(f"| {kind} | {probe} | {counts} | {item['assessed']}/6 |")


def _material_tables(lines, result):
    lines += ['', '## Source-bound material counterfactual audit', '',
              f"Run source binding: `{result.get('source_sha256', 'not supplied')}`. "
              'The following history IDs bind the material audit to this result. These '
              'promotions assess material relevance, not observed model errors.', '',
              '| History | Setting / type | Record type | Records | Action flips | Contradictions | Unchanged | Narrower, same action | Retention resolved | Unassessable | Required outcome / passed |',
              '| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
    materials = result.get('material_audits')
    if materials is None:
        lines += ['| unavailable | | | | | | | | | | pending |']
    for material in materials or []:
        audit = material.get('counterfactual', {})
        for kind, item in audit.get('by_type', {}).items():
            n = item.get('record_count', 0)
            if not n:
                lines.append(f"| {_safe(material['history_id'])} | {material['setting']} / {material['task_type']} | "
                             f"{kind} (absent) | 0 | undefined | undefined | undefined | undefined | undefined | undefined | not applicable |")
                continue
            values = ' | '.join(_count(item.get(key)) for key in ('record_count', 'action_flip', 'contradiction',
                'unchanged_constraints', 'narrower_same_actions', 'retention_resolved', 'unassessable'))
            lines.append(f"| {_safe(material['history_id'])} | {material['setting']} / {material['task_type']} | "
                         f"{kind} | {values} | {audit.get('required_outcome')} / {audit.get('passed')} |")
    lines += ['', 'Exactly one publicly recoverable record configuration is promoted while '
              'preserving all genuine evidence. A nonempty compatible set with changed action '
              'is a flip; an empty set is a contradiction and has no action. Each present '
              'manipulated type requires a flip witness in unidentifiable histories and a '
              'contradiction witness in the other task types. Absent types have no success '
              'denominator. Detailed qualifying record IDs and promotions are preserved in '
              'the material audit and human-review export.', '']


def _conflict_tables(lines, summary):
    lines += ['', '## Apparent-conflict heuristic associations', '',
              'These secondary markers describe wrong behaviour compatible with a registered '
              'majority or latest-record heuristic. They do not establish that the model used '
              'the heuristic. Only transfer change, observed change and resolved retention '
              'with transfer are eligible; unidentifiable histories are excluded.', '',
              'Within each complete current context, each visible current target approval and '
              'each publicly recoverable manipulated-record promotion counts once. Copies '
              'count separately, retaining their origin IDs. Old approvals are projected to '
              'the current version; forwards use their destination and visible arrival time. '
              'Registrations and technical logs supply no target-configuration vote. Majority '
              'requires unequal counts. Recency uses the maximum visible timestamp, not list '
              'position or origin time; contradictory values tied at that timestamp remain '
              'undefined. Unusable target configurations make the predictions undefined.', '',
              'An association requires both configurations to be visible in the same context, '
              'a unanimous oracle value, a unique wrong heuristic prediction, and the same '
              'wrong executed or retained effect. Purely cross-context logical conflicts '
              'without two visible values in one cell are outside this conservative marker. '
              'Ties, missing effects and invalid retained guidance are not zero-error cases.', '',
              '| Task type | Stage | Known eligible contexts | Majority matches / assessed | Recency matches / assessed | Majority / recency ties | Overlap | Also compatible with baseline default, majority / recency |',
              '| --- | --- | ---: | --- | --- | --- | --- | --- |']
    for kind in TASK_TYPES:
        if kind == 'unidentifiable':
            continue
        for phase in ('C1', 'C2'):
            item = summary['conflict_by_task_type'][kind][phase]
            majority, recency = (item['methods'][method] for method in CONFLICT_METHODS)
            lines.append(f"| {kind} | {phase} | {_count(item['registered_eligible_contexts'])} | "
                f"{_count(majority['association_count'])}/{majority['assessed_contexts']} | "
                f"{_count(recency['association_count'])}/{recency['assessed_contexts']} | "
                f"{majority['tie_contexts']} / {recency['tie_contexts']} | "
                f"{_count(item['overlapping_association_contexts'])} | "
                f"{_count(majority['default_also_explains_count'])} / {_count(recency['default_also_explains_count'])} |")
    lines += ['', 'Each stage has six planned preparations per task type and four context cells '
              'per preparation. Eligible-context counts are narrower than those fixed totals; '
              'unknown counts stay undefined. The two markers may overlap each other and '
              'existing scope errors. They are never added as independent failures and do not '
              'change headroom or confirm content-error attribution. Retaining the baseline '
              'can also explain some matches without any majority or recency reasoning. '
              'Explicit model rationale and any actual human attribution review remain separate.', '',
              '| Task type | Arm | Probe | Known eligible contexts | Majority matches / assessed | Recency matches / assessed |',
              '| --- | --- | --- | ---: | --- | --- |']
    for kind in TASK_TYPES:
        if kind == 'unidentifiable':
            continue
        for arm in ('B', 'C'):
            for probe in PROBES:
                item = summary['by_task_type'][kind][arm][probe]['conflict_resolution']
                counts = ' | '.join(f"{_count(item['methods'][method]['association_count'])}/"
                                   f"{item['methods'][method]['assessed_contexts']}" for method in CONFLICT_METHODS)
                lines.append(f"| {kind} | {arm} | {probe} | {_count(item['registered_eligible_contexts'])} | {counts} |")


def write_report(path, result: dict, *, offline: bool | None = None) -> Path:
    """Write once; result may be aggregate itself or {aggregate, amortisation}.

    Run metadata can supply config.backend, rows and prep_rows. No report field
    can confer human material approval or permission for a live execution.
    """
    summary = result.get('aggregate', result)
    resources = result.get('amortisation')
    if offline is None:
        config = result.get('config', {})
        offline = (config.get('backend') == 'mock' or result.get('origin') in ('mock', 'offline_mock')
                   or result.get('offline') is True)
    label = ('OFFLINE MOCK — implementation check; no model efficacy evidence.' if offline
             else 'Exploratory synthetic difficulty map; review status must be read separately.')
    lines = ['# Pilot v0.4 difficulty map', '', label, '',
             'Outcomes concern completed structured fields and warranted updates. '
             'They do not measure professional quality or enterprise utility.', '',
             f"Fixed generation denominator: 144 (24 diagnostic and 24 control tasks per arm). "
             f"Observed rows: {summary['observed_generation_rows']}. "
             f"Complete registered design: {summary['design_valid']}.", '']
    if summary['design_errors']:
        lines.extend(['Design violations: ' + '; '.join(summary['design_errors']) + '.', ''])
    lines += ['## Outcomes', '',
              '| Setting | Arm | Probe | Warranted updates | Field world compliance | Completed |',
              '| --- | --- | --- | ---: | ---: | ---: |']
    for setting in SETTINGS:
        for arm in ARMS:
            for probe in PROBES:
                item = summary['by_setting'][setting][arm][probe]
                warrant = (f"not comparable ({item['update_correct']}/4 current-only)" if arm == 'A'
                           else f"{item['update_correct']}/4")
                lines.append(f"| {setting} | {arm} | {probe} | {warrant} | "
                             f"{item['world_compliant']}/4 | {item['completed_deliverable']}/4 |")
    lines += ['', 'Missing and blocked tasks retain their registered denominator. '
              'Controls are reported separately and do not enter the headroom flag. '
              'A has only current-task information: its warrant score checks baseline retention '
              'under that information and is not comparable to B/C history-based warrant. '
              'Field world compliance uses the same world obligations for all arms.', '',
              '| Setting | Arm | Diagnostic regime | Warranted updates | Field world compliance |',
              '| --- | --- | --- | ---: | ---: |']
    for setting in SETTINGS:
        for arm in ARMS:
            for regime, item in summary['by_setting'][setting][arm]['diagnostic']['by_regime'].items():
                warrant = (f"not comparable ({item['update_correct']}/{item['n']} current-only)" if arm == 'A'
                           else f"{item['update_correct']}/{item['n']}")
                lines.append(f"| {setting} | {arm} | {regime} | {warrant} | "
                             f"{item['world_compliant']}/{item['n']} |")
    lines += ['', '| Task type | Arm | Probe | Warranted updates | Field world compliance |',
              '| --- | --- | --- | --- | ---: |']
    for kind in TASK_TYPES:
        for arm in ARMS:
            for probe in PROBES:
                item = summary['by_task_type'][kind][arm][probe]
                warrant = (f"not comparable ({item['update_correct']}/6 current-only)" if arm == 'A'
                           else f"{item['update_correct']}/6")
                lines.append(f"| {kind} | {arm} | {probe} | {warrant} | {item['world_compliant']}/6 |")
    lines += ['',
              '## C diagnostic failure attribution and exploratory headroom', '',
              '| Setting | C correct | Content / technical / mixed / unresolved | Confirmed content lower bound | Content + mixed sensitivity | Headroom |',
              '| --- | ---: | --- | ---: | ---: | --- |']
    for setting in SETTINGS:
        item = summary['headroom'][setting]
        failures = item['failure_attribution']
        counts = failures['category_counts']
        categories = ' / '.join(str(counts[key]) for key in ('content', 'technical', 'mixed', 'unresolved'))
        flag = 'provisional' if item['qualifies'] is None else str(item['qualifies'])
        lines.append(f"| {setting} | {item['C_correct']}/4 | {categories} | "
                     f"{_percent(failures['confirmed_content_fraction_lower_bound'])} | "
                     f"{_percent(failures['mixed_inclusive_sensitivity'])} | {flag} |")
    lines += ['', 'The registered criterion is at most 2/4 C diagnostics correct and at least '
              '60% pure content errors among all diagnostic failures. Mixed and unresolved '
              'failures stay in the denominator. Provisional machine attribution is not '
              'independent human validation; only invariant conclusions across admissible '
              'attributions produce a definitive flag.', '',
              '| Setting | C control failures | Content / technical / mixed / unresolved | Provisional |',
              '| --- | ---: | --- | ---: |']
    for setting in SETTINGS:
        failures = summary['by_setting'][setting]['C']['control']['failures']
        counts = failures['category_counts']
        categories = ' / '.join(str(counts[key]) for key in ('content', 'technical', 'mixed', 'unresolved'))
        lines.append(f"| {setting} | {failures['failure_count']}/4 | {categories} | {failures['provisional_count']} |")
    lines += ['',
              '## Candidate content errors', '',
              'Each candidate is counted once even if it has several content errors. C1 and C2 '
              'remain separate. Correct downstream tasks do not erase preparation errors. '
              'These are finite-probe confirmed lower bounds; cited IDs alone do not establish '
              'semantic grounding. Exclusively non-authoritative support, support from a different '
              'workflow, or old-only support for current scope can establish an evidence-basis '
              'error even when the operational rule is correct. Copies inherit root authority; '
              'old historical scopes and counterevidence remain distinct. Other free-text '
              'provenance reasoning and ambiguous operator encodings still require review.', '',
              '| Setting | Stage | Present preparations | Content errors / candidates | Unassessable | Technical candidates | Mean defined history rate | Defined histories |',
              '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for setting in SETTINGS:
        for phase in ('C1', 'C2'):
            item = summary['candidate_analysis'][setting][phase]
            lines.append(f"| {setting} | {phase} | {item['present_preparations']}/4 | "
                         f"{item['content_error_count']}/{item['candidate_count']} | {item['unassessable_count']} | "
                         f"{item['technical_candidate_count']} | {_percent(item['mean_defined_history_rate'])} | "
                         f"{item['defined_history_rates']}/4 |")
    lines += ['', 'Missing, empty or wholly unassessable preparations have undefined history '
              'rates. Candidate numbers are model-controlled and dependent; pooled candidate '
              'fractions are not independent observations or substitutes for the history mean.', '',
              '| Setting | Stage | History | Errors / candidates | History rate | Unassessable |',
              '| --- | --- | --- | ---: | ---: | ---: |']
    for setting in SETTINGS:
        for phase in ('C1', 'C2'):
            for item in summary['candidate_analysis'][setting][phase]['histories']:
                lines.append(f"| {setting} | {phase} | {_safe(item['history_id'])} | "
                             f"{item['content_error_count']}/{item['candidate_count']} | "
                             f"{_percent(item['content_error_rate'])} | {item['unassessable_count']} |")
    _scope_tables(lines, summary)
    _conflict_tables(lines, summary)
    _material_tables(lines, result)
    lines += ['', '## All registered case outcomes', '',
              '| Setting | History | Task type | Arm | Probe / control basis | Call status | Warrant | World fields | Direction tags | Possible conflict associations | Cause / review status |',
              '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for item in summary.get('case_outcomes', []):
        attribution = item.get('error_attribution') or {}
        cause = attribution.get('category') or 'none'
        if attribution.get('provisional'):
            cause += ' (provisional)'
        if attribution.get('reviewer'):
            cause += ' (reviewed by ' + _safe(attribution['reviewer']) + ')'
        direction = item.get('transfer_analysis') or {}
        tags = ', '.join(direction.get('tags', [])) if direction.get('assessable') else 'undefined'
        conflict = item.get('conflict_resolution') or {}
        associated = sorted({method for cell in conflict.get('cells', []) for method in CONFLICT_METHODS
                             if cell['heuristics'][method].get('association') is True})
        conflict_label = (', '.join(associated) if associated else 'none' if any(
            cell['heuristics'][method].get('assessable') for cell in conflict.get('cells', [])
            for method in CONFLICT_METHODS) else 'undefined / not eligible')
        basis = f" / {item.get('control_basis')}" if item['probe'] == 'control' else ''
        lines.append(f"| {item['setting']} | {_safe(item['history_id'])} | {item['task_type']} | "
                     f"{item['arm']} | {item['probe']}{basis} | {item['call_status']} | {item['update_correct']} | "
                     f"{item['world_compliant']} | {tags or 'none'} | {conflict_label} | {cause} |")
    if resources is not None:
        lines += ['', '## Conditional token amortisation', '',
                  f"Actual calls: {resources['actual_calls']}. Reported input + output tokens: "
                  f"{resources['reported_total_tokens']}. Calls with unknown or invalid usage: "
                  f"{resources['unknown_or_invalid_usage_calls']}.", '',
                  '| Arm / phase | Calls | Failed | Input | Output | Cached input subset | Reasoning output subset |',
                  '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
        for key, item in resources['by_arm_phase'].items():
            lines.append(f"| {key} | {item['calls']} | {item['failed_calls']} | {item['input_tokens']} | "
                         f"{item['output_tokens']} | {item['cached_input_tokens']} | {item['reasoning_output_tokens']} |")
        lines += ['', '| History | Scenario | Prep tokens | B/task | C/task | First strictly cheaper N | Failed calls |',
                  '| --- | --- | ---: | ---: | ---: | ---: | ---: |']
        for history, item in resources['by_history'].items():
            for name, scenario in item['scenarios'].items():
                n = scenario.get('first_strictly_cheaper_N')
                display = str(n) if n is not None else 'no finite threshold' if scenario['available'] else 'unavailable'
                lines.append(f"| {_safe(history)} | {name} | {scenario.get('preparation_tokens', 'unknown')} | "
                             f"{scenario.get('B_mean_generation_tokens', 'unknown')} | "
                             f"{scenario.get('C_mean_generation_tokens', 'unknown')} | {display} | {item['failed_calls']} |")
        lines += ['', 'B(N)=N×b and C(N)=P+N×c; if b>c, the first strictly cheaper integer '
                  'is floor(P/(b−c))+1. Otherwise no finite threshold exists. Missing metering '
                  'does not become zero. Cached and reasoning tokens are subsets, not extra costs.', '',
                  'These scenarios assume stationary future tasks, reusable guidance and no '
                  'additional preparation, maintenance or growing-history cost. Two observed '
                  'future tasks per history cannot validate those assumptions. Scenarios are '
                  'not confidence intervals. Lower tokens with worse outcomes are not equivalent '
                  'efficiency. No monetary or latency claim is made.', '']
    lines += ['', '## Limits and prospective decision', '',
              'This is a synthetic finite policy class with supplied field alternatives and '
              'structured outputs, four diagnostic histories per setting, related templates '
              'and one registered model/reasoning configuration. These cases do not estimate '
              'population performance, establish causal effects of individual difficulty '
              'factors, or validate real workplace outcomes. Scope equivalence holds only over '
              'the registered probes. Sparse, dependent cases and model-controlled candidate '
              'counts preclude treating candidate rows as independent replications.', '',
              'H14 excludes XOR and XNOR. Identifying an unobserved cell from three observations '
              'depends on that publicly supplied exclusion. The current templates have 1, 3, '
              '1 and 4 compatible current functions respectively; the private slot allocation '
              'does not remove other publicly admissible hypotheses. Transfer counts are not '
              'evidence of unrestricted requirement discovery.', '',
              ('No v0.5 mechanism is selected from this offline run: mock results provide no '
               'efficacy evidence.' if offline else
               'A prospective v0.5 decision remains pending interpretation and refinement '
               'after the content-error audit. Witness-search or temporal-provenance approaches '
               'are hypotheses for a separate protocol with fresh cases; no mechanism is '
               'automatically recommended.'), '',
              '## Review and authorisation boundaries', '',
              'Consult the separate actual human material-review and live-approval records. '
              'This report grants neither approval. Automated attribution and offline checks '
              'do not replace independent semantic review. Historical v0.3 scores are unchanged.', '']
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x', encoding='utf-8') as stream:
        stream.write('\n'.join(lines))
    return destination
