"""No model calls: exercise CLI isolation, event auditing and failure records."""

import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from grounded_reflection.codex_backend import (
    DISABLED_FEATURES, InferenceRunError, run_completion,
)


class CodexBackendTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="reflection-backend-test-")
        self.root = Path(self.temporary.name)
        self.run_dir = self.root / "run"
        self.schema = {"type": "object", "properties": {"answer": {"type": "string"}}}

    def tearDown(self):
        self.temporary.cleanup()

    def invoke(self, **kwargs):
        return run_completion("Use only these fictional task materials.", self.schema,
                              self.run_dir, "test-model", "high", executable="codex-test", **kwargs)

    def events(self, item_type="agent_message", usage=True):
        events = [{"type": "thread.started", "thread_id": "test-thread"},
                  {"type": "turn.started"},
                  {"type": "item.completed", "item": {"type": item_type, "text": "result"}},
                  {"type": "turn.completed"}]
        if usage:
            events[-1]["usage"] = {"input_tokens": 12, "output_tokens": 4}
        return "\n".join(json.dumps(event) for event in events)

    def fake_process(self, *, stdout=None, returncode=0, final='{"answer": "ok"}'):
        def execute(command, **kwargs):
            self.assertFalse(kwargs["shell"])
            self.assertTrue(kwargs["cwd"].is_dir())
            self.assertEqual(list(kwargs["cwd"].iterdir()), [])
            self.assertEqual(command[-1], "-")
            self.assertNotIn(kwargs["input"], command)
            self.assertNotIn("--ignore-rules", command)
            self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)
            if final is not None:
                Path(command[command.index("-o") + 1]).write_text(final, encoding="utf-8")
            return subprocess.CompletedProcess(command, returncode,
                                               self.events() if stdout is None else stdout,
                                               "test diagnostic")
        return execute

    def metadata(self):
        return json.loads((self.run_dir / "metadata.json").read_text(encoding="utf-8"))

    def test_success_records_complete_artifacts_and_isolation_flags(self):
        with patch("grounded_reflection.codex_backend.subprocess.run", side_effect=self.fake_process()) as call:
            result = self.invoke()
        self.assertEqual(result["response"], {"answer": "ok"})
        self.assertEqual(result["metadata"]["usage"]["input_tokens"], 12)
        self.assertEqual(result["metadata"]["status"], "completed")
        self.assertFalse(result["metadata"]["tool_use_detected"])
        self.assertEqual(result["metadata"]["requested_model"], "test-model")
        command = call.call_args.args[0]
        self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
        self.assertIn("--ignore-user-config", command)
        self.assertIn("--ephemeral", command)
        for feature in DISABLED_FEATURES:
            self.assertIn(["--disable", feature], [command[i:i+2] for i in range(len(command)-1)])
        for filename in ["prompt.txt", "response.schema.json", "stdout.jsonl", "stderr.txt", "final.json", "metadata.json"]:
            self.assertTrue((self.run_dir / filename).is_file(), filename)

    def test_existing_nonempty_directory_is_never_overwritten(self):
        self.run_dir.mkdir()
        protected = self.run_dir / "keep.txt"
        protected.write_text("original", encoding="utf-8")
        with patch("grounded_reflection.codex_backend.subprocess.run") as call:
            with self.assertRaises(FileExistsError):
                self.invoke()
        call.assert_not_called()
        self.assertEqual(protected.read_text(encoding="utf-8"), "original")

    def test_empty_preexisting_directory_is_allowed(self):
        self.run_dir.mkdir()
        with patch("grounded_reflection.codex_backend.subprocess.run", side_effect=self.fake_process()):
            self.assertEqual(self.invoke()["metadata"]["status"], "completed")

    def test_command_mcp_web_file_and_unknown_items_are_rejected(self):
        for item_type in ["command_execution", "mcp_tool_call", "web_search", "file_change", "future_tool"]:
            with self.subTest(item_type=item_type):
                self.run_dir = self.root / item_type
                with patch("grounded_reflection.codex_backend.subprocess.run",
                           side_effect=self.fake_process(stdout=self.events(item_type))):
                    with self.assertRaises(InferenceRunError):
                        self.invoke()
                self.assertTrue(self.metadata()["tool_use_detected"])
                self.assertEqual(self.metadata()["status"], "audit_failed")
                self.assertTrue((self.run_dir / "final.json").exists())

    def test_process_failure_preserves_output_without_retry(self):
        with patch("grounded_reflection.codex_backend.subprocess.run",
                   side_effect=self.fake_process(returncode=7, final=None)) as call:
            with self.assertRaises(InferenceRunError):
                self.invoke()
        call.assert_called_once()
        self.assertEqual(self.metadata()["returncode"], 7)
        self.assertEqual(self.metadata()["status"], "process_failed")
        self.assertEqual((self.run_dir / "stderr.txt").read_text(encoding="utf-8"), "test diagnostic")

    def test_timeout_preserves_partial_bytes(self):
        timeout = subprocess.TimeoutExpired(["codex-test"], 1,
                                            output=b'{"type":"turn.started"}\n', stderr=b"partial stderr")
        with patch("grounded_reflection.codex_backend.subprocess.run", side_effect=timeout):
            with self.assertRaises(InferenceRunError):
                self.invoke(timeout_seconds=1)
        self.assertEqual(self.metadata()["status"], "timed_out")
        self.assertEqual((self.run_dir / "stderr.txt").read_text(encoding="utf-8"), "partial stderr")
        self.assertEqual(self.metadata()["event_types"], ["turn.started"])

    def test_missing_usage_is_recorded_as_unavailable(self):
        with patch("grounded_reflection.codex_backend.subprocess.run",
                   side_effect=self.fake_process(stdout=self.events(usage=False))):
            self.assertIsNone(self.invoke()["metadata"]["usage"])

    def test_missing_invalid_and_nonobject_final_response_fail(self):
        for final, folder in [(None, "missing"), ("{bad json", "invalid"), ("[]", "array")]:
            with self.subTest(final=final):
                self.run_dir = self.root / folder
                with patch("grounded_reflection.codex_backend.subprocess.run", side_effect=self.fake_process(final=final)):
                    with self.assertRaises(InferenceRunError):
                        self.invoke()
                self.assertEqual(self.metadata()["status"], "response_failed")

    def test_unknown_event_invalid_json_and_incomplete_turn_fail_closed(self):
        cases = [self.events() + '\n{"type":"future.event"}',
                 self.events() + "\nnot JSON", '{"type":"turn.started"}']
        for number, stdout in enumerate(cases):
            with self.subTest(number=number):
                self.run_dir = self.root / str(number)
                with patch("grounded_reflection.codex_backend.subprocess.run", side_effect=self.fake_process(stdout=stdout)):
                    with self.assertRaises(InferenceRunError):
                        self.invoke()
                self.assertEqual(self.metadata()["status"], "audit_failed")

    def test_launch_error_is_preserved(self):
        with patch("grounded_reflection.codex_backend.subprocess.run", side_effect=FileNotFoundError("missing executable")):
            with self.assertRaises(InferenceRunError):
                self.invoke()
        self.assertEqual(self.metadata()["status"], "launch_failed")
        self.assertIn("FileNotFoundError", self.metadata()["error"])


if __name__ == "__main__":
    unittest.main()
