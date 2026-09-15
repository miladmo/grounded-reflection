"""Small local CLI. No model calls, remote telemetry or deployment side effects."""

from __future__ import annotations

import argparse
from importlib.resources import files
import json
from pathlib import Path
import sys

from .models import EvidenceBundle, PairedEvaluation, SelectionDecision, SelectionPolicy, SplitManifest
from .workflow import assess_candidate, context_artifact, select_update, verify_references


def load_example() -> EvidenceBundle:
    return EvidenceBundle.model_validate_json(
        files("grounded_reflection").joinpath("examples/hr_evidence.json").read_text(encoding="utf-8"))


def read_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_outputs(directory: str, payloads: dict[str, object]) -> None:
    """Refuse to overwrite existing output files."""
    destination = Path(directory)
    if any((destination / name).exists() for name in payloads):
        raise ValueError("An output file already exists; choose a new output directory")
    destination.mkdir(parents=True, exist_ok=True)
    for name, payload in payloads.items():
        (destination / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2,
                                                   allow_nan=False) + "\n", encoding="utf-8")


def demo(output: str | None) -> dict:
    bundle = load_example()
    assessments = [assess_candidate(c, bundle) for c in bundle.candidates]
    splits = SplitManifest(development=[e.episode_id for e in bundle.episodes],
                           validation=["reserved-validation-01", "reserved-validation-02"],
                           final_test=["reserved-final-01"])
    candidate = next(c for c in bundle.candidates if c.candidate_id == "scoped-update")
    decision = select_update(candidate, bundle, [], splits, baseline_version="unmodified-agent")
    summary = {
        "status": "research-infrastructure demonstration",
        "data_origin": "synthetic",
        "hypothesis_origin": "curated_fixture",
        "model_calls": 0,
        "episodes": len(bundle.episodes),
        "evidence_items": sum(len(e.evidence) for e in bundle.episodes),
        "candidates": [a.model_dump(mode="json") for a in assessments],
        "selection": decision.model_dump(mode="json"),
        "interpretation": "Reference and scope checks executed. No performance evaluation was run; "
                          "the baseline identifier is retained and no context update is exported.",
    }
    if output:
        write_outputs(output, {"summary.json": summary, "evidence.json": bundle.model_dump(mode="json"),
                               "splits.json": splits.model_dump(mode="json")})
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect evidence contracts and adaptation decisions.")
    sub = parser.add_subparsers(dest="command", required=True)
    p_demo = sub.add_parser("demo", help="Replay the authored HR example without model calls")
    p_demo.add_argument("--output", help="New directory for JSON artifacts")
    p_validate = sub.add_parser("validate", help="Validate a bundle and resolve its evidence references")
    p_validate.add_argument("bundle")
    p_schema = sub.add_parser("schema", help="Export versioned JSON Schema contracts")
    p_schema.add_argument("--output", required=True)
    p_select = sub.add_parser("select", help="Evaluate one candidate using caller-supplied paired validation records")
    for flag in ("bundle", "candidate", "records", "splits", "baseline", "output"):
        p_select.add_argument("--" + flag, required=True)
    p_select.add_argument("--policy", help="SelectionPolicy JSON; defaults are demonstration settings")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            result = demo(args.output)
        elif args.command == "validate":
            bundle = EvidenceBundle.model_validate(read_json(args.bundle))
            problems = {h.hypothesis_id: errors for h in bundle.hypotheses
                        if (errors := verify_references(h, bundle.episodes))}
            result = {"references_valid": not problems, "reference_errors": problems,
                      "assessments": [assess_candidate(c, bundle).model_dump(mode="json")
                                      for c in bundle.candidates]}
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 1 if problems else 0
        elif args.command == "schema":
            schemas = {model.__name__ + ".schema.json": model.model_json_schema()
                       for model in (EvidenceBundle, PairedEvaluation, SplitManifest,
                                     SelectionPolicy, SelectionDecision)}
            write_outputs(args.output, schemas)
            result = {"schema_version": "0.1", "files": list(schemas)}
        else:
            bundle = EvidenceBundle.model_validate(read_json(args.bundle))
            candidate = next((c for c in bundle.candidates if c.candidate_id == args.candidate), None)
            if candidate is None:
                raise ValueError("Unknown candidate ID")
            raw_records = read_json(args.records)
            if not isinstance(raw_records, list):
                raise ValueError("Records must be a JSON array")
            records = [PairedEvaluation.model_validate(r) for r in raw_records]
            splits = SplitManifest.model_validate(read_json(args.splits))
            policy = SelectionPolicy.model_validate(read_json(args.policy)) if args.policy else SelectionPolicy()
            decision = select_update(candidate, bundle, records, splits, args.baseline, policy)
            payloads = {"decision.json": decision.model_dump(mode="json")}
            if decision.status == "accepted" and "fixture" not in decision.record_origins:
                payloads["context.json"] = context_artifact(candidate, decision)
            write_outputs(args.output, payloads)
            result = {"decision": decision.model_dump(mode="json"), "written": list(payloads),
                      "notice": "A policy decision over supplied ratings is not independent evidence of improvement. "
                                "No agent has been changed or deployed."}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
