"""Offline observation checks without sockets, CLI processes or model calls."""

import json
import unittest
from unittest.mock import Mock

from observation import observe_https


def connection(headers, status=200):
    response = Mock()
    response.status, response.version = status, 11
    response.getheader.side_effect = lambda name, default=None: headers.get(name.lower(), default)
    wrapped = Mock()
    wrapped.getresponse.return_value = response
    return wrapped, response


class ObservationTests(unittest.TestCase):
    def test_normal_sse_only_records_safe_metadata_without_reading_body(self):
        original, response = connection({"content-type": "text/event-stream; charset=utf-8",
                                         "content-encoding": "identity"})
        observations = {}
        observed = observe_https(Mock(return_value=original), observations)("chatgpt.com")
        self.assertIs(observed.getresponse(), response)
        self.assertEqual(observations["response"], {
            "status": 200, "mime": "text/event-stream", "content_encoding": "identity",
            "http_version": 11, "cf_mitigated_challenge": False, "via_present": False,
        })
        response.read.assert_not_called()
        response.readline.assert_not_called()
        response.read1.assert_not_called()

    def test_http_200_html_and_json_are_observed_without_changing_response(self):
        for mime in ("text/html", "application/json"):
            with self.subTest(mime=mime):
                original, response = connection({"content-type": mime, "cf-mitigated": "challenge"})
                observations = {}
                observed = observe_https(Mock(return_value=original), observations)("chatgpt.com")
                self.assertIs(observed.getresponse(), response)
                self.assertEqual(observations["response"]["status"], 200)
                self.assertEqual(observations["response"]["mime"], mime)
                self.assertTrue(observations["response"]["cf_mitigated_challenge"])

    def test_secrets_and_header_values_are_not_serialized(self):
        original, response = connection({
            "content-type": "application/json; private=secret-mime-parameter",
            "content-encoding": "secret-encoding", "via": "secret-internal-proxy",
            "set-cookie": "secret-cookie", "cf-mitigated": "secret-status",
        })
        observations = {}
        observed = observe_https(Mock(return_value=original), observations)("chatgpt.com")
        observed.request("POST", "/responses", headers={
            "AUTHORIZATION": "Bearer secret-token", "ChatGPT-Account-ID": "secret-account",
            "Accept": "secret-accept-value", "Cookie": "secret-request-cookie",
        })
        observed.getresponse()
        serialized = json.dumps(observations)
        self.assertNotIn("secret-", serialized)
        self.assertEqual(observations["request"], {
            "authorization_present": True, "chatgpt_account_id_present": True, "accept_present": True,
        })
        self.assertEqual(observations["response"]["content_encoding"], "other")
        self.assertTrue(observations["response"]["via_present"])

    def test_constructor_request_and_response_arguments_are_unchanged(self):
        original, response = connection({})
        factory, observations = Mock(return_value=original), {}
        context = object()
        observed = observe_https(factory, observations)("chatgpt.com", 443, timeout=27, context=context)
        factory.assert_called_once_with("chatgpt.com", 443, timeout=27, context=context)
        body, headers = b"body untouched", {"Authorization": "secret"}
        result = observed.request("POST", "/backend-api/codex/responses", body, headers, encode_chunked=False)
        original.request.assert_called_once_with("POST", "/backend-api/codex/responses", body, headers,
                                                 encode_chunked=False)
        self.assertIs(result, original.request.return_value)
        self.assertIs(original.request.call_args.args[3], headers)
        self.assertIs(observed.getresponse(), response)
        original.getresponse.assert_called_once_with()

    def test_socket_and_other_attributes_delegate_to_original(self):
        original, _ = connection({})
        original.sock, original.host = object(), "chatgpt.com"
        observed = observe_https(Mock(return_value=original), {})("chatgpt.com")
        self.assertIs(observed.sock, original.sock)
        self.assertEqual(observed.host, original.host)
        observed.connect()
        observed.close()
        original.connect.assert_called_once_with()
        original.close.assert_called_once_with()

    def test_missing_or_unrecognised_headers_stay_coarse(self):
        for headers, expected in (({}, "missing"), ({"content-type": "private/example"}, "other")):
            with self.subTest(headers=headers):
                original, _ = connection(headers)
                observations = {}
                observed = observe_https(Mock(return_value=original), observations)("chatgpt.com")
                observed.request("POST", "/responses")
                observed.getresponse()
                self.assertEqual(observations["response"]["mime"], expected)
                self.assertEqual(observations["response"]["content_encoding"], "missing")
                self.assertFalse(any(observations["request"].values()))


if __name__ == "__main__":
    unittest.main()
