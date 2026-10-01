"""Synthetic work histories and split-specific tasks; no model or network access.

World rules are constant across seeds. Seeds change case facts, never the policy
that a prepared adaptation has to transfer. Final tasks are generated only when
the caller explicitly requests ``final_test`` after the experiment freeze.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from ..models import EvidenceItem, Provenance, Scope, WorkEpisode
from .contracts import FamilyTruth, History, Rule, Task, TaskTruth


DEFAULT_SEED = 20260928
FIELDS = ["emphasis", "route", "source_id", "summary"]
WORLDS = {
    "recruiting": {
        "channel": "vacancy_brief", "audiences": ("specialists", "career_starters"),
        "emphases": ("work_ownership", "supported_learning"),
        "route": "role_page", "outside_channel": "staffing_review",
        "outside_emphasis": "capacity_planning", "outside_route": "planning_queue",
        "subject": "research software vacancy", "detail": "documenting reproducible experiments",
        "preference": "community_story", "technical_route": "email_attachment",
    },
    "sales": {
        "channel": "account_handover", "audiences": ("discovery_team", "proposal_team"),
        "emphases": ("unresolved_needs", "agreed_next_steps"),
        "route": "account_workspace", "outside_channel": "territory_review",
        "outside_emphasis": "portfolio_coverage", "outside_route": "territory_board",
        "subject": "measurement software opportunity", "detail": "checking the customer's workflow needs",
        "preference": "product_story", "technical_route": "local_spreadsheet",
    },
    "research": {
        "channel": "study_note", "audiences": ("exploratory_review", "replication_review"),
        "emphases": ("limitations", "reproducibility"),
        "route": "versioned_notebook", "outside_channel": "portfolio_summary",
        "outside_emphasis": "programme_milestones", "outside_route": "programme_board",
        "subject": "synthetic assay study", "detail": "comparing simulated measurement runs",
        "preference": "novelty_story", "technical_route": "unversioned_export",
    },
}

REVIEW_NOTES = {
    "recruiting": {
        "corrections": (
            "An experienced applicant cannot yet see what they would own. Bring the concrete responsibility into the opening.",
            "The introduction reads like a training offer. Show the work the new colleague would be responsible for and why it matters.",
            "The draft sounds as though the new starter must take charge immediately. Explain the mentoring and supported first activities.",
            "The support arrangements are buried. Someone entering this work should be able to picture how they will learn it.",
        ),
        "outside_source": "The next quarterly planning meeting needs a view of staffing capacity and pending allocations.",
        "outside_review": "This gives the planning group what it needs for the allocation discussion. Approved.",
        "local_review": "Mira, editor: For tomorrow's project showcase, start with the story of how the team came together.",
    },
    "sales": {
        "corrections": (
            "The handover jumps to next steps before we know the customer's constraints. Make the unanswered questions visible.",
            "The receiving colleague still cannot tell which needs have been established and which they must investigate.",
            "The needs review is complete. The receiving colleague needs the actions agreed with the customer, including who owns each one.",
            "Another needs summary will not help the proposal team move this forward. Bring the agreed follow-up commitments to the front.",
        ),
        "outside_source": "The territory planning meeting needs an overview of account coverage and gaps across the portfolio.",
        "outside_review": "The coverage view is ready for the allocation meeting. Approved.",
        "local_review": "Mira, editor: For tomorrow's product showcase, start with the story of how this product developed.",
    },
    "research": {
        "corrections": (
            "These are early simulated runs. The reader needs to see what the sample and assumptions do not let us conclude.",
            "The procedural detail is useful, but it hides the limits of this exploratory result. Bring those into the opening.",
            "The replication group needs to repeat the analysis. Put the run configuration and the path to reproducing it first.",
            "This review is about recreating an already reported analysis. The reader should be able to locate the settings and sequence of steps.",
        ),
        "outside_source": "The programme committee needs an overview of milestones completed and work remaining across studies.",
        "outside_review": "The milestone view is ready for the programme meeting. Approved.",
        "local_review": "Mira, editor: For tomorrow's research showcase, lead with how the idea emerged and what makes it novel.",
    },
}


def _token(seed: int, *parts: str) -> str:
    material = json.dumps([seed, *parts], separators=(",", ":"))
    return hashlib.sha256(material.encode()).hexdigest()[:12]


def _context(family: str, audience: int = 0, *, outside: bool = False) -> dict[str, str]:
    world = WORLDS[family]
    return {
        "family": family,
        "role": family,
        "occasion": "routine",
        "channel": world["outside_channel"] if outside else world["channel"],
        "audience": world["audiences"][audience],
    }


def _scope(family: str, audience: int | None = None) -> Scope:
    match = {"role": [family], "channel": [WORLDS[family]["channel"]]}
    if audience is not None:
        match["audience"] = [WORLDS[family]["audiences"][audience]]
    return Scope(match=match)


def generate_family_truth(seed: int = DEFAULT_SEED) -> list[FamilyTruth]:
    """Return evaluator-only rules, invariant to the instance-generation seed."""
    del seed
    result = []
    for family, world in WORLDS.items():
        recoverable = [
            Rule(field="emphasis", value=value, scope=_scope(family, index))
            for index, value in enumerate(world["emphases"])
        ]
        recoverable.append(Rule(field="route", value=world["route"], scope=_scope(family)))
        unidentifiable = [
            Rule(field="closing_style", value=value, scope=_scope(family))
            for value in ("invitation", "statement")
        ]
        distractors = [
            Rule(field="emphasis", value=world["preference"], scope=_scope(family)),
            Rule(field="emphasis", value=world["outside_emphasis"], scope=_scope(family)),
            Rule(field="route", value=world["technical_route"], scope=_scope(family)),
        ]
        outside_scope = Scope(match={"role": [family], "channel": [world["outside_channel"]]})
        showcase_scope = Scope(match={
            "role": [family], "channel": [world["channel"]],
            "audience": [world["audiences"][0]], "occasion": ["showcase"],
        })
        supported_exceptions = [
            Rule(field="emphasis", value=world["outside_emphasis"], scope=outside_scope),
            Rule(field="route", value=world["outside_route"], scope=outside_scope),
            Rule(field="emphasis", value=world["preference"], scope=showcase_scope),
        ]
        unknown = _context(family)
        unknown.pop("audience")
        result.append(FamilyTruth(
            family=family, recoverable=recoverable, unidentifiable=unidentifiable,
            distractors=distractors, supported_exceptions=supported_exceptions,
            scope_probes=[_context(family, 0), _context(family, 1),
                          _context(family, 0, outside=True),
                          _context(family, 1, outside=True), unknown],
        ))
    return result


def _episode(family: str, seed: int, index: int, context: dict[str, str],
             task: str, records: list[tuple[str, str]],
             missingness: list[str] | None = None) -> WorkEpisode:
    token = _token(seed, family, "history", str(index))
    case = f"work-{token}"
    evidence = []
    for position, (kind, text) in enumerate(records):
        evidence.append(EvidenceItem(
            evidence_id=f"record-{position + 1}", kind=kind, text=text,
            provenance=Provenance(
                origin="synthetic", source_id=f"document-{token}-{position + 1}",
                recorded_at=datetime(2031, 3, index + 1, 9, position, tzinfo=timezone.utc),
            ),
        ))
    return WorkEpisode(
        episode_id=case, split="development", context=context,
        task=f"{task} Work order {token}.", evidence=evidence,
        missingness=missingness or [],
    )


def generate_histories(seed: int = DEFAULT_SEED) -> list[History]:
    """Eight episodes per family with observed decisions and situated reviews."""
    histories = []
    for family, world in WORLDS.items():
        notes = REVIEW_NOTES[family]
        episodes = []
        for index in range(4):
            audience = index // 2
            emphasis = world["emphases"][audience]
            other = world["emphases"][1 - audience]
            subject = f"{world['subject']} {str(index + 1)}-{_token(seed, family, str(index))[:5]}"
            records = [
                ("source", f"Current work concerns {subject}, {world['detail']}. "
                 f"The intended audience is {world['audiences'][audience]}."),
                ("agent_output", f"Decision record: emphasis={other}; route={world['route']}."),
                ("human_feedback", notes["corrections"][index]),
                ("human_revision", f"Accepted decision record: emphasis={emphasis}; "
                 f"route={world['route']}. The underlying facts about {subject} remain unchanged."),
            ]
            episodes.append(_episode(family, seed, index, _context(family, audience),
                                     f"Prepare a decision record about {subject}.", records))

        for audience in (0, 1):
            episodes.append(_episode(family, seed, 4 + audience,
                _context(family, audience, outside=True),
                "Prepare the record for the forthcoming planning meeting.", [
                    ("source", notes["outside_source"]),
                    ("agent_output", f"emphasis={world['outside_emphasis']}; route={world['outside_route']}."),
                    ("human_feedback", notes["outside_review"]),
                    ("human_revision", f"Accepted decision record: emphasis={world['outside_emphasis']}; "
                     f"route={world['outside_route']}."),
                ]))
        episodes.append(_episode(family, seed, 6, {**_context(family), "occasion": "showcase"},
            "Prepare a version of the existing record for tomorrow's showcase.", [
                ("source", "Commission: one presentation record for the project showcase. "
                 "Editorial review batch 41 lists Mira, Ari and Bo, each with role=editor."),
                ("agent_output", f"emphasis={world['emphases'][0]}; route={world['route']}."),
                ("human_feedback", notes["local_review"]),
                ("human_revision", f"Accepted opening and destination for showcase copy: "
                 f"emphasis={world['preference']}; route={world['route']}."),
                ("human_feedback", "Ari, editor, batch 41: End by inviting the reader to discuss the work with us."),
                ("agent_output", "Closing draft A, batch 41: closing_style=invitation."),
                ("human_feedback", "Bo, editor, batch 41: End with a concise statement of what the work contributes."),
                ("agent_output", "Closing draft B, batch 41: closing_style=statement."),
            ], ["Release receipt is absent from the extracted records."]))
        episodes.append(_episode(family, seed, 7, _context(family),
            f"Save an accepted {world['channel']} record.", [
                ("agent_output", f"emphasis={world['emphases'][0]}; route={world['route']}."),
                ("tool_result", f"save attempt=1 route={world['route']} status=503; "
                 f"client fallback option: route={world['technical_route']}."),
                ("tool_result", f"save attempt=2 route={world['route']} status=200; stored=true."),
            ]))
        histories.append(History(family=family, episodes=episodes))
    return histories


def _task(family: str, split: str, seed: int, index: int, category: str,
          audience: int = 0) -> tuple[Task, TaskTruth]:
    world = WORLDS[family]
    token = _token(seed, family, split, str(index))
    context = _context(family, audience, outside=category == "boundary")
    subject = f"{world['subject']} K{token[:6]}"
    source_id = f"source-{token}"
    facts = {
        "source_id": source_id,
        "subject": subject,
        "work_detail": world["detail"],
        "source_note": f"Current source document {source_id} describes {subject}.",
    }
    request = (
        "Produce a compact work decision record. Copy the current source_id into its field "
        "and include the complete subject name in a factual summary. Choose emphasis and "
        "route for the supplied context, using prior workflow records when available. "
        "If a required decision cannot be supported, identify the missing context instead of guessing. "
        "Use undetermined or omit a field that cannot yet be settled. "
        "You may retain independently supported fields when asking or deferring."
    )
    checks = [Rule(field="source_id", value=source_id),
              Rule(field="summary", operator="contains", value=subject)]
    kinds = ["explicit", "generic"]
    missing_fields = []
    allowed_actions = ["deliver"]
    if category == "boundary":
        request += (f" For this internal record, use emphasis={world['outside_emphasis']} "
                    f"and route={world['outside_route']} as specified by its current owner.")
        checks += [Rule(field="emphasis", value=world["outside_emphasis"]),
                   Rule(field="route", value=world["outside_route"])]
        kinds += ["explicit", "explicit"]
    elif category == "override":
        emphasis = "collaborative_review"
        request += (f" The owner specifies emphasis={emphasis} for this record only. "
                    "This current instruction takes precedence over previous examples; the usual route remains in force.")
        checks += [Rule(field="emphasis", value=emphasis), Rule(field="route", value=world["route"])]
        kinds += ["explicit", "hidden"]
    elif category == "ambiguous":
        context.pop("audience")
        facts["source_note"] += " The routing sheet does not name the receiving audience."
        checks += [Rule(field="route", value=world["route"]),
                   Rule(field="emphasis", value="undetermined")]
        kinds += ["hidden", "generic"]
        missing_fields = ["audience"]
        allowed_actions = ["clarify", "defer"]
    else:
        checks += [Rule(field="emphasis", value=world["emphases"][audience]),
                   Rule(field="route", value=world["route"])]
        kinds += ["hidden", "hidden"]
    distractors = [
        Rule(field="emphasis", value=world["preference"]),
        Rule(field="route", value=world["technical_route"]),
    ]
    if category != "boundary":
        distractors.append(Rule(field="emphasis", value=world["outside_emphasis"]))
    else:
        distractors.extend([Rule(field="emphasis", value=world["emphases"][0]),
                            Rule(field="route", value=world["route"])])
    task = Task(case_id=f"case-{token}", family=family, split=split, context=context,
                request=request, facts=facts, output_fields=list(FIELDS))
    truth = TaskTruth(case_id=task.case_id, family=family, category=category,
                      checks=checks, check_kinds=kinds, allowed_actions=allowed_actions,
                      missing_fields=missing_fields, distractors=distractors,
                      unresolved_output_fields=["emphasis"] if category == "ambiguous" else [])
    return task, truth


def generate_tasks(split: str, seed: int = DEFAULT_SEED) -> tuple[list[Task], list[TaskTruth]]:
    """Generate only the requested split. Call final_test only after freeze."""
    layouts = {
        "calibration": [("transfer", 0), ("boundary", 1)],
        "validation": [("boundary", 0), ("ambiguous", 0)],
        "final_test": [("transfer", 0), ("boundary", 1), ("override", 0), ("ambiguous", 0)],
    }
    if split not in layouts:
        raise ValueError(f"unknown pilot split: {split}")
    tasks, truths = [], []
    for family in WORLDS:
        for index, (category, audience) in enumerate(layouts[split]):
            task, truth = _task(family, split, seed, index, category, audience)
            tasks.append(task)
            truths.append(truth)
    return tasks, truths


def task_content_fingerprint(task: Task) -> str:
    """Detect a copied case even when its case_id or split label was changed."""
    payload = task.model_dump(exclude={"case_id", "split"})
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def write_development(root: str | Path, seed: int = DEFAULT_SEED) -> dict[str, Path]:
    """Write development files beneath a data directory, refusing to replace files."""
    root = Path(root)
    calibration, calibration_truth = generate_tasks("calibration", seed)
    validation, validation_truth = generate_tasks("validation", seed)
    material = {
        "histories.json": generate_histories(seed),
        "calibration.json": calibration,
        "validation.json": validation,
        "ground_truth/families.json": generate_family_truth(seed),
        "ground_truth/calibration.json": calibration_truth,
        "ground_truth/validation.json": validation_truth,
    }
    paths = {name: root / name for name in material}
    if any(path.exists() for path in paths.values()):
        raise FileExistsError("development output already exists; choose a new directory")
    for name, records in material.items():
        path = paths[name]
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump([record.model_dump(mode="json") for record in records], handle, indent=2)
            handle.write("\n")
    return paths
