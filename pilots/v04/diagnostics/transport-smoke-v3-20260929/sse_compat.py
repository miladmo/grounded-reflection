"""Diagnostic compatibility for a missing MIME header on validated SSE only.

The existing gateway still validates every event. Explicit content types stay
unchanged. Prefetched bytes are replayed through the gateway's readline API.
"""

import io
import math
import time


MAX_PREFIX_BYTES = 64 * 1024
_NAMED_EVENTS = frozenset({"response.created", "response.in_progress", "response.completed",
                         "rate_limits.updated"})
_EVENT_FAMILIES = ("response.output_item.", "response.output_text.", "response.refusal.",
                   "response.content_part.", "response.reasoning_text.",
                   "response.reasoning_summary_text.", "response.reasoning_summary_part.")


def _event_label(kind):
    if kind in _NAMED_EVENTS:
        return kind
    return next((prefix[:-1] for prefix in _EVENT_FAMILIES if kind.startswith(prefix)),
                "other_recognized_event")


class _ReplayedResponse:
    def __init__(self, response, prefix):
        self._response, self._prefix = response, io.BytesIO(prefix)

    def __getattr__(self, name):
        return getattr(self._response, name)

    def getheader(self, name, default=None):
        if name.lower() == "content-type":
            return "text/event-stream"
        return self._response.getheader(name, default)

    def readline(self, size=-1):
        part = self._prefix.readline(size)
        if part.endswith(b"\n") or (size >= 0 and len(part) >= size):
            return part
        remaining = -1 if size < 0 else size - len(part)
        return part + self._response.readline(remaining)


def compatibility_https(factory, observations, *, validate_event, error_type):
    """Return a factory wrapper; no connection is made by this function."""
    class CompatibleConnection:
        def __init__(self, connection, timeout):
            self._connection, self._timeout = connection, timeout

        def __getattr__(self, name):
            return getattr(self._connection, name)

        def getresponse(self, *args, **kwargs):
            deadline = time.monotonic() + self._timeout
            sock = self._connection.sock
            response = self._connection.getresponse(*args, **kwargs)
            record = {"mode": "not_applied", "bytes_prefetched": 0, "first_event": None}
            observations["sse_compatibility"] = record
            if response.status != 200 or response.getheader("Content-Type") is not None:
                return response
            record["mode"] = "rejected_missing_content_type"
            encoding = response.getheader("Content-Encoding")
            if encoding is not None and (not isinstance(encoding, str) or encoding.strip().lower() != "identity"):
                raise error_type("missing_mime_nonidentity_encoding")
            prefix, frame = bytearray(), bytearray()
            while True:
                remaining_time = deadline - time.monotonic()
                if remaining_time <= 0:
                    raise error_type("missing_mime_probe_timeout")
                if sock is not None:
                    sock.settimeout(remaining_time)
                remaining_bytes = MAX_PREFIX_BYTES - len(prefix)
                if remaining_bytes <= 0:
                    raise error_type("missing_mime_prefix_limit")
                line = response.readline(remaining_bytes)
                prefix.extend(line)
                record["bytes_prefetched"] = len(prefix)
                if len(prefix) > MAX_PREFIX_BYTES:
                    raise error_type("missing_mime_prefix_limit")
                if not line:
                    raise error_type("missing_mime_no_valid_sse_event")
                if not line.startswith((b":", b"data:", b"event:", b"id:", b"retry:")) and line not in (b"\n", b"\r\n"):
                    raise error_type("missing_mime_invalid_sse_prefix")
                frame.extend(line)
                if line not in (b"\n", b"\r\n"):
                    continue
                kind = validate_event(bytes(frame))
                if kind is not None:
                    record.update(mode="validated_missing_content_type", first_event=_event_label(kind))
                    return _ReplayedResponse(response, bytes(prefix))
                data = b"\n".join(item[5:].strip() for item in frame.splitlines() if item.startswith(b"data:"))
                if data == b"[DONE]":
                    raise error_type("missing_mime_no_valid_sse_event")
                frame.clear()

    def compatible_factory(*args, **kwargs):
        timeout = kwargs.get("timeout", args[2] if len(args) > 2 else 60)
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
            timeout = 60
        return CompatibleConnection(factory(*args, **kwargs), timeout)

    return compatible_factory
