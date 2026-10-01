"""Offline FHGenie transport contracts; every process launch is mocked."""

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from reflectai_v04 import fhgenie_transport as transport


# Offline endpoint fixture; the real address is not part of this repository.
TEST_ENDPOINT = "https://fhgenie.invalid/v1/chat/completions"
TEST_ENDPOINT_SHA256 = hashlib.sha256(TEST_ENDPOINT.encode("utf-8")).hexdigest()
SCHEMA = {"type": "object", "properties": {"answer": {"type": "string"}},
          "required": ["answer"], "additionalProperties": False}
ENVELOPE = {
    "schema_version": 1, "status": "completed", "error_code": None,
    "network_requests": 1, "http_status": 200, "actual_model": transport.MODEL,
    "system_fingerprint": "test-fingerprint", "finish_reason": "stop", "role": "assistant",
    "choice_count": 1, "usage": {"input_tokens": 24, "output_tokens": 33,
                                "cached_input_tokens": None, "reasoning_output_tokens": None},
    "tool_use_detected": False, "reasoning_content_present": True, "refusal_present": False,
    "final_content": '{"answer":"ok"}',
}


class FhgenieTransportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="v04-fhgenie-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.pwsh = self.root / "pwsh.exe"
        self.pwsh.write_bytes(b"offline fixture; never executed")
        for patcher in (patch.object(transport, "ENDPOINT_SHA256", TEST_ENDPOINT_SHA256),
                        patch.dict(os.environ, {transport.ENDPOINT_ENV: TEST_ENDPOINT})):
            patcher.start()
            self.addCleanup(patcher.stop)

    def invoke(self, name="run", **kwargs):
        return transport.run_completion("Public prompt only\nUnchanged ünicode.", SCHEMA,
                                        self.root / name, transport.MODEL, "low",
                                        executable=str(self.pwsh), **kwargs)

    def process(self, envelope=None, returncode=0, stderr=""):
        return subprocess.CompletedProcess([], returncode,
                                           json.dumps(ENVELOPE if envelope is None else envelope), stderr)

    def saved(self, name="run"):
        return json.loads((self.root / name / "metadata.json").read_text(encoding="utf-8"))

    def all_artifacts(self, name="run"):
        return "\n".join(path.read_text(encoding="utf-8") for path in (self.root / name).iterdir())

    def test_one_public_request_on_stdin_with_empty_external_cwd(self):
        private_canary = "EVALUATOR_CANARY_NEVER_SEND"
        (self.root / "private-truth.json").write_text(private_canary, encoding="utf-8")
        observed = {}

        def complete(command, **kwargs):
            workspace = Path(kwargs["cwd"])
            observed["workspace"] = workspace
            self.assertFalse(any(workspace.iterdir()))
            self.assertFalse(workspace.is_relative_to(self.root))
            self.assertFalse(kwargs["shell"])
            self.assertEqual(command, [str(self.pwsh.resolve()), "-NoLogo", "-NoProfile",
                                       "-NonInteractive", "-File", str(transport.DRIVER.resolve())])
            self.assertEqual(kwargs["timeout"], 420)
            self.assertNotIn("OPENAI_API_KEY", kwargs["env"])
            self.assertNotIn("FHGENIE_TOKEN", kwargs["env"])
            self.assertNotIn("CUSTOM_SECRET", kwargs["env"])
            self.assertNotIn("HTTPS_PROXY", kwargs["env"])
            self.assertNotIn("OPENAI_BASE_URL", kwargs["env"])
            self.assertNotIn("PSModulePath", kwargs["env"])
            self.assertEqual(kwargs["env"]["LOCALAPPDATA"], "fake-local-app-data")
            message = json.loads(kwargs["input"])
            self.assertEqual(set(message), {"request", "timeout_seconds", "endpoint"})
            self.assertEqual(message["endpoint"], TEST_ENDPOINT)
            request = message["request"]
            self.assertEqual(set(request), {"model", "messages", "stream", "max_tokens",
                                           "reasoning_effort", "temperature", "top_p"})
            self.assertFalse(request["stream"])
            self.assertEqual(request["max_tokens"], 16384)
            self.assertEqual(request["model"], transport.MODEL)
            self.assertEqual(request["temperature"], 1)
            self.assertEqual(request["top_p"], 1)
            self.assertEqual([m["role"] for m in request["messages"]], ["system", "user"])
            self.assertEqual(request["messages"][1]["content"], "Public prompt only\nUnchanged ünicode.")
            self.assertEqual(json.loads(request["messages"][0]["content"].split("JSON schema: ", 1)[1]), SCHEMA)
            self.assertNotIn(private_canary, kwargs["input"])
            self.assertNotIn("response_format", kwargs["input"])
            self.assertEqual(json.loads((self.root / "run" / "request.json").read_text(encoding="utf-8")), request)
            return self.process()

        with patch.dict(os.environ, {"OPENAI_API_KEY": "SECRET_ENV_VALUE", "FHGENIE_TOKEN": "SECRET_ENV_VALUE",
                                     "CUSTOM_SECRET": "SECRET_ENV_VALUE", "HTTPS_PROXY": "SECRET_ENV_VALUE",
                                     "OPENAI_BASE_URL": "https://unused.invalid", "PSModulePath": "unused",
                                     "LOCALAPPDATA": "fake-local-app-data"}), \
                patch.object(transport.subprocess, "run", side_effect=complete) as launch:
            result = self.invoke()
        launch.assert_called_once()
        self.assertFalse(observed["workspace"].exists())
        self.assertEqual(result["response"], {"answer": "ok"})
        metadata = result["metadata"]
        self.assertEqual(metadata["status"], "completed")
        self.assertEqual(metadata["backend"], "fhgenie")
        self.assertEqual(metadata["response_model"], transport.MODEL)
        self.assertEqual(metadata["actual_model"], transport.MODEL)
        self.assertEqual(metadata["usage"], ENVELOPE["usage"])
        self.assertTrue(metadata["reasoning_content_present"])
        self.assertEqual(metadata["driver_sha256"], hashlib.sha256(transport.DRIVER.read_bytes()).hexdigest())
        self.assertNotIn("runtime_attestation", metadata)
        self.assertNotIn("SECRET_ENV_VALUE", self.all_artifacts())
        self.assertEqual((self.root / "run" / "final.txt").read_text(), ENVELOPE["final_content"])

    def test_max_output_tokens_and_timeout_are_sent_exactly(self):
        with patch.object(transport.subprocess, "run", return_value=self.process()) as launch:
            self.invoke(max_output_tokens=2048, timeout_seconds=90)
        self.assertEqual(json.loads(launch.call_args.kwargs["input"])["request"]["max_tokens"], 2048)
        self.assertEqual(json.loads(launch.call_args.kwargs["input"])["timeout_seconds"], 90)
        self.assertEqual(launch.call_args.kwargs["timeout"], 90)

    def test_same_directory_cannot_repeat_an_attempt(self):
        with patch.object(transport.subprocess, "run", return_value=self.process()) as launch:
            self.invoke()
            with self.assertRaises(FileExistsError):
                self.invoke()
        launch.assert_called_once()

    def test_unconfigured_or_unverified_endpoint_never_launches(self):
        missing = self.root / "no-local-app-data"
        for name, env in (("missing", {"LOCALAPPDATA": str(missing)}),
                          ("wrong", {transport.ENDPOINT_ENV: "https://example.invalid/v1/chat/completions"})):
            with self.subTest(name=name), patch.dict(os.environ, env), \
                    patch.object(transport.subprocess, "run") as launch:
                if name == "missing":
                    os.environ.pop(transport.ENDPOINT_ENV)
                with self.assertRaises(transport.InferenceRunError):
                    self.invoke(name)
                launch.assert_not_called()
                saved = self.saved(name)
                self.assertEqual(saved["status"], "launch_failed")
                self.assertIn(saved["error"], ("endpoint_unavailable", "endpoint_unverified"))
                self.assertNotIn("example.invalid", json.dumps(saved))

    def test_local_endpoint_file_is_read_and_verified(self):
        local = self.root / "appdata"
        (local / "reflectAI").mkdir(parents=True)
        (local / "reflectAI" / "fhgenie-endpoint.txt").write_text(TEST_ENDPOINT + "\n", encoding="utf-8")
        with patch.dict(os.environ, {"LOCALAPPDATA": str(local)}):
            os.environ.pop(transport.ENDPOINT_ENV)
            self.assertEqual(transport.resolve_endpoint(), TEST_ENDPOINT)

    def test_documented_reasoning_levels_are_forwarded_unchanged(self):
        for effort in ("low", "high", "max"):
            with self.subTest(effort=effort), \
                    patch.object(transport.subprocess, "run", return_value=self.process()) as launch:
                result = transport.run_completion("public", SCHEMA, self.root / effort, transport.MODEL,
                                                  effort, executable=str(self.pwsh))
                request = json.loads(launch.call_args.kwargs["input"])["request"]
                self.assertEqual(request["reasoning_effort"], effort)
                self.assertEqual(result["metadata"]["requested_reasoning_effort"], effort)

    def test_settings_validation_precedes_any_launch(self):
        for changes in ({"model": "other"}, {"reasoning_effort": "medium"},
                        {"reasoning_effort": "xhigh"}, {"reasoning_effort": "HIGH"},
                        {"reasoning_effort": None}, {"prompt": " "},
                        {"schema": {}}, {"schema": {"value": float("nan")}},
                        {"max_output_tokens": True}, {"max_output_tokens": 0},
                        {"timeout_seconds": True}, {"timeout_seconds": -1}):
            arguments = {"prompt": "public", "schema": SCHEMA, "output_dir": self.root / "run",
                         "model": transport.MODEL, "reasoning_effort": "low"} | changes
            with self.subTest(changes=changes), patch.object(transport.subprocess, "run") as launch:
                with self.assertRaises(ValueError):
                    transport.run_completion(**arguments)
                launch.assert_not_called()
        self.assertFalse((self.root / "run").exists())

    def test_missing_pwsh_fails_without_launch_and_preserves_metadata(self):
        with patch.object(transport.shutil, "which", return_value=None), \
                patch.object(transport.subprocess, "run") as launch:
            with self.assertRaises(transport.InferenceRunError):
                transport.run_completion("public", SCHEMA, self.root / "run", transport.MODEL, "low")
        launch.assert_not_called()
        self.assertEqual(self.saved()["status"], "launch_failed")

    def test_workspace_inside_repository_is_rejected_before_launch(self):
        with patch.object(transport.tempfile, "TemporaryDirectory") as temp, \
                patch.object(transport.subprocess, "run") as launch:
            temp.return_value.__enter__.return_value = str(Path(transport.__file__).resolve().parent)
            with self.assertRaises(transport.InferenceRunError):
                self.invoke()
        launch.assert_not_called()

    def test_launch_timeout_and_exit_failures_never_retry_or_log_raw_errors(self):
        secret = "SECRET_AND_REASONING_NOT_FOR_ARTIFACTS"
        cases = [("launch", OSError(secret), "launch_failed"),
                 ("timeout", subprocess.TimeoutExpired("pwsh", 10, output=secret, stderr=secret), "timed_out"),
                 ("exit", self.process(returncode=1, stderr=secret), "process_failed")]
        for name, result, status in cases:
            with self.subTest(name=name):
                effect = result if isinstance(result, Exception) else lambda *args, **kwargs: result
                with patch.object(transport.subprocess, "run", side_effect=effect) as launch:
                    with self.assertRaises(transport.InferenceRunError) as failure:
                        self.invoke(name)
                launch.assert_called_once()
                self.assertNotIn(secret, str(failure.exception))
                self.assertNotIn(secret, self.all_artifacts(name))
                self.assertEqual(self.saved(name)["status"], status)
        self.assertEqual(self.saved("exit")["usage"]["input_tokens"], 24)

    def test_invalid_final_content_is_preserved_without_repair_or_second_call(self):
        cases = ['{"answer":"first","answer":"second"}', '{"outer":{"x":1,"x":2}}',
                 '{"value":NaN}', '{"value":Infinity}', '{"value":1e999}', '[]', 'null',
                 '```json\n{"answer":"ok"}\n```', '{"answer": {"answer":"ok"}',
                 'prefix {"answer":"ok"}', '{"answer":"ok"} trailing']
        for index, content in enumerate(cases):
            name = f"invalid-{index}"
            envelope = deepcopy(ENVELOPE) | {"final_content": content}
            with self.subTest(content=content), \
                    patch.object(transport.subprocess, "run", return_value=self.process(envelope)) as launch:
                with self.assertRaises(transport.InferenceRunError):
                    self.invoke(name)
            launch.assert_called_once()
            self.assertEqual((self.root / name / "final.txt").read_text(encoding="utf-8"), content)
            self.assertFalse((self.root / name / "final.json").exists())
            self.assertEqual(self.saved(name)["usage"]["output_tokens"], 33)
            self.assertIn("response_invalid_json", self.saved(name)["audit_issues"])

    def test_wrong_model_refusal_truncation_tool_calls_and_noncompleted_fail_closed(self):
        cases = [("actual_model", "other-model"), ("finish_reason", "length"),
                 ("tool_use_detected", True), ("refusal_present", True), ("role", "tool"),
                 ("choice_count", 0), ("network_requests", 0), ("http_status", 500),
                 ("status", "process_failed"), ("status", "unknown"), ("schema_version", True)]
        for index, (field, value) in enumerate(cases):
            name = f"failure-{index}"
            envelope = deepcopy(ENVELOPE) | {field: value}
            with self.subTest(field=field, value=value), \
                    patch.object(transport.subprocess, "run", return_value=self.process(envelope)) as launch:
                with self.assertRaises(transport.InferenceRunError):
                    self.invoke(name)
            launch.assert_called_once()
            self.assertEqual(self.saved(name)["status"], "process_failed")
            self.assertTrue(self.saved(name)["audit_issues"])
            self.assertFalse((self.root / name / "final.json").exists())

    def test_usage_is_required_and_known_counts_survive_failures(self):
        cases = [None, {}, {"input_tokens": None}, {"input_tokens": True}, {"output_tokens": -1},
                 {"cached_input_tokens": 25}, {"reasoning_output_tokens": 34}, {"input_tokens": 2.5},
                 {"output_tokens": "33"}]
        for index, change in enumerate(cases):
            name = f"usage-{index}"
            envelope = deepcopy(ENVELOPE)
            envelope["usage"] = (deepcopy(ENVELOPE["usage"]) | change) if change else change
            with self.subTest(change=change), \
                    patch.object(transport.subprocess, "run", return_value=self.process(envelope)) as launch:
                with self.assertRaises(transport.InferenceRunError):
                    self.invoke(name)
            launch.assert_called_once()
            saved = self.saved(name)
            self.assertEqual(saved["status"], "process_failed")
            self.assertEqual(set(saved["usage"]), set(transport.USAGE_KEYS))
            if change and "input_tokens" not in change:
                self.assertEqual(saved["usage"]["input_tokens"], 24)
        self.assertIsNone(self.saved("usage-0")["usage"]["input_tokens"])
        self.assertIsNone(self.saved("usage-3")["usage"]["input_tokens"])
        self.assertIsNone(self.saved("usage-5")["usage"]["cached_input_tokens"])

    def test_optional_usage_remains_unknown_or_preserves_reported_zero(self):
        envelope = deepcopy(ENVELOPE)
        envelope["usage"].update(cached_input_tokens=0, reasoning_output_tokens=5)
        with patch.object(transport.subprocess, "run", return_value=self.process(envelope)):
            result = self.invoke()
        self.assertEqual(result["metadata"]["usage"]["cached_input_tokens"], 0)
        self.assertEqual(result["metadata"]["usage"]["reasoning_output_tokens"], 5)

    def test_untrusted_output_and_extra_reasoning_fields_are_not_saved(self):
        secret = "SECRET_OR_PRIVATE_REASONING"
        cases = [secret, json.dumps(ENVELOPE | {"reasoning_content": secret}),
                 json.dumps(ENVELOPE | {"error_code": secret}),
                 json.dumps(ENVELOPE | {"actual_model": secret + "\n"}),
                 '{"schema_version":1,"schema_version":1}', 'null']
        for index, stdout in enumerate(cases):
            name = f"redacted-{index}"
            process = subprocess.CompletedProcess([], 0, stdout, secret)
            with self.subTest(index=index), \
                    patch.object(transport.subprocess, "run", return_value=process):
                with self.assertRaises(transport.InferenceRunError) as failure:
                    self.invoke(name)
            self.assertNotIn(secret, str(failure.exception))
            self.assertNotIn(secret, self.all_artifacts(name))
            self.assertFalse((self.root / name / "stdout.json").exists())
            self.assertFalse((self.root / name / "stderr.txt").exists())

    def test_final_artifact_failure_preserves_usage_and_fixed_error(self):
        real_write = Path.write_text

        def write(path, *args, **kwargs):
            if path.name == "final.txt":
                raise OSError("SECRET_FILESYSTEM_ERROR")
            return real_write(path, *args, **kwargs)

        with patch.object(transport.subprocess, "run", return_value=self.process()) as launch, \
                patch.object(Path, "write_text", write):
            with self.assertRaises(transport.InferenceRunError) as failure:
                self.invoke()
        launch.assert_called_once()
        self.assertNotIn("SECRET_FILESYSTEM_ERROR", str(failure.exception))
        self.assertEqual(self.saved()["usage"], ENVELOPE["usage"])
        self.assertEqual(self.saved()["error"], "response_artifact_failed")
        self.assertEqual(self.saved()["status"], "process_failed")

    def test_request_artifact_failure_prevents_launch(self):
        real_write = Path.write_text

        def write(path, *args, **kwargs):
            if path.name == "request.json":
                raise OSError("SECRET_FILESYSTEM_ERROR")
            return real_write(path, *args, **kwargs)

        with patch.object(transport.subprocess, "run") as launch, patch.object(Path, "write_text", write):
            with self.assertRaises(transport.InferenceRunError):
                self.invoke()
        launch.assert_not_called()
        self.assertEqual(self.saved()["status"], "launch_failed")
        self.assertNotIn("SECRET_FILESYSTEM_ERROR", self.all_artifacts())


if __name__ == "__main__":
    unittest.main()
