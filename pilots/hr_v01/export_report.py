"""Render descriptive pilot results and complete outputs without raw runtime logs."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
LABEL = {"direct_evidence": "Direct evidence", "direct_adaptation": "Direct adaptation", "grounded_reflection": "Grounded reflection"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def result(name):
    return read(ROOT / "runs" / name / "final.json")


def save(path, content):
    if path.exists():
        raise ValueError(f"Refusing to overwrite {path}")
    path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "rendered",
                        help="New directory for the report, posts and review sheet")
    output = parser.parse_args().output.resolve()
    if output.exists():
        raise SystemExit("Output directory already exists; nothing was changed")
    data = read(ROOT / "results.json")
    manifest = read(ROOT / "frozen_manifest.json")
    task_data = read(ROOT / "tasks.json")
    tasks = task_data["tasks"]
    if (ROOT / "observed_outputs.json").exists():
        clean = read(ROOT / "observed_outputs.json")
    else:
        clean = {"preparations": {"direct_adaptation": result("prepare_direct"),
                                  "grounded_reflection": result("prepare_reflection")},
                 "outputs": [{"case_id": t["case_id"], "condition": arm,
                               "response": result(f"generate_{t['case_id']}_{arm}")}
                              for t in tasks for arm in LABEL],
                 "judgments": {t["case_id"]: result("judge_" + t["case_id"]) for t in tasks},
                 "blind_mapping": read(ROOT / "blind_mapping.json"),
                 "inference_audit": result("judge_inference")}
    responses = {(item["case_id"], item["condition"]): item["response"] for item in clean["outputs"]}
    output.mkdir(parents=True)
    save(output / "observed_outputs.json", json.dumps(clean, indent=2, ensure_ascii=False) + "\n")

    def save_markdown(name, content):
        def rebase(match):
            target = match.group(1)
            if target in {"OUTPUTS.md", "observed_outputs.json"}:
                return match.group(0)
            relative = os.path.relpath(ROOT / target, output).replace(os.sep, "/")
            return f"](<{relative}>)"
        save(output / name, re.sub(r"\]\(([^)]+)\)", rebase, content))
    usage = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "reasoning_output_tokens": 0}
    for meta in data["runs"].values():
        for key in usage:
            usage[key] += (meta.get("usage") or {}).get(key, 0)
    lines = ["# HR pilot v0.1 — observed model results", "",
        "**All three conditions received 10/10 model ratings on all six tasks: a complete rating ceiling, with no observed advantage for structured reflection.** These exploratory results use synthetic tasks and actual model responses. No human evaluation or recursive improvement was measured.", "",
        f"Inputs were frozen at `{manifest['frozen_at_utc']}`. Requested model: `{manifest['requested_model']}`; reasoning setting: `{manifest['reasoning_effort']}`. Six cases, three conditions, one generation per case/condition, two preparation calls, six blinded comparison calls and one inference audit. A separate transport smoke test is excluded.", "",
        "## Descriptive comparison", "",
        "The total is the sum of five ordinal 0–2 rubric judgments. Means describe this small run; no statistical significance or population effect is inferred.", "",
        "| Condition | Mean model score / 10 | Cases with model-flagged critical errors | Posts within 110–150 words |",
        "| --- | ---: | ---: | ---: |"]
    for arm, label in LABEL.items():
        item = data["summary"][arm]
        lines.append(f"| {label} | {item['mean_score']:.2f} | {item['cases_with_critical_errors']}/6 | {item['word_range_passes']}/6 |")
    lines += ["", "| Case | Type | Direct evidence | Direct adaptation | Grounded reflection | Reflection − evidence | Reflection − adaptation |",
              "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for task in tasks:
        scores = {r["arm"]: r["total"] for r in data["rows"] if r["case_id"] == task["case_id"]}
        delta = next(d for d in data["paired_differences"] if d["case_id"] == task["case_id"])
        lines.append(f"| {task['case_id']} | {task['case_type']} | {scores['direct_evidence']} | {scores['direct_adaptation']} | {scores['grounded_reflection']} | {delta['reflection_minus_direct_evidence']:+d} | {delta['reflection_minus_direct_adaptation']:+d} |")
    lines += ["", "## Actual inference and protocol checks", ""]
    reflection = clean["preparations"]["grounded_reflection"]
    lines.append(f"The model generated {len(reflection['hypotheses'])} hypotheses and {len(reflection['candidates'])} candidate updates. Formal parsing status: `{data['reflection_check']['status']}`.")
    for hypothesis in reflection["hypotheses"]:
        lines += ["", f"**{hypothesis['hypothesis_id']}:** {hypothesis['claim']}"]
    lines += ["", "| Candidate | Formal status | Resolved supporting/counterevidence references |", "| --- | --- | ---: |"]
    for item in data["reflection_check"]["assessments"]:
        lines.append(f"| {item['candidate_id']} | {item['status']} | {item['verified_reference_count']} |")
    lines += ["", "These checks establish that quotes exist and declared scopes are contained. Semantic validity is separate. The same-model inference audit is available in `results.json`; it does not replace practitioner assessment.", "",
        "The direct-adaptation response also identifies audience-specific openings, current-source precedence and the uncertainty of unexplained shortening. Consequently, successful inference alone does not establish that the structured method adds useful information.", "",
        "The recorded reviews and missingness annotations explicitly indicate several relevant distinctions. This demonstrates synthesis of annotated work episodes, with limited evidence about discovering implicit requirements in raw logs. All three generated candidates have empty blocking-question lists: the model chose conservative guidance, and no clarification intervention was performed.", "",
        "## Recorded resources", "",
        "Direct adaptation and grounded reflection used the same model/settings and number of preparation/generation calls. The measured token consumption differs; this is not an exact compute-matched comparison.", "",
        "| Condition | Generation + preparation calls | Reported input tokens | Reported output tokens | Sum of call durations (s) |",
        "| --- | ---: | ---: | ---: | ---: |"]
    for arm, label in LABEL.items():
        names = [name for name in data["runs"] if name.startswith("generate_") and name.endswith("_" + arm)]
        if arm != "direct_evidence":
            names.append("prepare_direct" if arm == "direct_adaptation" else "prepare_reflection")
        values = [data["runs"][name] for name in names]
        lines.append(f"| {label} | {len(names)} | {sum((v.get('usage') or {}).get('input_tokens', 0) for v in values)} | {sum((v.get('usage') or {}).get('output_tokens', 0) for v in values)} | {sum(v.get('wall_seconds') or 0 for v in values):.1f} |")
    lines += ["", f"Across all 27 experimental calls, CLI-reported input tokens: {usage['input_tokens']}; output tokens: {usage['output_tokens']}; cached input tokens (reported separately): {usage['cached_input_tokens']}; reasoning output tokens (reported separately): {usage['reasoning_output_tokens']}. Counts include the CLI's context overhead. Duration sums include concurrent calls and are not elapsed experiment time. No monetary cost is inferred.", "",
              "| Preparation | Guidance words | Requested ≤350-word limit met |", "| --- | ---: | --- |"]
    for arm, count in data["guidance_word_counts"].items():
        lines.append(f"| {LABEL[arm]} | {count['words']} | {count['requested_limit_met']} |")
    lines += ["", "## Interpretation and limits", "",
        "This run demonstrates machine-generated structured hypotheses, executable reference/scope checks and a complete experimental path to new task outputs and blinded model assessment. It does not demonstrate employee-validated requirements, expert-level work quality, large-scale inference or repeated self-improvement.", "",
        "Before execution, the protocol recorded that task briefs already expose much of the required information. The observed rating ceiling therefore leaves the value of learning implicit requirements unresolved. Six purposeful synthetic cases, one sample each, a coarse rubric and a judge from the same model family constrain interpretation. The structured condition combines prompting and deterministic scope filtering; no ablation isolates their contributions.", "",
        "No human revision time was measured. No paired validation record was fabricated to satisfy the library's update-selection gate, and no update was exported or deployed. Next research steps require independently calibrated professional tasks, human judgments and comparisons with repetitions and explicitly matched resources.", "",
        "## Inspect and reproduce", "",
        "- [Frozen protocol](protocol.md) and [file hashes](frozen_manifest.json)",
        "- [Task materials](tasks.json) and [rubric](rubric.json)",
        "- [Complete preparations, outputs and anonymous judgments](observed_outputs.json)",
        "- [All posts side by side](OUTPUTS.md)",
        "- [Machine-readable analysis](results.json)",
        "- [Runner](run_pilot.py) and [clean-replay preparation](prepare_replay.py)", "",
        "To prepare a separate repeat without overwriting the observed run, invoke `python pilots/hr_v01/prepare_replay.py ../grounded-reflection-replay` from the repository. Follow the printed commands using your own authenticated Codex CLI. Preparing the copy makes no model calls; executing the stages makes 27 calls. Raw local run directories contain full runtime logs and are excluded from Git by default. Exact sampling and hidden server-side model version are not controlled.", ""]
    lines += ["Run `python pilots/hr_v01/export_report.py` to generate report views and an anonymous human-review sheet in `pilots/hr_v01/rendered/`. This uses the published responses and makes no model calls.", ""]
    save_markdown("REPORT_en.md", "\n".join(lines))
    comparison = ["# Complete observed recruiting posts", "", "All materials are fictional. These are unedited model outputs from the recorded pilot, not examples selected for quality."]
    for task in tasks:
        comparison += ["", "## " + task["case_id"], "", task["task"]]
        for arm, label in LABEL.items():
            response = responses[task["case_id"], arm]
            row = next(r for r in data["rows"] if r["case_id"] == task["case_id"] and r["arm"] == arm)
            comparison += ["", "### " + label, "", response["post"], "",
                           f"Model-assessed total: {row['total']}/10. Programmatic word count: {row['word_count']}.", ""]
            for note in response["editorial_notes"]:
                comparison.append("- " + note)
            if row["critical_errors"]:
                comparison += ["", "Model-flagged critical errors:", ""] + ["- " + e for e in row["critical_errors"]]
    save_markdown("OUTPUTS.md", "\n".join(comparison) + "\n")
    review = ["# Human review sheet — HR pilot v0.1", "",
        "This sheet contains anonymous, unedited model outputs and no model-assessed scores. No human review has yet been collected. Review the task sources and [rubric](rubric.json) before rating. Avoid the result report and condition mapping until ratings are complete.", "",
        "Reviewer: ______  Date: ______  Relevant professional experience: ______", "",
        "For each output, score factual fidelity, task completeness, audience fit, work specificity and instruction/context fit from 0 to 2 using the frozen rubric. Record critical errors and uncertainty separately. Scores do not measure editing time; record actual time only if an editing task is separately performed.", "",
        "Shared task instructions:", "", task_data["shared_instructions"], "",
        "Read the historical work records in the `episodes` field of the [development evidence](../../src/grounded_reflection/examples/hr_evidence.json). The model judge received these records too. The curated hypotheses and candidates in that file were excluded from the experiment."]
    for task in tasks:
        case_id = task["case_id"]
        review += ["", "## " + case_id, "", task["task"], "", "Current source materials:"]
        for source in task["sources"]:
            review += ["", "**" + source["source_id"] + "**", "", source["text"]]
        for label, arm in clean["blind_mapping"][case_id].items():
            response = responses[case_id, arm]
            review += ["", "### " + label, "", response["post"], "", "Editorial notes:", ""]
            review += ["- " + note for note in response["editorial_notes"]]
            review += ["", "| Criterion | Score 0–2 | Evidence / uncertainty |", "| --- | --- | --- |"]
            review += ["| " + criterion["id"] + " |  |  |" for criterion in read(ROOT / "rubric.json")["criteria"]]
            review += ["", "Critical errors, if any: ______", "", "Additional observations: ______"]
    save_markdown("HUMAN_REVIEW.md", "\n".join(review) + "\n")


if __name__ == "__main__":
    main()
