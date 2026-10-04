"""Transport contract checks without CLI execution or model/API calls."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from reflectai_v04 import transport


SCHEMA = {"type": "object", "properties": {"answer": {"type": "string"}},
          "required": ["answer"], "additionalProperties": False}
SUCCESS_EVENTS = "\n".join(json.dumps(event) for event in (
    {"type": "thread.started"}, {"type": "turn.started"},
    {"type": "item.completed", "item": {"type": "agent_message", "text": "done"}},
    {"type": "turn.completed", "usage": {"input_tokens": 3, "output_tokens": 2}},
))


class V04TransportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="v04-transport-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.cli = self.root / "codex.exe"
        self.cli.write_bytes(b"test binary; never execute")
        self.catalog = self.root / "model-catalog.json"
        self.catalog.write_text(json.dumps({"models": [{"slug": "test-model"}]}), encoding="utf-8")
        self.attestation = {
            "schema_version": 1,
            "cli": {"path": str(self.cli.resolve()), "sha256": transport._sha256(self.cli),
                    "version": "test-cli"},
            "transport_sha256": transport._sha256(Path(transport.__file__)),
            "catalog_sha256": transport._sha256(self.catalog),
            "gateway_sha256": transport._sha256(Path(transport.gateway.__file__)),
            "fixed_arguments": transport.fixed_arguments(self.catalog),
            "allowed_request_tools": [],
            "isolation_check": {
                "passed": True, "checked_at": "2026-09-29",
                "workspace_outside_repository": True,
                "no_filesystem_code_or_network_tools": True,
                "no_request_tools": True,
            },
        }
        self.write_attestation()
        self.directory_patch = patch.object(transport, "TRANSPORT_DIR", self.root)
        self.gateway_patch = patch.object(transport.gateway, "one_request_gateway")
        relay_context = self.gateway_patch.start()
        self.addCleanup(self.gateway_patch.stop)
        self.relay = relay_context.return_value.__enter__.return_value
        self.relay.base_url = "http://127.0.0.1:1234/test-only"
        self.relay.summary = {"upstream_requests": 1, "blocked_requests": 0,
                              "response_events_blocked": 0, "completed": True, "failure": None}
        self.directory_patch.start()
        self.addCleanup(self.directory_patch.stop)

    def write_attestation(self):
        (self.root / "runtime-attestation.json").write_text(json.dumps(self.attestation), encoding="utf-8")

    def run_transport(self, name="run", **kwargs):
        return transport.run_completion("Public prompt only", SCHEMA, self.root / name,
                                        "test-model", "medium", executable=str(self.cli), **kwargs)

    def success(self, command, **kwargs):
        Path(command[command.index("-o") + 1]).write_text('{"answer":"ok"}', encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, SUCCESS_EVENTS, "")

    def test_empty_external_workspace_stdin_and_no_api_environment(self):
        observed = {}

        def complete(command, **kwargs):
            workspace = Path(kwargs["cwd"])
            observed["workspace"] = workspace
            self.assertFalse(any(workspace.iterdir()))
            self.assertFalse(workspace.is_relative_to(self.root))
            self.assertEqual(kwargs["input"], "Public prompt only")
            self.assertFalse(kwargs["shell"])
            self.assertNotIn("OPENAI_API_KEY", kwargs["env"])
            self.assertNotIn("CUSTOM_ACCESS_TOKEN", kwargs["env"])
            self.assertNotIn("OPENAI_BASE_URL", kwargs["env"])
            self.assertEqual(kwargs["env"]["HOME"], "preserved-home")
            self.assertEqual(kwargs["env"]["CODEX_HOME"], "preserved-codex-home")
            schema = Path(command[command.index("--output-schema") + 1])
            self.assertFalse(schema.is_relative_to(workspace))
            self.assertEqual(command[-1], "-")
            return self.success(command, **kwargs)

        with patch.dict(os.environ, {"OPENAI_API_KEY": "do-not-log", "CUSTOM_ACCESS_TOKEN": "private",
                                     "OPENAI_BASE_URL": "https://unused.invalid", "HOME": "preserved-home",
                                     "CODEX_HOME": "preserved-codex-home"}), \
                patch.object(transport.subprocess, "run", side_effect=complete) as launch:
            result = self.run_transport()
        launch.assert_called_once()
        self.assertFalse(observed["workspace"].exists())
        self.assertEqual(result["response"], {"answer": "ok"})
        serialized = json.dumps(result["metadata"])
        self.assertNotIn("do-not-log", serialized)
        self.assertIn("OPENAI_API_KEY", result["metadata"]["removed_environment_variables"])

    def test_hash_or_capability_mismatch_rejects_before_spawn(self):
        mutations = (
            ("catalog_sha256", "bad"), ("gateway_sha256", "bad"), ("transport_sha256", "bad"),
            ("fixed_arguments", []), ("allowed_request_tools", ["shell"]),
            ("isolation_check", {"passed": True}),
            ("cli", {"path": str(self.cli), "sha256": "bad", "version": "test"}),
        )
        for index, (field, value) in enumerate(mutations):
            with self.subTest(field=field):
                original = self.attestation[field]
                self.attestation[field] = value
                self.write_attestation()
                with patch.object(transport.subprocess, "run") as launch:
                    with self.assertRaises(transport.InferenceRunError):
                        self.run_transport(f"mismatch-{index}")
                    launch.assert_not_called()
                self.attestation[field] = original

    def test_missing_attestation_rejects_before_spawn(self):
        (self.root / "runtime-attestation.json").unlink()
        with patch.object(transport.subprocess, "run") as launch:
            with self.assertRaises(transport.InferenceRunError):
                self.run_transport()
            launch.assert_not_called()

    def test_temporary_directory_inside_repository_is_rejected(self):
        repository_subdirectory = Path(transport.__file__).resolve().parent
        with patch.object(transport.tempfile, "TemporaryDirectory") as temporary, \
                patch.object(transport.subprocess, "run") as launch:
            temporary.return_value.__enter__.return_value = str(repository_subdirectory)
            with self.assertRaises(transport.InferenceRunError):
                self.run_transport()
            launch.assert_not_called()

    def test_cli_update_invalidates_cached_binary_hash(self):
        with patch.object(transport.subprocess, "run", side_effect=self.success) as launch:
            self.run_transport("before-update")
            self.cli.write_bytes(b"updated binary with a different length")
            with self.assertRaises(transport.InferenceRunError):
                self.run_transport("after-update")
        self.assertEqual(launch.call_count, 1)

    def test_unknown_model_fails_before_spawn(self):
        with patch.object(transport.subprocess, "run") as launch:
            with self.assertRaises(transport.InferenceRunError):
                transport.run_completion("prompt", SCHEMA, self.root / "other-model", "unattested-model",
                                         "medium", executable=str(self.cli))
            launch.assert_not_called()

    def test_provider_retry_and_tool_capabilities_are_explicit(self):
        arguments = transport.fixed_arguments(self.catalog)
        for setting in ('model_provider="reflectai_codex"', 'model_providers.reflectai_codex.name="OpenAI"',
                        'model_providers.reflectai_codex.wire_api="responses"',
                        "model_providers.reflectai_codex.requires_openai_auth=true",
                        "model_providers.reflectai_codex.supports_websockets=false",
                        "model_providers.reflectai_codex.request_max_retries=0",
                        "model_providers.reflectai_codex.stream_max_retries=0",
                        "project_doc_max_bytes=0",
                        "tools.experimental_request_user_input={enabled=false}"):
            self.assertIn(setting, arguments)
        for feature in ("shell_tool", "code_mode", "goals", "view_image", "multi_agent_v2"):
            index = arguments.index(feature)
            self.assertEqual(arguments[index - 1], "--disable")

    def test_prohibited_event_is_rejected_and_artifacts_preserved(self):
        def prohibited(command, **kwargs):
            self.success(command, **kwargs)
            event = json.dumps({"type": "item.completed", "item": {"type": "command_execution"}})
            return subprocess.CompletedProcess(command, 0, event + "\n" + SUCCESS_EVENTS, "")

        with patch.object(transport.subprocess, "run", side_effect=prohibited) as launch:
            with self.assertRaises(transport.InferenceRunError):
                self.run_transport()
        launch.assert_called_once()
        metadata = json.loads((self.root / "run" / "metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["status"], "audit_failed")
        self.assertTrue(metadata["tool_use_detected"])
        self.assertTrue((self.root / "run" / "stdout.jsonl").exists())

    def test_timeout_and_process_failure_never_retry(self):
        for name, failure in (("timeout", subprocess.TimeoutExpired("codex", 10, output=b"")),
                              ("exit", subprocess.CompletedProcess([], 1, "", "test failure"))):
            with self.subTest(name=name):
                effect = failure if isinstance(failure, Exception) else lambda *args, **kwargs: failure
                with patch.object(transport.subprocess, "run", side_effect=effect) as launch:
                    with self.assertRaises(transport.InferenceRunError):
                        self.run_transport(name)
                launch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
