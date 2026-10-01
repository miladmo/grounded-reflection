"""One direct FHGenie completion through a credential-isolating PS7 driver.

Importing this module performs no I/O. Only the public prompt and response
schema become messages; no tools, files, evaluator data or session are attached.
The driver decrypts the Windows-user DPAPI credential in its own process and
returns an allowlisted envelope, never raw HTTP bodies or reasoning content.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
from typing import Any

from grounded_reflection.codex_backend import InferenceRunError, _utc_now, _write_json


MODEL = "deepseek-ai/DeepSeek-V4-Flash-0731"
# The endpoint address is not published. It is read from the environment or a
# local file outside the repository and must match this SHA-256 before any call.
ENDPOINT_SHA256 = "36247a636ec109c62faa6d828357e6027571e8f56e1c6890e8e0d169acc730db"
ENDPOINT_ENV = "REFLECTAI_FHGENIE_ENDPOINT"
ENDPOINT_PLACEHOLDER = "<FHGENIE_ENDPOINT>"
DRIVER = Path(__file__).resolve().parents[1] / "transport" / "fhgenie-request.ps1"
# Amendment 4: the model card's documented levels; the run fixes one of them.
REASONING_EFFORTS = ("low", "high", "max")
USAGE_KEYS = ("input_tokens", "output_tokens", "cached_input_tokens", "reasoning_output_tokens")
MAX_CONTENT_BYTES = 1_048_576
ERROR_CODES = frozenset({
    "request_invalid", "credential_unavailable", "credential_invalid", "http_error",
    "response_rejected", "response_invalid_json", "response_model_invalid",
    "response_model_mismatch", "response_usage_invalid", "response_usage_unknown",
    "response_choice_invalid", "response_finish_invalid", "response_role_invalid",
    "response_tool_call", "response_refusal", "response_content_invalid", "local_error",
})
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/+@-]{0,199}\Z")
FINGERPRINT = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,99}\Z")


def _object(pairs: list[tuple[str, Any]]) -> dict:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON property")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ValueError("Nonfinite JSON number")


def _finite_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("Nonfinite JSON number")
    return number


def _parse_object(text: str) -> dict:
    value = json.loads(text, object_pairs_hook=_object, parse_constant=_invalid_constant,
                       parse_float=_finite_float)
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object")
    return value


def _environment() -> dict[str, str]:
    # Names/values are never logged. Endpoint overrides and inherited credentials
    # are unnecessary for a fixed-endpoint, DPAPI-only driver.
    return {key: value for key, value in os.environ.items()
            if not any(token in key.upper() for token in
                       ("KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "AUTH", "PROXY"))
            and key.upper() not in {"OPENAI_BASE_URL", "OPENAI_API_BASE", "AZURE_OPENAI_ENDPOINT",
                                    "OPENAI_ORG_ID", "OPENAI_PROJECT_ID", "OPENAI_API_TYPE",
                                    "OPENAI_API_VERSION", "PSMODULEPATH"}}


def endpoint_file() -> Path:
    return Path(os.environ.get("LOCALAPPDATA", "")) / "reflectAI" / "fhgenie-endpoint.txt"


def resolve_endpoint() -> str:
    """Return the locally configured endpoint only if it matches the pinned hash."""
    value = os.environ.get(ENDPOINT_ENV)
    if value is None:
        try:
            value = endpoint_file().read_text(encoding="utf-8")
        except OSError:
            raise ValueError("endpoint_unavailable") from None
    value = value.strip()
    if hashlib.sha256(value.encode("utf-8")).hexdigest() != ENDPOINT_SHA256:
        raise ValueError("endpoint_unverified")
    return value


def _count(value: Any) -> bool:
    return type(value) is int and 0 <= value <= 2**63 - 1


def _capture_envelope(envelope: dict, metadata: dict) -> str | None:
    """Copy only typed, bounded fields; never persist the process output itself."""
    issues = metadata["audit_issues"]
    allowed = {"schema_version", "status", "error_code", "network_requests", "http_status",
               "actual_model", "system_fingerprint", "finish_reason", "usage",
               "tool_use_detected", "reasoning_content_present", "refusal_present",
               "final_content", "role", "choice_count"}
    if set(envelope) != allowed or type(envelope.get("schema_version")) is not int \
            or envelope["schema_version"] != 1:
        issues.append("driver_envelope_invalid")
        return None
    if envelope.get("status") not in ("completed", "process_failed"):
        issues.append("driver_status_invalid")
    error_code = envelope.get("error_code")
    if error_code in ERROR_CODES:
        issues.append(error_code)
    elif error_code is not None:
        issues.append("driver_error_invalid")
    if envelope.get("status") != "completed" and not issues:
        issues.append("driver_not_completed")
    for key in ("tool_use_detected", "reasoning_content_present", "refusal_present"):
        if type(envelope.get(key)) is bool:
            metadata[key] = envelope[key]
        else:
            issues.append("driver_flags_invalid")
    if metadata["tool_use_detected"]:
        issues.append("response_tool_call")
    if metadata["refusal_present"]:
        issues.append("response_refusal")
    for key, pattern in (("actual_model", IDENTIFIER), ("system_fingerprint", FINGERPRINT),
                         ("finish_reason", FINGERPRINT), ("role", FINGERPRINT)):
        value = envelope.get(key)
        if isinstance(value, str) and pattern.fullmatch(value):
            metadata[key] = value
        elif value is not None:
            issues.append("driver_identifiers_invalid")
    if metadata["actual_model"] != MODEL:
        issues.append("response_model_mismatch")
    metadata["response_model"] = metadata["actual_model"]
    if metadata["finish_reason"] != "stop":
        issues.append("response_finish_invalid")
    if metadata.get("role") != "assistant":
        issues.append("response_role_invalid")
    for key, minimum, maximum in (("http_status", 100, 599), ("network_requests", 0, 1),
                                  ("choice_count", 0, 1)):
        value = envelope.get(key)
        if type(value) is int and minimum <= value <= maximum:
            metadata[key] = value
        elif value is not None:
            issues.append("driver_http_metadata_invalid")
    if metadata["http_status"] != 200 or metadata["network_requests"] != 1:
        issues.append("http_completion_invalid")
    if metadata.get("choice_count") != 1:
        issues.append("response_choice_invalid")
    raw_usage = envelope.get("usage")
    if not isinstance(raw_usage, dict) or set(raw_usage) != set(USAGE_KEYS):
        issues.append("response_usage_invalid")
    else:
        for key in USAGE_KEYS:
            value = raw_usage[key]
            if value is None or _count(value):
                metadata["usage"][key] = value
            else:
                issues.append("response_usage_invalid")
        for subset, total in (("cached_input_tokens", "input_tokens"),
                              ("reasoning_output_tokens", "output_tokens")):
            if (metadata["usage"][subset] is not None and metadata["usage"][total] is not None
                    and metadata["usage"][subset] > metadata["usage"][total]):
                metadata["usage"][subset] = None
                issues.append("response_usage_invalid")
    if any(metadata["usage"][key] is None for key in ("input_tokens", "output_tokens")):
        issues.append("response_usage_unknown")
    content = envelope.get("final_content")
    if isinstance(content, str) and len(content.encode("utf-8")) <= MAX_CONTENT_BYTES:
        return content
    issues.append("response_content_invalid")
    return None


def run_completion(
    prompt: str, schema: dict, output_dir: Path, model: str, reasoning_effort: str,
    timeout_seconds: int = 420, *, max_output_tokens: int = 16384,
    executable: str | None = None,
) -> dict[str, Any]:
    """Attempt one request; reject malformed output without retries or repairs.

    ``request.json`` is the credential-free HTTP request. ``final.txt`` preserves
    the bounded final channel, even if it is invalid JSON; the separate reasoning
    channel is excluded. Final-channel text is never relabeled or repaired.
    Typed schema validation remains the caller's responsibility.
    """
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a nonempty string")
    if not isinstance(schema, dict) or not schema:
        raise ValueError("schema must be a nonempty JSON schema object")
    if model != MODEL or reasoning_effort not in REASONING_EFFORTS:
        raise ValueError("FHGenie requires the registered DeepSeek model and a documented reasoning effort")
    for name, value in (("timeout_seconds", timeout_seconds), ("max_output_tokens", max_output_tokens)):
        if type(value) is not int or not 0 < value <= 2**31 - 1:
            raise ValueError(f"{name} must be a positive 32-bit integer")
    schema_text = json.dumps(schema, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    request = {
        "model": model,
        "messages": [{"role": "system", "content":
                      "Return one JSON object conforming to the JSON schema below. "
                      "Return only the JSON object, without markdown fences or extra text. "
                      "Do not use tools. JSON schema: " + schema_text},
                     {"role": "user", "content": prompt}],
        "stream": False, "max_tokens": max_output_tokens, "reasoning_effort": reasoning_effort,
        "temperature": 1, "top_p": 1,
    }
    output_dir = Path(output_dir).resolve()
    if output_dir.exists() and (not output_dir.is_dir() or any(output_dir.iterdir())):
        raise FileExistsError("output_dir must be absent or empty")
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        raise InferenceRunError("FHGenie inference failed; the artifact directory is unavailable.") from None
    metadata: dict[str, Any] = {
        "backend": "fhgenie", "transport": "direct_http_via_powershell", "endpoint": ENDPOINT_PLACEHOLDER,
        "endpoint_sha256": ENDPOINT_SHA256,
        "requested_model": model, "actual_model": None, "response_model": None,
        "system_fingerprint": None,
        "requested_reasoning_effort": reasoning_effort, "reasoning_effort": reasoning_effort,
        "max_output_tokens": max_output_tokens, "temperature": 1, "top_p": 1,
        "started_at": _utc_now(), "timeout_seconds": timeout_seconds,
        "returncode": None, "status": "launch_failed", "retries": 0,
        "network_requests": None, "http_status": None, "finish_reason": None,
        "usage": dict.fromkeys(USAGE_KEYS), "audit_issues": [], "tool_use_detected": False,
        "reasoning_content_present": False, "refusal_present": False,
        "request_tools": [], "schema_mode": "prompt_only", "driver_sha256": None,
        "isolation_basis": "Direct chat request with no tools or session; empty subprocess cwd",
    }
    started = time.perf_counter()
    response = None
    failure = None
    process = None
    try:
        _write_json(output_dir / "request.json", request)
        metadata["driver_sha256"] = hashlib.sha256(DRIVER.read_bytes()).hexdigest()
        resolved = executable or shutil.which("pwsh")
        try:
            endpoint = resolve_endpoint()
        except ValueError as exc:
            endpoint, failure = None, str(exc)
        if failure is None and not resolved:
            failure = "powershell_7_unavailable"
        elif failure is None:
            # Only pwsh is searched; the driver also has #Requires -Version 7.0.
            command = [str(Path(resolved).resolve()), "-NoLogo", "-NoProfile", "-NonInteractive",
                       "-File", str(DRIVER.resolve())]
            repository = Path(__file__).resolve().parents[3]
            with tempfile.TemporaryDirectory(prefix="reflectai-v04-fhgenie-") as directory:
                workspace = Path(directory).resolve()
                if workspace.is_relative_to(repository) or workspace.is_relative_to(output_dir) \
                        or any(workspace.iterdir()):
                    raise ValueError("Temporary workspace must be empty and external")
                metadata.update(workspace_was_empty=True, workspace_outside_repository=True)
                _write_json(output_dir / "metadata.json", metadata)
                process = subprocess.run(
                    command, input=json.dumps({"request": request, "timeout_seconds": timeout_seconds,
                                               "endpoint": endpoint},
                                              ensure_ascii=False, allow_nan=False),
                    text=True, encoding="utf-8", errors="strict", capture_output=True,
                    shell=False, cwd=workspace, env=_environment(), timeout=timeout_seconds,
                    check=False,
                )
    except subprocess.TimeoutExpired:
        failure, metadata["status"] = "request_timed_out", "timed_out"
    except (OSError, ValueError, TypeError):
        # Never log exception messages: process failures can include secrets.
        failure = "transport_launch_or_artifact_failed"
    if process is not None:
        metadata.update(returncode=process.returncode, status="process_failed")
        try:
            if not isinstance(process.stdout, str) or len(process.stdout.encode("utf-8")) > 8_388_608:
                raise ValueError("Invalid driver output")
            final_content = _capture_envelope(_parse_object(process.stdout), metadata)
            if final_content is not None:
                (output_dir / "final.txt").write_text(final_content, encoding="utf-8")
                try:
                    response = _parse_object(final_content)
                except (ValueError, RecursionError):
                    metadata["audit_issues"].append("response_invalid_json")
            if process.returncode != 0:
                failure = "driver_process_failed"
            if metadata["audit_issues"]:
                failure = failure or "response_integrity_failed"
            if not failure:
                _write_json(output_dir / "final.json", response)
                metadata["status"] = "completed"
        except (ValueError, TypeError, RecursionError):
            failure = "driver_output_invalid"
            metadata["audit_issues"].append("driver_output_invalid")
        except OSError:
            failure = "response_artifact_failed"
    metadata["audit_issues"] = list(dict.fromkeys(metadata["audit_issues"]))
    metadata.update(finished_at=_utc_now(), wall_seconds=round(time.perf_counter() - started, 6))
    if failure:
        metadata["error"] = failure
    try:
        _write_json(output_dir / "metadata.json", metadata)
    except OSError:
        failure = "metadata_artifact_failed"
    if failure:
        raise InferenceRunError("FHGenie inference failed; inspect the preserved transport metadata.") from None
    return {"response": response, "metadata": metadata}
