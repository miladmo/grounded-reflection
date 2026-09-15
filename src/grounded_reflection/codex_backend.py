"""Recorded, tool-free Codex CLI inference for a bounded research pilot.

The backend is optional: it uses the caller's installed/authenticated Codex CLI,
does not read credentials, and does not retry or repair failed model responses.
It preserves raw local run artifacts. Review those artifacts before publication.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import time
from typing import Any


DISABLED_FEATURES = (
    "shell_tool", "unified_exec", "multi_agent", "memories", "apps", "plugins",
    "hooks", "browser_use", "browser_use_external", "computer_use",
    "image_generation", "skill_search", "workspace_dependencies",
)
ALLOWED_ITEM_TYPES = frozenset({"reasoning", "agent_message"})
ALLOWED_EVENT_TYPES = frozenset({
    "thread.started", "turn.started", "item.started", "item.updated",
    "item.completed", "turn.completed", "turn.failed", "error",
})


class InferenceRunError(RuntimeError):
    """A run failed; its available artifacts and metadata remain on disk."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _text(value: str | bytes | None) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value or ""


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
                    encoding="utf-8")


def _audit_events(stdout: str) -> dict[str, Any]:
    """Fail closed on unsupported event/item types, preserving observed types.

    Unknown items are conservatively marked as potential tool use. This is a
    post-run audit, not a replacement for CLI capability/sandbox restrictions.
    """
    event_types: set[str] = set()
    item_types: set[str] = set()
    issues: list[str] = []
    usage: dict[str, Any] | None = None
    completed_turns = 0
    for line_number, line in enumerate(stdout.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            issues.append(f"stdout line {line_number} is not valid JSON")
            continue
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            issues.append(f"stdout line {line_number} lacks an event type")
            continue
        event_type = event["type"]
        event_types.add(event_type)
        if event_type not in ALLOWED_EVENT_TYPES:
            issues.append(f"unsupported event type: {event_type}")
        if event_type in {"turn.failed", "error"}:
            issues.append(f"CLI emitted {event_type}")
        if event_type.startswith("item."):
            item = event.get("item")
            item_type = item.get("type") if isinstance(item, dict) else None
            if not isinstance(item_type, str):
                issues.append(f"stdout line {line_number} lacks an item type")
            else:
                item_types.add(item_type)
                if item_type not in ALLOWED_ITEM_TYPES:
                    issues.append(f"tool or unsupported item type: {item_type}")
        if event_type == "turn.completed":
            completed_turns += 1
            usage_value = event.get("usage")
            if isinstance(usage_value, dict):
                usage = usage_value
    if completed_turns != 1:
        issues.append(f"expected one completed turn; observed {completed_turns}")
    return {
        "event_types": sorted(event_types),
        "item_types": sorted(item_types),
        "allowed_item_types": sorted(ALLOWED_ITEM_TYPES),
        "tool_use_detected": bool(item_types - ALLOWED_ITEM_TYPES),
        "usage": usage,
        "completed_turns": completed_turns,
        "audit_issues": list(dict.fromkeys(issues)),
    }


def run_completion(
    prompt: str,
    schema: dict,
    run_dir: Path,
    model: str,
    reasoning_effort: str,
    timeout_seconds: int = 420,
    *,
    executable: str | None = None,
) -> dict[str, Any]:
    """Run one structured inference call and return response plus metadata.

    ``run_dir`` must be absent or empty. Its isolated ``model-workspace`` child
    is empty; the prompt is supplied on stdin. No user config, project documents,
    tools, or persisted model session are requested. Managed policy remains in
    effect. The CLI validates the requested JSON schema; callers should also
    validate the parsed response against their own typed experiment contracts.
    """
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a nonempty string")
    if not isinstance(schema, dict) or not schema:
        raise ValueError("schema must be a nonempty JSON schema object")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("model must be explicitly specified")
    if not isinstance(reasoning_effort, str) or not reasoning_effort.strip():
        raise ValueError("reasoning_effort must be explicitly specified")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int) or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be a positive integer")
    # Verify serializability before creating any run files.
    json.dumps(schema, allow_nan=False)
    run_dir = Path(run_dir).resolve()
    if run_dir.exists() and (not run_dir.is_dir() or any(run_dir.iterdir())):
        raise FileExistsError(f"run_dir must be absent or empty: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=True)
    workspace = run_dir / "model-workspace"
    workspace.mkdir()
    schema_path = run_dir / "response.schema.json"
    final_path = run_dir / "final.json"
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    _write_json(schema_path, schema)

    metadata: dict[str, Any] = {
        "backend": "codex_cli",
        "requested_model": model,
        "requested_reasoning_effort": reasoning_effort,
        "reasoning_effort": reasoning_effort,
        "started_at": _utc_now(),
        "timeout_seconds": timeout_seconds,
        "disabled_features": list(DISABLED_FEATURES),
        "sandbox": "read-only",
        "ignore_user_config": True,
        "managed_policy_bypassed": False,
        "ephemeral": True,
        "returncode": None,
        "status": "running",
    }
    _write_json(run_dir / "metadata.json", metadata)
    started = time.perf_counter()
    stdout, stderr = "", ""
    failure: str | None = None
    parsed_response: dict | None = None
    resolved_executable = executable or shutil.which("codex")
    if not resolved_executable:
        failure = "Codex CLI was not found on PATH"
        metadata["status"] = "launch_failed"
    else:
        command = [
            resolved_executable, "exec", "--ignore-user-config", "--ephemeral",
            "--skip-git-repo-check", "--sandbox", "read-only", "--json", "--color", "never",
            "--output-schema", str(schema_path), "-o", str(final_path),
            "-C", str(workspace), "--model", model,
            "-c", "model_reasoning_effort=" + json.dumps(reasoning_effort),
            "-c", 'web_search="disabled"', "-c", "project_doc_max_bytes=0",
        ]
        for feature in DISABLED_FEATURES:
            command.extend(["--disable", feature])
        command.append("-")
        metadata["command"] = command
        try:
            process = subprocess.run(
                command, input=prompt, text=True, encoding="utf-8", errors="replace",
                capture_output=True, shell=False, cwd=workspace,
                timeout=timeout_seconds, check=False,
            )
            stdout, stderr = _text(process.stdout), _text(process.stderr)
            metadata["returncode"] = process.returncode
            if process.returncode != 0:
                failure = f"Codex CLI exited with code {process.returncode}"
                metadata["status"] = "process_failed"
        except subprocess.TimeoutExpired as exc:
            stdout, stderr = _text(exc.stdout), _text(exc.stderr)
            failure = f"Codex CLI exceeded {timeout_seconds} seconds"
            metadata["status"] = "timed_out"
        except OSError as exc:
            failure = f"Could not launch Codex CLI: {type(exc).__name__}: {exc}"
            metadata["status"] = "launch_failed"

    (run_dir / "stdout.jsonl").write_text(stdout, encoding="utf-8")
    (run_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
    metadata.update(_audit_events(stdout))
    if failure is None and metadata["audit_issues"]:
        failure = "; ".join(metadata["audit_issues"])
        metadata["status"] = "audit_failed"
    if failure is None:
        try:
            parsed_response = json.loads(final_path.read_text(encoding="utf-8-sig"))
            if not isinstance(parsed_response, dict):
                raise ValueError("final response must be a JSON object")
        except (OSError, ValueError) as exc:
            failure = f"Invalid or missing final JSON: {type(exc).__name__}: {exc}"
            metadata["status"] = "response_failed"
    metadata["finished_at"] = _utc_now()
    metadata["wall_seconds"] = round(time.perf_counter() - started, 6)
    if failure is None:
        metadata["status"] = "completed"
    else:
        metadata["error"] = failure
    _write_json(run_dir / "metadata.json", metadata)
    if failure is not None:
        raise InferenceRunError(f"{failure}. Preserved run artifacts: {run_dir}")
    return {"response": parsed_response, "metadata": metadata}
