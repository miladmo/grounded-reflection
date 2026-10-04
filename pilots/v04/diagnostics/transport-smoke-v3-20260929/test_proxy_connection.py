import unittest
from unittest.mock import Mock, patch
from proxy_connection import proxy_https


class ProxyConnectionTests(unittest.TestCase):
    def test_existing_http_proxy_is_used_with_tls_tunnel(self):
        factory, observations = Mock(), {}
        with patch('proxy_connection.urllib.request.getproxies', return_value={'https': 'http://127.0.0.1:18080'}), \
                patch('proxy_connection.urllib.request.proxy_bypass', return_value=False):
            result = proxy_https(factory, observations)('chatgpt.com', timeout=60)
        factory.assert_called_once_with('127.0.0.1', 18080, timeout=60)
        result.set_tunnel.assert_called_once_with('chatgpt.com', 443)
        self.assertEqual(observations['network_route']['route'], 'configured_proxy')

    def test_environment_exclusion_is_respected(self):
        factory, observations = Mock(), {}
        with patch('proxy_connection.urllib.request.getproxies', return_value={'https': 'http://127.0.0.1:18080'}), \
                patch('proxy_connection.urllib.request.proxy_bypass', return_value=True):
            result = proxy_https(factory, observations)('chatgpt.com', timeout=60)
        factory.assert_called_once_with('chatgpt.com', timeout=60)
        result.set_tunnel.assert_not_called()

    def test_unsupported_proxy_fails_without_direct_fallback(self):
        for proxy in ('socks5://localhost:123', 'https://localhost:123',
                      'http://user:secret@localhost:123', 'http://localhost/path'):
            with self.subTest(proxy=proxy):
                factory = Mock()
                with patch('proxy_connection.urllib.request.getproxies', return_value={'https': proxy}), \
                        patch('proxy_connection.urllib.request.proxy_bypass', return_value=False):
                    with self.assertRaises(ValueError):
                        proxy_https(factory, {})('chatgpt.com', timeout=60)
                factory.assert_not_called()

    def test_no_second_connection_or_retry_on_proxy_error(self):
        factory = Mock(side_effect=OSError('fixture connection failed'))
        with patch('proxy_connection.urllib.request.getproxies', return_value={'https': 'http://localhost:123'}), \
                patch('proxy_connection.urllib.request.proxy_bypass', return_value=False):
            with self.assertRaises(OSError):
                proxy_https(factory, {})('chatgpt.com', timeout=60)
        factory.assert_called_once()

    def test_other_destination_is_rejected(self):
        factory = Mock()
        with self.assertRaises(ValueError):
            proxy_https(factory, {})('unapproved.invalid', timeout=60)
        factory.assert_not_called()


if __name__ == '__main__':
    unittest.main()
