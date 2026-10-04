"""Read-only field audit of a sealed calibration, separate from registered scoring.

This script never changes model responses, recomputes calibration gates, or
authorises a main run. It uses only the standard library and makes no model calls.
"""

import argparse
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fields(items):
    return {item["name"]: item["value"] for item in items}


def audit(run):
    manifest = read(run / "artifact_manifest.json")
    for relative, expected in manifest.items():
        path = (run / relative).resolve()
        if not path.is_relative_to(run):
            raise ValueError("manifest path escapes the run directory")
        if sha256(path) != expected:
            raise ValueError(f"sealed artifact changed: {relative}")

    result = read(run / "results.json")
    tasks = {item["task_id"]: item for item in read(run / "public/tasks.json")}
    summaries, audited_rows = {}, []
    for row in result["rows"]:
        arm, probe = row["arm"], row["probe"]
        call_id = f'{arm}-{row["repetition"]}-{row["task_id"]}'
        record_path = run / "calls" / call_id / "record.json"
        record = read(record_path) if record_path.is_file() else {}
        response = record.get("response") or {}
        actual = fields(response.get("fields", []))
        baseline = fields(tasks[row["task_id"]]["baseline_fields"])
        usable = bool(record.get("status") == "completed"
                      and response.get("task_id") == row["task_id"]
                      and response.get("completed") is True
                      and response.get("questions") == [])
        exact = usable and actual == row["world_fields"]
        effective_decision = ("apply" if actual != baseline else "keep") if usable else None
        label_mismatch = usable and response.get("decision") != effective_decision
        summary = summaries.setdefault(arm, {}).setdefault(probe, {
            "planned": 0, "registered_update_correct": 0,
            "registered_world_compliant": 0, "exact_fields_in_completed_output": 0,
            "declared_decision_mismatches": 0,
        })
        summary["planned"] += 1
        summary["registered_update_correct"] += bool(row["update_correct"])
        summary["registered_world_compliant"] += bool(row["world_compliant"])
        summary["exact_fields_in_completed_output"] += exact
        summary["declared_decision_mismatches"] += label_mismatch
        audited_rows.append({
            "call_id": call_id, "scenario": row["scenario_id"], "probe": probe,
            "arm": arm, "task_id": row["task_id"],
            "registered_update_correct": row["update_correct"],
            "registered_world_compliant": row["world_compliant"],
            "exact_fields_in_completed_output": exact,
            "declared_decision": response.get("decision"),
            "effective_decision": effective_decision,
            "declared_decision_mismatch": label_mismatch,
            "actual_equals_warranted_fields": usable and actual == row["expected_warranted_fields"],
            "actual_fields": actual, "registered_errors": row["errors"],
        })
    return {
        "analysis": "posthoc_field_audit_not_registered_primary_result",
        "source_run": run.name,
        "source_results_sha256": sha256(run / "results.json"),
        "artifact_manifest_sha256": sha256(run / "artifact_manifest.json"),
        "audit_script_sha256": sha256(Path(__file__)),
        "verified_sealed_files": len(manifest),
        "registered_calibration_passed": result["calibration"]["passed"],
        "registered_failed_checks": [name for name, passed in result["calibration"]["checks"].items()
                                     if not passed],
        "reported_budget": result["budget"],
        "definition": "Exact field equality in a decoded, completed response for the correct task, "
                      "with no employee questions. It ignores decision labels and rule validity. "
                      "It is neither update warrant nor real-world professional quality.",
        "summary": summaries,
        "rows": audited_rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    run = args.run.resolve()
    if args.out and args.out.resolve().is_relative_to(run):
        parser.error("audit output must stay outside the sealed run")
    payload = json.dumps(audit(run), indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
