"""One-request loopback relay to the fixed ChatGPT Codex Responses endpoint.

No retries, redirects, credentials, request bodies or response bodies are stored.
The relay rejects advertised tools and withholds response tool events from the
CLI. Authentication headers are forwarded only to the pinned HTTPS endpoint.
"""

from contextlib import contextmanager
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import secrets
import socket
import threading
import time


UPSTREAM_HOST = "chatgpt.com"
UPSTREAM_PATH = "/backend-api/codex/responses"
MAX_BYTES = 16 * 1024 * 1024
_HOP_HEADERS = frozenset({
    "host", "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "proxy-connection", "te", "trailer", "transfer-encoding", "upgrade",
    "content-length", "content-encoding", "accept-encoding",
})


class GatewayError(ValueError):
    """A fixed, nonsensitive rejection reason safe to include in metadata."""


def _event_kind(frame: bytes) -> str | None:
    """Validate an SSE frame before releasing it to the CLI."""
    data = b"\n".join(line[5:].lstrip() for line in frame.splitlines() if line.startswith(b"data:"))
    if not data or data == b"[DONE]":
        return None
    value = json.loads(data)
    kind = value.get("type", "")
    basic = {"response.created", "response.in_progress", "response.completed",
             "response.incomplete", "response.failed", "error", "rate_limits.updated"}
    prefixes = ("response.output_text.", "response.refusal.", "response.content_part.",
                "response.reasoning_text.", "response.reasoning_summary_text.",
                "response.reasoning_summary_part.", "response.output_item.")
    if kind not in basic and not kind.startswith(prefixes):
        raise GatewayError("unsupported_response_event")
    items = []
    if kind.startswith("response.output_item."):
        items.append(value.get("item", {}))
    if isinstance(value.get("response"), dict):
        items.extend(value["response"].get("output", []))
    if any(not isinstance(item, dict) or item.get("type") not in {"message", "reasoning"}
           for item in items):
        raise GatewayError("response_tool_item")
    if kind in {"error", "response.failed", "response.incomplete"}:
        raise GatewayError("upstream_response_failed")
    return kind


class Gateway:
    def __init__(self, timeout_seconds: int):
        if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, int) or timeout_seconds <= 0:
            raise GatewayError("timeout_seconds must be a positive integer")
        self.timeout_seconds = timeout_seconds
        self.path = "/" + secrets.token_urlsafe(24)
        self.base_url = ""
        self._lock = threading.Lock()
        self._closed = False
        self._upstream = None
        self._upstream_socket = None
        self._clients = set()
        self._summary = {"received_model_posts": 0, "upstream_requests": 0,
                         "blocked_requests": 0, "response_events_blocked": 0,
                         "upstream_status": None, "completed": False, "failure": None}

    @property
    def summary(self) -> dict:
        with self._lock:
            return dict(self._summary)

    def _fail(self, reason: str) -> None:
        with self._lock:
            self._summary["failure"] = self._summary["failure"] or reason

    def handle(self, handler) -> None:
        if handler.path != self.path + "/responses":
            handler.send_error(404, "Unknown local route")
            return
        with self._lock:
            self._summary["received_model_posts"] += 1
            rejected = self._closed or self._summary["received_model_posts"] != 1
            if rejected:
                self._summary["blocked_requests"] += 1
                self._summary["failure"] = self._summary["failure"] or "additional_request_blocked"
            else:
                self._clients.add(handler.connection)
        if rejected:
            handler.send_error(409, "Only one upstream request is permitted")
            return
        started = False
        connection = None
        try:
            handler.connection.settimeout(self.timeout_seconds)
            length = int(handler.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_BYTES or handler.headers.get("Transfer-Encoding"):
                raise GatewayError("invalid_request_length")
            raw = handler.rfile.read(length)
            if len(raw) != length:
                raise GatewayError("incomplete_request_body")
            encoding = handler.headers.get("Content-Encoding", "identity").lower()
            if encoding != "identity":
                raise GatewayError("request_compression_must_be_disabled")
            body = json.loads(raw)
            if not isinstance(body, dict) or body.get("stream") is not True:
                raise GatewayError("streaming_responses_request_required")
            additional_tools = any(isinstance(item, dict) and item.get("type") == "additional_tools"
                                   and item.get("tools") for item in body.get("input", []))
            if body.get("tools") or additional_tools:
                raise GatewayError("advertised_tools_blocked")
            hop = _HOP_HEADERS | {item.strip().lower() for item in handler.headers.get("Connection", "").split(",")}
            headers = {key: value for key, value in handler.headers.items() if key.lower() not in hop}
            headers["Accept-Encoding"] = "identity"
            connection = http.client.HTTPSConnection(UPSTREAM_HOST, timeout=self.timeout_seconds)
            with self._lock:
                if self._closed:
                    raise GatewayError("gateway_closed")
                self._upstream = connection
            deadline = time.monotonic() + self.timeout_seconds
            connection.connect()
            with self._lock:
                if self._closed:
                    raise GatewayError("gateway_closed")
                self._upstream_socket = connection.sock
                self._summary["upstream_requests"] += 1
            connection.request("POST", UPSTREAM_PATH, body=raw, headers=headers)
            response = connection.getresponse()
            with self._lock:
                self._summary["upstream_status"] = response.status
            if response.status != 200:
                self._fail("upstream_http_error")
                handler.send_error(response.status if 400 <= response.status <= 599 else 502,
                                   "Upstream request failed; no retry")
                return
            if not response.getheader("Content-Type", "").lower().startswith("text/event-stream"):
                raise GatewayError("streaming_response_required")
            if response.getheader("Content-Encoding", "identity").lower() != "identity":
                raise GatewayError("compressed_response_rejected")
            handler.send_response(200)
            handler.send_header("Content-Type", "text/event-stream")
            handler.send_header("Connection", "close")
            handler.end_headers()
            handler.close_connection = True
            started = True
            frame = bytearray()
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("gateway_deadline")
                if self._upstream_socket is not None:
                    self._upstream_socket.settimeout(remaining)
                line = response.readline(MAX_BYTES + 1)
                if not line:
                    if frame:
                        raise GatewayError("truncated_sse_frame")
                    break
                frame.extend(line)
                if len(frame) > MAX_BYTES:
                    raise GatewayError("oversized_sse_frame")
                if line in (b"\n", b"\r\n"):
                    try:
                        kind = _event_kind(bytes(frame))
                    except (ValueError, TypeError, AttributeError):
                        with self._lock:
                            self._summary["response_events_blocked"] += 1
                        raise GatewayError("response_event_rejected") from None
                    handler.wfile.write(frame)
                    handler.wfile.flush()
                    if kind == "response.completed":
                        with self._lock:
                            self._summary["completed"] = True
                        break
                    frame.clear()
            if not self.summary["completed"]:
                raise GatewayError("missing_response_completed")
        except (OSError, ValueError, TypeError, AttributeError, http.client.HTTPException) as exc:
            self._fail(str(exc) if isinstance(exc, GatewayError) else type(exc).__name__)
            with self._lock:
                if self._summary["upstream_requests"] == 0:
                    self._summary["blocked_requests"] += 1
            if not started:
                handler.send_error(502, "Local transport rejected the request or upstream response")
            handler.close_connection = True
        finally:
            if connection is not None:
                connection.close()
            with self._lock:
                self._clients.discard(handler.connection)
                self._upstream = None
                self._upstream_socket = None

    def close(self) -> None:
        with self._lock:
            self._closed = True
            sockets = [*self._clients, self._upstream_socket]
            upstream = self._upstream
        for connection in sockets:
            if connection is not None:
                try:
                    connection.shutdown(socket.SHUT_RDWR)
                    connection.close()
                except OSError:
                    pass
        if upstream is not None:
            upstream.close()


@contextmanager
def one_request_gateway(timeout_seconds: int = 420):
    gateway = Gateway(timeout_seconds)

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(gateway.timeout_seconds)
            with gateway._lock:
                if gateway._closed:
                    self.connection.close()
                    raise ConnectionAbortedError("Gateway closed")
                gateway._clients.add(self.connection)

        def finish(self):
            try:
                super().finish()
            finally:
                with gateway._lock:
                    gateway._clients.discard(self.connection)

        def log_message(self, *args):
            pass

        def do_POST(self):
            gateway.handle(self)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    server.block_on_close = False
    gateway.base_url = f"http://127.0.0.1:{server.server_address[1]}{gateway.path}"
    worker = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    worker.start()
    try:
        yield gateway
    finally:
        gateway.close()
        server.shutdown()
        server.server_close()
        worker.join(timeout=1)
