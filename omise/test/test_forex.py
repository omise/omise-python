import mock
import unittest

from .helper import _ResourceMixin


class ForexTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Forex
        return Forex

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "forex",
            "from": "thb",
            "to": "usd",
            "rate": 32.747069,
            "location": "/forex/usd"
        }""")

        forex = class_.retrieve('usd')
        self.assertTrue(isinstance(forex, class_))
        self.assertTrue(forex.to, 'usd')
        self.assertTrue(forex.rate, 32.747069)
        self.assertRequest(api_call, 'https://api.omise.co/forex/usd')
