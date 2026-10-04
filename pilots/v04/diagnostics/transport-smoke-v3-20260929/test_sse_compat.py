"""Compatibility tests with in-memory responses only."""

import io
import json
import unittest
from unittest.mock import Mock, patch

from reflectai_v04 import gateway
from sse_compat import MAX_PREFIX_BYTES, compatibility_https


def event(kind, **fields):
    return b"data: " + json.dumps({"type": kind, **fields}).encode() + b"\n\n"


FIRST = event("response.created", response={"output": []})
LAST = event("response.completed", response={"output": [{"type": "message"}]})


def fixture(body, headers=None, status=200):
    response = Mock()
    response.status = status
    response.getheader.side_effect = lambda name, default=None: (headers or {}).get(name.lower(), default)
    response.readline.side_effect = io.BytesIO(body).readline
    connection = Mock()
    connection.getresponse.return_value = response
    observations = {}
    factory = Mock(return_value=connection)
    wrapped = compatibility_https(factory, observations, validate_event=gateway._event_kind,
                                  error_type=gateway.GatewayError)("chatgpt.com", timeout=60)
    return wrapped, connection, response, observations


class SseCompatibilityTests(unittest.TestCase):
    def test_valid_missing_mime_replays_prefix_and_remaining_stream_exactly(self):
        body = b": heartbeat\n\n" + FIRST + LAST
        wrapped, _, original, observations = fixture(body)
        response = wrapped.getresponse()
        self.assertEqual(response.getheader("Content-Type"), "text/event-stream")
        self.assertIsNone(original.getheader("Content-Type"))
        self.assertEqual(response.readline(0), b"")
        received = bytearray()
        sizes = (1, 3, 11, 2, 100)
        for index in range(len(body) + 1):
            part = response.readline(sizes[index % len(sizes)])
            if not part:
                break
            self.assertLessEqual(len(part), sizes[index % len(sizes)])
            received.extend(part)
        self.assertEqual(bytes(received), body)
        self.assertEqual(response.readline(), b"")
        self.assertEqual(observations["sse_compatibility"], {
            "mode": "validated_missing_content_type", "bytes_prefetched": len(b": heartbeat\n\n" + FIRST),
            "first_event": "response.created",
        })

    def test_explicit_html_json_or_empty_content_type_never_reads_body(self):
        for mime in ("text/html", "application/json", ""):
            with self.subTest(mime=mime):
                wrapped, _, original, observations = fixture(FIRST, {"content-type": mime})
                self.assertIs(wrapped.getresponse(), original)
                original.readline.assert_not_called()
                self.assertEqual(observations["sse_compatibility"]["mode"], "not_applied")

    def test_comments_empty_or_done_without_json_event_are_rejected(self):
        for body in (b": heartbeat\n\n", b"\n\n", b"data: [DONE]\n\n", b""):
            with self.subTest(body=body):
                wrapped, _, _, observations = fixture(body)
                with self.assertRaises(gateway.GatewayError):
                    wrapped.getresponse()
                self.assertIsNone(observations["sse_compatibility"]["first_event"])

    def test_tool_or_error_as_first_event_is_rejected(self):
        for body in (event("response.output_item.added", item={"type": "function_call", "name": "secret-tool"}),
                     event("response.failed", response={"output": []})):
            with self.subTest(body=body):
                wrapped, _, _, observations = fixture(body)
                with self.assertRaises(gateway.GatewayError):
                    wrapped.getresponse()
                self.assertNotIn("secret-tool", json.dumps(observations))
                self.assertEqual(observations["sse_compatibility"]["mode"], "rejected_missing_content_type")

    def test_json_or_html_without_mime_is_not_relabelled(self):
        for body in (b'{"secret":"private-body"}', b"<html>private-body</html>\n\n" + FIRST):
            with self.subTest(body=body):
                wrapped, _, _, observations = fixture(body)
                with self.assertRaises(gateway.GatewayError):
                    wrapped.getresponse()
                self.assertNotIn("private-body", json.dumps(observations))

    def test_prefix_is_bounded(self):
        wrapped, _, original, observations = fixture(b":" + b"x" * (MAX_PREFIX_BYTES + 1))
        with self.assertRaisesRegex(gateway.GatewayError, "prefix_limit"):
            wrapped.getresponse()
        original.readline.assert_called_once_with(MAX_PREFIX_BYTES)
        self.assertEqual(observations["sse_compatibility"]["bytes_prefetched"], MAX_PREFIX_BYTES)

    def test_compressed_missing_mime_is_rejected_before_body_read(self):
        wrapped, _, original, observations = fixture(FIRST, {"content-encoding": "gzip"})
        with self.assertRaisesRegex(gateway.GatewayError, "nonidentity_encoding"):
            wrapped.getresponse()
        original.readline.assert_not_called()
        self.assertEqual(observations["sse_compatibility"]["bytes_prefetched"], 0)

    def test_timeout_is_bounded_by_factory_timeout(self):
        wrapped, _, original, _ = fixture(FIRST)
        with patch("sse_compat.time.monotonic", side_effect=[100.0, 161.0]):
            with self.assertRaisesRegex(gateway.GatewayError, "probe_timeout"):
                wrapped.getresponse()
        original.readline.assert_not_called()


if __name__ == "__main__":
    unittest.main()
