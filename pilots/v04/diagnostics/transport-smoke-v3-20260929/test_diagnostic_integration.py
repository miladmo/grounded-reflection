"""Scoped diagnostic instrumentation checks without network or model calls."""

from email.message import Message
import http.client
import io
import json
import unittest
from unittest.mock import Mock, patch

from observation import observe_https
from reflectai_v04 import gateway
import run_smoke


class DiagnosticIntegrationTests(unittest.TestCase):
    def test_real_https_constructor_works_without_replacing_stdlib_class(self):
        original_https, original_namespace = http.client.HTTPSConnection, gateway.http
        observations = {}
        factory = observe_https(original_https, observations)
        with patch.object(original_https, "connect", side_effect=AssertionError("No connection permitted")) as connect:
            with run_smoke.shadow_gateway_http(gateway, factory):
                connection = gateway.http.client.HTTPSConnection("chatgpt.com", timeout=2)
                self.assertIs(http.client.HTTPSConnection, original_https)
                self.assertIs(gateway.http.client.HTTPException, http.client.HTTPException)
                self.assertIsNone(connection.sock)
                self.assertEqual(connection.host, "chatgpt.com")
                connection.close()
            connect.assert_not_called()
        self.assertIs(gateway.http, original_namespace)
        self.assertIs(http.client.HTTPSConnection, original_https)
        self.assertEqual(observations, {})

    def test_scoped_namespace_is_restored_after_exception(self):
        original_namespace, original_https = gateway.http, http.client.HTTPSConnection
        with self.assertRaisesRegex(RuntimeError, "local test failure"):
            with run_smoke.shadow_gateway_http(gateway, Mock()):
                self.assertIsNot(gateway.http, original_namespace)
                self.assertIs(http.client.HTTPSConnection, original_https)
                raise RuntimeError("local test failure")
        self.assertIs(gateway.http, original_namespace)
        self.assertIs(http.client.HTTPSConnection, original_https)

    def test_unchanged_gateway_rejects_html_without_recording_secrets(self):
        response = Mock()
        response.status, response.version = 200, 11
        headers = {"content-type": "text/html; private=secret-parameter",
                   "cf-mitigated": "challenge", "via": "secret-proxy", "set-cookie": "secret-cookie"}
        response.getheader.side_effect = lambda name, default=None: headers.get(name.lower(), default)
        upstream = Mock()
        upstream.getresponse.return_value = response
        factory = Mock(return_value=upstream)
        observations = {}
        relay = gateway.Gateway(2)
        body = json.dumps({"stream": True, "input": [], "tools": []}).encode()
        handler = Mock()
        handler.path = relay.path + "/responses"
        handler.rfile, handler.wfile = io.BytesIO(body), io.BytesIO()
        handler.headers = Message()
        for name, value in {"Content-Length": str(len(body)), "Content-Type": "application/json",
                            "Authorization": "Bearer secret-token", "ChatGPT-Account-ID": "secret-account",
                            "Accept": "text/event-stream"}.items():
            handler.headers[name] = value
        original_https = http.client.HTTPSConnection
        with run_smoke.shadow_gateway_http(gateway, observe_https(factory, observations)):
            relay.handle(handler)
        self.assertIs(http.client.HTTPSConnection, original_https)
        factory.assert_called_once_with("chatgpt.com", timeout=2)
        upstream.connect.assert_called_once_with()
        upstream.request.assert_called_once()
        self.assertEqual(relay.summary["upstream_requests"], 1)
        self.assertEqual(relay.summary["upstream_status"], 200)
        self.assertEqual(relay.summary["failure"], "streaming_response_required")
        self.assertFalse(relay.summary["completed"])
        self.assertEqual(observations["response"]["mime"], "text/html")
        self.assertTrue(observations["response"]["cf_mitigated_challenge"])
        self.assertTrue(observations["response"]["via_present"])
        self.assertEqual(observations["request"], {"authorization_present": True,
                         "chatgpt_account_id_present": True, "accept_present": True})
        self.assertNotIn("secret-", json.dumps(observations))
        response.read.assert_not_called()
        response.readline.assert_not_called()
        self.assertEqual(handler.wfile.getvalue(), b"")

    def test_pending_approval_cannot_reserve_a_live_attempt(self):
        with patch.object(run_smoke, "HERE", Mock()):
            with self.assertRaises(ValueError):
                run_smoke.reserve({"approved": None, "reviewer": None, "response": None,
                                   "date": None, "plan_sha256": "pending-plan"}, "pending-plan")


if __name__ == "__main__":
    unittest.main()
