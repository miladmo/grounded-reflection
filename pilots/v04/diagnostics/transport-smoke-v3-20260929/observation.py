"""Header-only observation for a separately authorised transport diagnostic.

The wrapper neither reads response bodies nor changes connection arguments,
routing or gateway acceptance rules. Only booleans, enums and integers are kept.
"""


def _enum_header(value, allowed):
    if not isinstance(value, str) or not value.strip():
        return "missing"
    normalised = value.strip().lower()
    return normalised if normalised in allowed else "other"


def observe_https(factory, observations):
    """Wrap an HTTPSConnection factory and fill a caller-owned summary dict."""
    class ObservedConnection:
        def __init__(self, connection):
            self._connection = connection

        def __getattr__(self, name):
            return getattr(self._connection, name)

        def request(self, *args, **kwargs):
            headers = args[3] if len(args) > 3 else kwargs.get("headers", {})
            names = {key.lower() for key in (headers or {}) if isinstance(key, str)}
            observations["request"] = {
                "authorization_present": "authorization" in names,
                "chatgpt_account_id_present": "chatgpt-account-id" in names,
                "accept_present": "accept" in names,
            }
            return self._connection.request(*args, **kwargs)

        def getresponse(self, *args, **kwargs):
            response = self._connection.getresponse(*args, **kwargs)
            content_type = response.getheader("Content-Type")
            mime = content_type.split(";", 1)[0] if isinstance(content_type, str) else None
            mitigated = response.getheader("CF-Mitigated")
            observations["response"] = {
                "status": response.status if type(response.status) is int else None,
                "content_type_present": content_type is not None,
                "mime": _enum_header(mime, {"text/html", "application/json", "text/event-stream"}),
                "content_encoding": _enum_header(response.getheader("Content-Encoding"),
                                                  {"identity", "gzip", "br", "deflate", "zstd"}),
                "http_version": response.version if type(response.version) is int else None,
                "cf_mitigated_challenge": isinstance(mitigated, str) and mitigated.strip().lower() == "challenge",
                "via_present": response.getheader("Via") is not None,
            }
            return response

    def observed_factory(*args, **kwargs):
        return ObservedConnection(factory(*args, **kwargs))

    return observed_factory
