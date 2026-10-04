"""Attested Codex CLI transport for v04; no model calls occur on import.

The empty temporary cwd is independent of the repository. Isolation also relies
on the pinned request capabilities checked in the local, non-inference preflight.
Read-only sandboxing alone does not prevent reading external files.
"""

from __future__ import annotations

from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from typing import Any

from grounded_reflection.codex_backend import (
    DISABLED_FEATURES as LEGACY_DISABLED_FEATURES,
    InferenceRunError, _audit_events, _text, _utc_now, _write_json,
)


from . import gateway

TRANSPORT_DIR = Path(__file__).resolve().parents[1] / "transport"
DISABLED_FEATURES = LEGACY_DISABLED_FEATURES + (
    "view_image", "goals", "sleep_tool", "code_mode", "code_mode_host",
    "multi_agent_v2", "tool_suggest", "collaboration_modes",
    "default_mode_request_user_input", "unbounded_connection_retries",
)
REMOVED_ENDPOINT_VARIABLES = frozenset({
    "OPENAI_BASE_URL", "OPENAI_API_BASE", "AZURE_OPENAI_ENDPOINT",
    "OPENAI_ORG_ID", "OPENAI_PROJECT_ID", "OPENAI_API_TYPE", "OPENAI_API_VERSION",
})


def fixed_arguments(catalog_path: Path) -> list[str]:
    """Exact static CLI arguments covered by the runtime attestation."""
    arguments = [
        "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check",
        "--sandbox", "read-only", "--json", "--color", "never",
    ]
    settings = [
        'web_search="disabled"', "project_doc_max_bytes=0", 'forced_login_method="chatgpt"',
        "tools.experimental_request_user_input={enabled=false}",
        "features.enable_request_compression=false",
        "model_catalog_json=" + json.dumps(catalog_path.resolve().as_posix()),
        'model_provider="reflectai_codex"', 'model_providers.reflectai_codex.name="OpenAI"',
        'model_providers.reflectai_codex.wire_api="responses"',
        "model_providers.reflectai_codex.requires_openai_auth=true",
        "model_providers.reflectai_codex.supports_websockets=false",
        "model_providers.reflectai_codex.request_max_retries=0",
        "model_providers.reflectai_codex.stream_max_retries=0",
    ]
    for setting in settings:
        arguments.extend(["-c", setting])
    for feature in DISABLED_FEATURES:
        arguments.extend(["--disable", feature])
    return arguments


def _sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


@lru_cache(maxsize=8)
def _binary_hash(path: str, signature: tuple[int, int, int, int]) -> str:
    # The signature keys the cache; replacements/updates require a fresh digest.
    return _sha256(Path(path))


def _attest(executable: str, catalog_path: Path) -> dict:
    attestation = json.loads((TRANSPORT_DIR / "runtime-attestation.json").read_text(encoding="utf-8"))
    cli_path = Path(executable).resolve(strict=True)
    stat = cli_path.stat()
    digest = _binary_hash(str(cli_path), (stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns))
    cli = attestation.get("cli", {})
    checks = attestation.get("isolation_check", {})
    valid = (
        attestation.get("schema_version") == 1
        and Path(cli.get("path", "")).resolve() == cli_path
        and cli.get("sha256") == digest
        and isinstance(cli.get("version"), str) and bool(cli["version"].strip())
        and attestation.get("transport_sha256") == _sha256(Path(__file__))
        and attestation.get("gateway_sha256") == _sha256(Path(gateway.__file__))
        and attestation.get("catalog_sha256") == _sha256(catalog_path)
        and attestation.get("fixed_arguments") == fixed_arguments(catalog_path)
        and attestation.get("allowed_request_tools") == []
        and all(checks.get(key) is True for key in (
            "passed", "workspace_outside_repository", "no_filesystem_code_or_network_tools",
            "no_request_tools",
        ))
        and isinstance(checks.get("checked_at"), str) and bool(checks["checked_at"].strip())
    )
    if not valid:
        raise ValueError("Runtime attestation does not match the CLI, transport, catalog or capabilities")
    return attestation


def _environment() -> tuple[dict[str, str], list[str]]:
    removed = sorted(key for key in os.environ if (
        any(token in key.upper() for token in ("API_KEY", "ACCESS_TOKEN", "AUTH_TOKEN"))
        or key.upper() in REMOVED_ENDPOINT_VARIABLES
    ))
    return {key: value for key, value in os.environ.items() if key not in removed}, removed


def run_completion(
    prompt: str, schema: dict, run_dir: Path, model: str, reasoning_effort: str,
    timeout_seconds: int = 420, *, executable: str | None = None,
) -> dict[str, Any]:
    """One attested invocation, without retries or API-key fallback.

    Credentials remain managed by the installed CLI. The schema and preserved
    run artifacts stay outside the empty model cwd; the prompt travels on stdin.
    An absent or mismatched local attestation fails before spawning the CLI.
    """
    for name, value in (("prompt", prompt), ("model", model), ("reasoning_effort", reasoning_effort)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a nonempty string")
    if not isinstance(schema, dict) or not schema:
        raise ValueError("schema must be a nonempty JSON schema object")
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int) or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be a positive integer")
    json.dumps(schema, allow_nan=False)
    run_dir = Path(run_dir).resolve()
    if run_dir.exists() and (not run_dir.is_dir() or any(run_dir.iterdir())):
        raise FileExistsError(f"run_dir must be absent or empty: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=True)
    schema_path, final_path = run_dir / "response.schema.json", run_dir / "final.json"
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    _write_json(schema_path, schema)
    metadata: dict[str, Any] = {
        "backend": "codex_cli", "requested_model": model,
        "requested_reasoning_effort": reasoning_effort, "reasoning_effort": reasoning_effort,
        "started_at": _utc_now(), "timeout_seconds": timeout_seconds,
        "disabled_features": list(DISABLED_FEATURES), "sandbox": "read-only",
        "ignore_user_config": True, "managed_policy_bypassed": False,
        "ephemeral": True, "returncode": None, "status": "preflight",
        "retries": 0, "required_request_tools": [],
        "isolation_basis": "Empty external cwd and locally inspected request capabilities; not OS read denial",
    }
    started = time.perf_counter()
    stdout, stderr, failure, parsed_response = "", "", None, None
    try:
        resolved = executable or shutil.which("codex")
        if not resolved:
            raise ValueError("Codex CLI was not found on PATH")
        catalog = TRANSPORT_DIR / "model-catalog.json"
        attestation = _attest(resolved, catalog)
        catalog_models = json.loads(catalog.read_text(encoding="utf-8"))["models"]
        if model not in {entry["slug"] for entry in catalog_models}:
            raise ValueError("Requested model is absent from the attested catalog")
        metadata["runtime_attestation"] = attestation
        metadata["remaining_attested_request_tools"] = attestation["allowed_request_tools"]
        environment, metadata["removed_environment_variables"] = _environment()
        repository = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory(prefix="reflectai-v04-model-") as directory, \
                gateway.one_request_gateway(timeout_seconds) as relay:
            workspace = Path(directory).resolve()
            if workspace.is_relative_to(repository) or workspace.is_relative_to(run_dir):
                raise ValueError("Temporary model workspace must be outside the repository and run artifacts")
            if any(workspace.iterdir()):
                raise ValueError("Temporary model workspace must be empty")
            command = [str(Path(resolved).resolve()), *fixed_arguments(catalog),
                       "--output-schema", str(schema_path), "-o", str(final_path),
                       "-C", str(workspace), "--model", model,
                       "-c", "model_reasoning_effort=" + json.dumps(reasoning_effort),
                       "-c", "model_providers.reflectai_codex.base_url=" + json.dumps(relay.base_url), "-"]
            metadata.update(command=command, workspace=str(workspace),
                            workspace_was_empty=True, workspace_outside_repository=True, status="running")
            _write_json(run_dir / "metadata.json", metadata)
            try:
                process = subprocess.run(
                    command, input=prompt, text=True, encoding="utf-8", errors="replace",
                    capture_output=True, shell=False, cwd=workspace, env=environment,
                    timeout=timeout_seconds, check=False,
                )
            finally:
                metadata["gateway"] = relay.summary
            stdout, stderr = _text(process.stdout), _text(process.stderr)
            metadata["returncode"] = process.returncode
            if process.returncode != 0:
                failure = f"Codex CLI exited with code {process.returncode}"
                metadata["status"] = "process_failed"
    except subprocess.TimeoutExpired as exc:
        stdout, stderr = _text(exc.stdout), _text(exc.stderr)
        failure, metadata["status"] = f"Codex CLI exceeded {timeout_seconds} seconds", "timed_out"
    except (OSError, ValueError, KeyError, TypeError) as exc:
        failure = f"Transport rejected or failed: {type(exc).__name__}: {exc}"
        metadata["status"] = "preflight_failed" if metadata["status"] == "preflight" else "launch_failed"
    (run_dir / "stdout.jsonl").write_text(stdout, encoding="utf-8")
    (run_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
    metadata.update(_audit_events(stdout))
    relay_result = metadata.get("gateway", {})
    if failure is None and not (relay_result.get("upstream_requests") == 1
                               and relay_result.get("blocked_requests") == 0
                               and relay_result.get("response_events_blocked") == 0
                               and relay_result.get("completed") is True
                               and relay_result.get("failure") is None):
        failure, metadata["status"] = "Gateway integrity check failed", "audit_failed"
        metadata["audit_issues"].append(failure)
    if failure is None and metadata["audit_issues"]:
        failure, metadata["status"] = "; ".join(metadata["audit_issues"]), "audit_failed"
    if failure is None:
        try:
            parsed_response = json.loads(final_path.read_text(encoding="utf-8-sig"))
            if not isinstance(parsed_response, dict):
                raise ValueError("final response must be a JSON object")
        except (OSError, ValueError) as exc:
            failure, metadata["status"] = f"Invalid or missing final JSON: {exc}", "response_failed"
    metadata.update(finished_at=_utc_now(), wall_seconds=round(time.perf_counter() - started, 6))
    metadata["status"] = metadata["status"] if failure else "completed"
    if failure:
        metadata["error"] = failure
    _write_json(run_dir / "metadata.json", metadata)
    if failure:
        raise InferenceRunError(f"{failure}. Preserved run artifacts: {run_dir}")
    return {"response": parsed_response, "metadata": metadata}
