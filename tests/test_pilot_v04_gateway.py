"""Offline gateway tests. No sockets, CLI processes or model requests are used."""

from email.message import Message
import io
import json
import unittest
from unittest.mock import Mock, patch

from reflectai_v04 import gateway


def frame(value):
    return b"data: " + json.dumps(value).encode() + b"\n\n"


SUCCESS = frame({"type": "response.created", "response": {"output": []}}) + frame({
    "type": "response.completed", "response": {"output": [{"type": "message"}]},
})


def request(relay, body=None, headers=None):
    raw = json.dumps(body if body is not None else {"stream": True, "input": [], "tools": []}).encode()
    handler = Mock()
    handler.path = relay.path + "/responses"
    handler.rfile, handler.wfile = io.BytesIO(raw), io.BytesIO()
    handler.headers = Message()
    for key, value in {"Content-Length": str(len(raw)), "Content-Type": "application/json",
                       "Authorization": "Bearer secret-auth", "Host": "127.0.0.1",
                       **(headers or {})}.items():
        handler.headers[key] = value
    return handler


def upstream(stream=SUCCESS, status=200):
    response = Mock()
    response.status = status
    response.getheader.side_effect = lambda key, default="": {
        "Content-Type": "text/event-stream", "Content-Encoding": "identity",
    }.get(key, default)
    response.readline.side_effect = io.BytesIO(stream).readline
    connection = Mock()
    connection.getresponse.return_value = response
    return connection


class GatewayTests(unittest.TestCase):
    def test_one_streamed_request_to_pinned_https_endpoint(self):
        relay, connection = gateway.Gateway(20), upstream()
        handler = request(relay)
        with patch.object(gateway.http.client, "HTTPSConnection", return_value=connection) as factory:
            relay.handle(handler)
        factory.assert_called_once_with("chatgpt.com", timeout=20)
        connection.request.assert_called_once()
        args, kwargs = connection.request.call_args
        self.assertEqual(args, ("POST", "/backend-api/codex/responses"))
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer secret-auth")
        self.assertNotIn("Host", kwargs["headers"])
        self.assertEqual(kwargs["headers"]["Accept-Encoding"], "identity")
        self.assertEqual(handler.wfile.getvalue(), SUCCESS)
        self.assertTrue(relay.summary["completed"])
        self.assertIsNone(relay.summary["failure"])
        self.assertNotIn("secret-auth", json.dumps(relay.summary))
        connection.close.assert_called_once()

    def test_second_request_is_blocked_before_upstream(self):
        relay, connection = gateway.Gateway(20), upstream()
        with patch.object(gateway.http.client, "HTTPSConnection", return_value=connection) as factory:
            relay.handle(request(relay))
            second = request(relay)
            relay.handle(second)
        factory.assert_called_once()
        connection.request.assert_called_once()
        second.send_error.assert_called_once_with(409, "Only one upstream request is permitted")
        self.assertEqual(relay.summary["received_model_posts"], 2)
        self.assertEqual(relay.summary["upstream_requests"], 1)
        self.assertEqual(relay.summary["blocked_requests"], 1)
        self.assertEqual(relay.summary["failure"], "additional_request_blocked")

    def test_completed_event_ends_stream_without_touching_closed_socket(self):
        relay, connection = gateway.Gateway(20), upstream()
        reader = io.BytesIO(SUCCESS)
        closed = False

        def line(size):
            nonlocal closed
            value = reader.readline(size)
            if reader.tell() == len(SUCCESS):
                closed = True
            return value

        def set_timeout(seconds):
            if closed:
                raise OSError("upstream socket already closed at terminal event")

        connection.getresponse.return_value.readline.side_effect = line
        connection.sock.settimeout.side_effect = set_timeout
        with patch.object(gateway.http.client, "HTTPSConnection", return_value=connection):
            relay.handle(request(relay))
        self.assertTrue(relay.summary["completed"])
        self.assertIsNone(relay.summary["failure"])

    def test_advertised_tools_are_rejected_in_both_locations(self):
        for body in ({"stream": True, "tools": [{"type": "function", "name": "read_file"}]},
                     {"stream": True, "input": [{"type": "additional_tools", "tools": [{"name": "exec"}]}]}):
            with self.subTest(body=body):
                relay = gateway.Gateway(20)
                with patch.object(gateway.http.client, "HTTPSConnection") as factory:
                    relay.handle(request(relay, body))
                factory.assert_not_called()
                self.assertEqual(relay.summary["blocked_requests"], 1)
                self.assertEqual(relay.summary["failure"], "advertised_tools_blocked")

    def test_unadvertised_tool_event_never_reaches_cli(self):
        for item_type in ("function_call", "custom_tool_call", "web_search_call"):
            with self.subTest(item_type=item_type):
                relay = gateway.Gateway(20)
                created = frame({"type": "response.created", "response": {"output": []}})
                tool = frame({"type": "response.output_item.added", "item": {"type": item_type,
                              "name": "request_user_input", "arguments": "must not be dispatched"}})
                handler = request(relay)
                with patch.object(gateway.http.client, "HTTPSConnection", return_value=upstream(created + tool)):
                    relay.handle(handler)
                self.assertEqual(handler.wfile.getvalue(), created)
                self.assertEqual(relay.summary["response_events_blocked"], 1)
                self.assertFalse(relay.summary["completed"])
                self.assertEqual(relay.summary["failure"], "response_event_rejected")

    def test_tool_hidden_in_completed_response_is_rejected(self):
        relay = gateway.Gateway(20)
        stream = frame({"type": "response.completed", "response": {"output": [{"type": "function_call"}]}})
        handler = request(relay)
        with patch.object(gateway.http.client, "HTTPSConnection", return_value=upstream(stream)):
            relay.handle(handler)
        self.assertEqual(handler.wfile.getvalue(), b"")
        self.assertFalse(relay.summary["completed"])

    def test_http_error_and_redirect_do_not_retry_or_follow(self):
        for status in (503, 307):
            with self.subTest(status=status):
                relay, connection = gateway.Gateway(20), upstream(status=status)
                with patch.object(gateway.http.client, "HTTPSConnection", return_value=connection) as factory:
                    relay.handle(request(relay))
                factory.assert_called_once()
                connection.request.assert_called_once()
                self.assertEqual(relay.summary["upstream_status"], status)
                self.assertEqual(relay.summary["failure"], "upstream_http_error")

    def test_malformed_or_incomplete_stream_is_not_completed(self):
        streams = (b"data: {invalid}\n\n", b"data: {}", frame({"type": "response.created"}),
                   frame({"type": "response.function_call_arguments.delta", "delta": "hidden"}))
        for stream in streams:
            with self.subTest(stream=stream):
                relay = gateway.Gateway(20)
                with patch.object(gateway.http.client, "HTTPSConnection", return_value=upstream(stream)):
                    relay.handle(request(relay))
                self.assertFalse(relay.summary["completed"])
                self.assertIsNotNone(relay.summary["failure"])

    def test_compressed_request_is_rejected_before_upstream(self):
        relay = gateway.Gateway(20)
        with patch.object(gateway.http.client, "HTTPSConnection") as factory:
            relay.handle(request(relay, headers={"Content-Encoding": "zstd"}))
        factory.assert_not_called()
        self.assertEqual(relay.summary["failure"], "request_compression_must_be_disabled")

    def test_close_during_connect_prevents_late_post(self):
        relay, connection = gateway.Gateway(20), upstream()
        connection.connect.side_effect = relay.close
        with patch.object(gateway.http.client, "HTTPSConnection", return_value=connection):
            relay.handle(request(relay))
        connection.request.assert_not_called()
        self.assertEqual(relay.summary["upstream_requests"], 0)
        self.assertEqual(relay.summary["failure"], "gateway_closed")

    def test_context_manager_closes_server_even_on_failure(self):
        with patch.object(gateway, "ThreadingHTTPServer") as server_class, \
                patch.object(gateway.threading, "Thread") as thread_class:
            server_class.return_value.server_address = ("127.0.0.1", 12345)
            with self.assertRaisesRegex(RuntimeError, "test error"):
                with gateway.one_request_gateway(20) as relay:
                    self.assertTrue(relay.base_url.startswith("http://127.0.0.1:12345/"))
                    raise RuntimeError("test error")
            server_class.return_value.shutdown.assert_called_once()
            server_class.return_value.server_close.assert_called_once()
            thread_class.return_value.join.assert_called_once_with(timeout=1)
            self.assertTrue(relay._closed)


if __name__ == "__main__":
    unittest.main()
