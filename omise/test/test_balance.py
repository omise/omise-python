import mock
import unittest

from .helper import _ResourceMixin


class BalanceTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Balance
        return Balance

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "balance",
            "livemode": false,
            "available": 0,
            "total": 0,
            "currency": "thb"
        }""")

        balance = class_.retrieve()
        self.assertTrue(isinstance(balance, class_))
        self.assertEqual(balance.available, 0)
        self.assertEqual(balance.currency, 'thb')
        self.assertEqual(balance.total, 0)
        self.assertRequest(api_call, 'https://api.omise.co/balance')

        self.mockResponse(api_call, """{
            "object": "balance",
            "livemode": false,
            "available": 4294967295,
            "total": 0,
            "currency": "thb"
        }""")

        balance.reload()
        self.assertEqual(balance.available, 4294967295)
        self.assertRequest(api_call, 'https://api.omise.co/balance')
