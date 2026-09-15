"""Exploratory model pilot, with frozen inputs and no automatic answer repair.

Run stages separately: smoke, freeze, prepare, generate, judge, report.
Uses the user's existing Codex CLI authentication; never reads credentials.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import re
import sys

from grounded_reflection.codex_backend import run_completion
from grounded_reflection.models import CandidateUpdate, EvidenceBundle, Hypothesis, Scope
from grounded_reflection.workflow import assess_candidate, digest

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
MODEL = "gpt-6-astra"
EFFORT = "xhigh"
ARMS = ("direct_evidence", "direct_adaptation", "grounded_reflection")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    path = Path(path)
    if path.exists():
        raise ValueError(f"Refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def obj(properties):
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


def arr(items):
    return {"type": "array", "items": items}


S = {"type": "string"}
REF = obj({"episode_id": S, "evidence_id": S, "quote": S})
SCOPE = arr(obj({"attribute": S, "values": arr(S)}))
REFLECTION_SCHEMA = obj({
    "hypotheses": arr(obj({"hypothesis_id": S, "claim": S, "scope": SCOPE,
        "support": arr(REF), "counterevidence": arr(REF), "alternatives": arr(S), "unresolved_questions": arr(S)})),
    "candidates": arr(obj({"candidate_id": S, "hypothesis_id": S, "scope": SCOPE,
        "patch": S, "prediction": S, "blocking_questions": arr(S)})),
})
DIRECT_SCHEMA = obj({"guidance": S})
POST_SCHEMA = obj({"case_id": S, "post": S, "editorial_notes": arr(S)})
JUDGE_SCHEMA = obj({"case_id": S, "ratings": arr(obj({"output_id": S,
    "scores": arr(obj({"criterion_id": S, "score": {"type": "integer", "enum": [0, 1, 2]}, "reason": S})),
    "critical_errors": arr(S), "uncertainties": arr(S)}))})
INFERENCE_JUDGE_SCHEMA = obj({"assessments": arr(obj({"hypothesis_id": S,
    "support_relevance": {"type": "integer", "enum": [0, 1, 2]},
    "scope_justification": {"type": "integer", "enum": [0, 1, 2]},
    "uncertainty_handling": {"type": "integer", "enum": [0, 1, 2]}, "explanation": S})),
    "limitations": arr(S)})

COMMON = ("This is a bounded research task on wholly fictional work records. Use only the information in this "
          "prompt. Do not use tools, browse, inspect files, or ask the experiment operator questions. "
          "Return only the requested JSON. Provide concise evidence-based summaries, not private reasoning.\n")
PREP = ("Study these historical recruiting work episodes and prepare reusable guidance for future professional "
        "recruiting tasks. Current facts and explicit instructions in each future task take precedence. "
        "Do not invent missing approvals or explanations. No future task or evaluation rubric is available here.\n")
DIRECT_INSTRUCTIONS = ("Produce the best compact context guidance you can using any suitable approach. "
                       "The guidance will be supplied to a separate model producing new recruiting posts. "
                       "Keep the guidance to at most 350 words.\n")
REFLECTION_INSTRUCTIONS = (
    "Infer at most three requirement hypotheses and at most three concrete context-update candidates. "
    "Each hypothesis must identify exact supporting quotations by episode_id and evidence_id, relevant "
    "counterevidence, plausible alternatives, unresolved questions, and a bounded scope. "
    "Scope is a conjunction of attributes with allowed values drawn from observed context metadata. "
    "A candidate's scope must stay within its hypothesis scope. Each patch must be a usable context instruction, "
    "with an untested effect prediction. Put questions that prevent using a specific proposed patch in "
    "blocking_questions; general questions for future evaluation may remain unresolved without blocking it. "
    "You may return no hypothesis or candidate if the evidence is insufficient. Use no curated answers. "
    "All candidate patches combined must use at most 350 words.\n")
GENERATION_INSTRUCTIONS = (
    "You are preparing a professional recruiting deliverable for review. Produce the LinkedIn post requested "
    "in CURRENT TASK and up to three concise editorial notes. Follow the stated word range for the post; "
    "notes are separate. Use current approved sources for employment facts and application details. "
    "Historical material and guidance are fallible context; follow current explicit instructions in a conflict. "
    "Do not describe the experiment or condition.\n")
JUDGE_INSTRUCTIONS = (
    "Evaluate the anonymous recruiting outputs using the supplied prewritten rubric, current task sources "
    "and historical work evidence where relevant to context fit. Output labels carry no quality information. "
    "Do not infer which method produced an output. Score every criterion independently using the 0/1/2 anchors. "
    "Equivalent correct formulations are acceptable; do not reward verbosity or a preferred writing style "
    "without evidence. Historical preferences do not override the current brief. List substantive critical "
    "errors separately; minor stylistic preferences are not critical errors. State uncertainty when evidence "
    "does not support a definite judgment. The rubric is exploratory, not validated.\n")


def tasks():
    value = read(ROOT / "tasks.json")
    return value if isinstance(value, list) else value["tasks"]


def task_payload(task):
    value = read(ROOT / "tasks.json")
    return {**{k: v for k, v in task.items() if k != "case_type"},
            "shared_instructions": value.get("shared_instructions", "") if isinstance(value, dict) else ""}


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def frozen_paths():
    return [ROOT / "tasks.json", ROOT / "rubric.json", ROOT / "protocol.md", Path(__file__),
            REPO / "src/grounded_reflection/examples/hr_evidence.json",
            REPO / "src/grounded_reflection/codex_backend.py",
            REPO / "src/grounded_reflection/models.py", REPO / "src/grounded_reflection/workflow.py"]


def check_freeze():
    manifest = read(ROOT / "frozen_manifest.json")
    for name, expected in manifest["files"].items():
        if file_hash(REPO / name) != expected:
            raise ValueError(f"Frozen input changed: {name}; do not continue this run")
    return manifest


def load_development():
    # Intentionally exclude the fixture's curated hypotheses and candidates.
    episodes = read(REPO / "src/grounded_reflection/examples/hr_evidence.json")["episodes"]
    if any(ep["split"] != "development" for ep in episodes):
        raise ValueError("Non-development evidence encountered")
    return episodes


def complete(name, prompt, schema):
    return run_completion(COMMON + prompt, schema, ROOT / "runs" / name,
                          model=MODEL, reasoning_effort=EFFORT)["response"]


def run_jobs(jobs):
    failures = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(complete, *job): job[0] for job in jobs}
        for future in as_completed(futures):
            name = futures[future]
            try:
                future.result()
                print("Completed " + name, flush=True)
            except Exception as exc:
                failures.append({"run": name, "error": str(exc)})
                print("Failed " + name + ": " + str(exc), flush=True)
    if failures:
        raise RuntimeError(json.dumps(failures))


def result(name):
    metadata = read(ROOT / "runs" / name / "metadata.json")
    if metadata.get("status") != "completed":
        raise ValueError(f"Run not complete: {name}")
    return read(ROOT / "runs" / name / "final.json")


def decode_scope(entries):
    names = [entry["attribute"] for entry in entries]
    if len(set(names)) != len(names):
        raise ValueError("Duplicate scope attribute")
    return Scope(match={entry["attribute"]: entry["values"] for entry in entries})


def validate_reflection(raw):
    """Validate actual model output; never fill in missing semantic answers."""
    try:
        hypotheses = [Hypothesis(**{**h, "scope": decode_scope(h["scope"]), "origin": "model_generated"})
                      for h in raw["hypotheses"]]
        candidates = [CandidateUpdate(candidate_id=c["candidate_id"], hypothesis_id=c["hypothesis_id"],
            scope=decode_scope(c["scope"]), target="context", patch=c["patch"],
            expected_effect={"metric": "professional_quality", "prediction": c["prediction"]},
            blocking_questions=c["blocking_questions"]) for c in raw["candidates"]]
        if len(hypotheses) > 3 or len(candidates) > 3:
            raise ValueError("Preparation exceeded the declared candidate/hypothesis count")
        if not hypotheses or not candidates:
            return {"status": "abstained", "bundle": None, "assessments": [], "error": None}
        bundle = EvidenceBundle(episodes=load_development(), hypotheses=hypotheses, candidates=candidates)
        assessments = [assess_candidate(c, bundle).model_dump(mode="json") for c in candidates]
        return {"status": "parsed", "bundle": bundle.model_dump(mode="json"),
                "assessments": assessments, "error": None}
    except (ValueError, KeyError, TypeError) as exc:
        return {"status": "invalid", "bundle": None, "assessments": [], "error": str(exc)}


def condition_context(arm, task):
    if arm == "direct_evidence":
        return {"historical_work_episodes": load_development()}
    if arm == "direct_adaptation":
        return {"historical_guidance": result("prepare_direct")["guidance"]}
    checked = read(ROOT / "reflection_check.json")
    if checked["bundle"] is None:
        return {"historical_guidance": []}
    bundle = EvidenceBundle.model_validate(checked["bundle"])
    eligible = {a["candidate_id"] for a in checked["assessments"] if a["status"] == "eligible_for_validation"}
    return {"historical_guidance": [c.patch for c in bundle.candidates
            if c.candidate_id in eligible and c.scope.applies_to(task["context"]) == "match"]}


def freeze():
    case_list = tasks()
    if len(case_list) != 6 or len({c["case_id"] for c in case_list}) != 6:
        raise ValueError("Exactly six unique evaluation cases are required")
    if {e["episode_id"] for e in load_development()} & {c["case_id"] for c in case_list}:
        raise ValueError("Evaluation IDs overlap development")
    rubric = read(ROOT / "rubric.json")
    if {c["case_id"] for c in rubric["cases"]} != {c["case_id"] for c in case_list}:
        raise ValueError("Rubric cases do not match tasks")
    write(ROOT / "frozen_manifest.json", {
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(), "protocol": "hr-pilot-v0.1",
        "requested_model": MODEL, "reasoning_effort": EFFORT, "conditions": ARMS,
        "case_ids": [c["case_id"] for c in case_list], "repetitions": 1,
        "preparation_calls": 2, "generation_calls": 18, "paired_judge_calls": 6,
        "inference_audit_calls": 1, "blind_order_seed": 20260915,
        "files": {str(p.relative_to(REPO)).replace("\\", "/"): file_hash(p) for p in frozen_paths()},
        "restriction": "No experimental output available at freeze; no prompt or task tuning within this run."})


def prepare():
    history = "\nHISTORICAL EPISODES\n" + json.dumps(load_development(), ensure_ascii=False)
    run_jobs([("prepare_direct", PREP + DIRECT_INSTRUCTIONS + history, DIRECT_SCHEMA),
              ("prepare_reflection", PREP + REFLECTION_INSTRUCTIONS + history, REFLECTION_SCHEMA)])
    write(ROOT / "reflection_check.json", validate_reflection(result("prepare_reflection")))


def generate():
    jobs = []
    order = [(arm, task) for task in tasks() for arm in ARMS]
    random.Random(20260915).shuffle(order)
    write(ROOT / "generation_order.json", [{"arm": a, "case_id": t["case_id"]} for a, t in order])
    for arm, task in order:
        prompt = GENERATION_INSTRUCTIONS + "\nHISTORICAL CONTEXT\n" + json.dumps(condition_context(arm, task), ensure_ascii=False)
        prompt += "\nCURRENT TASK\n" + json.dumps(task_payload(task), ensure_ascii=False)
        jobs.append((f"generate_{task['case_id']}_{arm}", prompt, POST_SCHEMA))
    run_jobs(jobs)


def judge():
    rubric = read(ROOT / "rubric.json")
    mapping = {}
    jobs = []
    rng = random.Random(20260915)
    for task in tasks():
        case_id = task["case_id"]
        order = list(ARMS)
        rng.shuffle(order)
        mapping[case_id] = {f"output-{i+1}": arm for i, arm in enumerate(order)}
        anonymous = []
        for label, arm in mapping[case_id].items():
            output = result(f"generate_{case_id}_{arm}")
            if output["case_id"] != case_id:
                raise ValueError("Model returned the wrong case ID")
            anonymous.append({"output_id": label, "post": output["post"], "editorial_notes": output["editorial_notes"]})
        payload = {"task": task_payload(task), "historical_evidence": load_development(), "criteria": rubric["criteria"],
                   "scoring_instructions": rubric.get("scoring", {}),
                   "case_rubric": next(c for c in rubric["cases"] if c["case_id"] == case_id), "outputs": anonymous}
        jobs.append(("judge_" + case_id, JUDGE_INSTRUCTIONS + json.dumps(payload, ensure_ascii=False), JUDGE_SCHEMA))
    write(ROOT / "blind_mapping.json", mapping)
    audit = ("Assess these machine-generated requirement hypotheses against their source episodes. "
             "Score each hypothesis 0=unsupported/problematic, 1=partial/uncertain, 2=well supported on "
             "support relevance, scope justification and uncertainty handling. Exact quotes alone do not "
             "prove a claim. This is a model assessment, not a domain-expert validation.\n")
    jobs.append(("judge_inference", audit + json.dumps({"episodes": load_development(),
                 "generated": result("prepare_reflection")}, ensure_ascii=False), INFERENCE_JUDGE_SCHEMA))
    run_jobs(jobs)


def report():
    mapping = read(ROOT / "blind_mapping.json")
    rubric = read(ROOT / "rubric.json")
    criteria = {c["id"] for c in rubric["criteria"]}
    rows = []
    for task in tasks():
        case_id = task["case_id"]
        ratings = result("judge_" + case_id)
        if ratings["case_id"] != case_id or len(ratings["ratings"]) != 3:
            raise ValueError("Invalid judge case/count")
        if {r["output_id"] for r in ratings["ratings"]} != set(mapping[case_id]):
            raise ValueError("Missing or duplicate anonymous rating labels")
        for rating in ratings["ratings"]:
            if len(rating["scores"]) != len(criteria) or {s["criterion_id"] for s in rating["scores"]} != criteria:
                raise ValueError("Judge criteria differ from frozen rubric")
            arm = mapping[case_id][rating["output_id"]]
            output = result(f"generate_{case_id}_{arm}")
            count = len(re.findall(r"\S+", output["post"]))
            bounds = task["output_constraints"]
            rows.append({"case_id": case_id, "case_type": task["case_type"], "arm": arm,
                         "total": sum(s["score"] for s in rating["scores"]),
                         "scores": rating["scores"], "critical_errors": rating["critical_errors"],
                         "word_count": count, "word_range_met": bounds["min_words"] <= count <= bounds["max_words"],
                         "uncertainties": rating["uncertainties"]})
    totals = {arm: {"mean_score": sum(r["total"] for r in rows if r["arm"] == arm) / 6,
                    "cases_with_critical_errors": sum(bool(r["critical_errors"]) for r in rows if r["arm"] == arm),
                    "word_range_passes": sum(r["word_range_met"] for r in rows if r["arm"] == arm)} for arm in ARMS}
    paired_differences = []
    for task in tasks():
        scores = {r["arm"]: r["total"] for r in rows if r["case_id"] == task["case_id"]}
        paired_differences.append({"case_id": task["case_id"],
            "reflection_minus_direct_evidence": scores["grounded_reflection"] - scores["direct_evidence"],
            "reflection_minus_direct_adaptation": scores["grounded_reflection"] - scores["direct_adaptation"]})
    direct_words = len(re.findall(r"\S+", result("prepare_direct")["guidance"]))
    reflection_words = sum(len(re.findall(r"\S+", c["patch"])) for c in result("prepare_reflection")["candidates"])
    guidance = {"direct_adaptation": {"words": direct_words, "requested_limit_met": direct_words <= 350},
                "grounded_reflection": {"words": reflection_words, "requested_limit_met": reflection_words <= 350}}
    usage = {}
    for p in sorted((ROOT / "runs").glob("*/metadata.json")):
        if p.parent.name == "smoke":
            continue
        meta = read(p)
        usage[p.parent.name] = {k: meta.get(k) for k in ("status", "wall_seconds", "usage", "requested_model", "reasoning_effort", "tool_use_detected")}
    write(ROOT / "results.json", {"model_ratings_only": True, "n_cases": 6, "repetitions": 1,
        "rows": rows, "summary": totals, "paired_differences": paired_differences,
        "guidance_word_counts": guidance, "runs": usage, "reflection_check": read(ROOT / "reflection_check.json"),
        "inference_audit": result("judge_inference"),
        "human_revision_time": None, "exported_or_deployed_update": False,
        "conclusion_boundary": "Exploratory synthetic model pilot. No significance, human validity, real-world effect or recursive improvement claim."})
    print(json.dumps(totals, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["smoke", "freeze", "prepare", "generate", "judge", "report"])
    args = parser.parse_args()
    if args.stage == "smoke":
        complete("smoke", "Return status='ok' and the sum of 12 and 19 as result. No tools.",
                 obj({"status": S, "result": {"type": "integer"}}))
    elif args.stage == "freeze":
        freeze()
    else:
        check_freeze()
        globals()[args.stage]()


if __name__ == "__main__":
    main()
