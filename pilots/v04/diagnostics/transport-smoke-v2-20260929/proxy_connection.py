"""Use the existing HTTP proxy for a TLS tunnel, without changing proxy settings."""
from urllib.parse import urlsplit
import urllib.request


def proxy_https(factory, observations):
    def connect(host, *, timeout):
        if host != 'chatgpt.com':
            raise ValueError('Unexpected diagnostic destination')
        proxies = urllib.request.getproxies()
        proxy = proxies.get('https') or proxies.get('all')
        bypass = urllib.request.proxy_bypass(host)
        observations['network_route'] = {
            'https_proxy_configured': bool(proxy), 'destination_bypassed': bypass,
            'route': 'configured_proxy' if proxy and not bypass else 'direct_by_environment',
        }
        if not proxy or bypass:
            return factory(host, timeout=timeout)
        parsed = urlsplit(proxy)
        if parsed.scheme != 'http' or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('Diagnostic supports only the configured HTTP proxy without credentials')
        if parsed.path not in ('', '/') or parsed.query or parsed.fragment:
            raise ValueError('Unsupported proxy URL components')
        connection = factory(parsed.hostname, parsed.port or 80, timeout=timeout)
        connection.set_tunnel(host, 443)
        return connection
    return connect
