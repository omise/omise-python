import mock
import unittest

from .helper import _RequestAssertable


class RequestTest(_RequestAssertable, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Request
        return Request

    def test_init(self):
        class_ = self._getTargetClass()
        request = class_('skey_test', 'https://api.omise.co', '2015-11-01')
        self.assertEqual(request.api_key, 'skey_test')
        self.assertEqual(request.api_base, 'https://api.omise.co')
        self.assertEqual(request.api_version, '2015-11-01')

    def test_init_no_api_key(self):
        class_ = self._getTargetClass()

        def _func():
            class_(None, 'https://api.omise.co', '2015-11-01')
        self.assertRaises(AttributeError, _func)

    @mock.patch('requests.get')
    def test_send(self, api_call):
        from ..version import __VERSION__
        class_ = self._getTargetClass()
        request = class_('skey_test', 'https://api.omise.co', '2015-11-01')
        self.mockResponse(api_call, '{"ping":"pong"}')
        self.assertEqual(request.send('get', 'ping'), {'ping': 'pong'})
        self.assertRequest(api_call, 'https://api.omise.co/ping', headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Omise-Version': '2015-11-01',
            'User-Agent': 'OmisePython/%s' % __VERSION__
        })

    @mock.patch('requests.get')
    def test_send_tuple_url(self, api_call):
        class_ = self._getTargetClass()
        request = class_('skey_test', 'https://api.omise.co', '2015-11-01')
        self.mockResponse(api_call, '{"ping":"pong"}')
        self.assertEqual(request.send('get', ('ping', 1)), {'ping': 'pong'})
        self.assertRequest(api_call, 'https://api.omise.co/ping/1')

    @mock.patch('requests.get')
    def test_send_no_version(self, api_call):
        from ..version import __VERSION__
        class_ = self._getTargetClass()
        request = class_('skey_test', 'https://api.omise.co', None)
        self.mockResponse(api_call, '{"ping":"pong"}')
        self.assertEqual(request.send('get', 'ping'), {'ping': 'pong'})
        self.assertRequest(api_call, 'https://api.omise.co/ping', headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'OmisePython/%s' % __VERSION__
        })

    @mock.patch('requests.post')
    def test_send_post(self, api_call):
        class_ = self._getTargetClass()
        request = class_('skey_test', 'https://api.omise.co', '2015-11-01')
        params = {'test': 'request'}
        self.mockResponse(api_call, '{"ping":"pong"}')
        self.assertEqual(request.send('post', 'ping', params), {'ping': 'pong'})
        self.assertRequest(api_call, 'https://api.omise.co/ping', params)
