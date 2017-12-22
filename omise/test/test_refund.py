import mock
import unittest

from .helper import _ResourceMixin


class RefundTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Refund
        return Refund

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'refund',
            'id': 'rfnd_test',
            'location': '/charges/chrg_test/refunds/rfnd_test',
            'amount': 10000,
            'currency': 'thb',
            'charge': 'chrg_test',
            'transaction': None,
            'created': '2015-01-26T15:06:16Z'
        })

    @mock.patch('requests.get')
    def test_reload(self, api_call):
        refund = self._makeOne()
        class_ = self._getTargetClass()

        self.assertTrue(isinstance(refund, class_))
        self.assertEqual(refund.transaction, None)

        self.mockResponse(api_call, """{
            "object": "refund",
            "id": "rfnd_test",
            "location": "/charges/chrg_test/refunds/rfnd_test",
            "amount": 10000,
            "currency": "thb",
            "charge": "chrg_test",
            "transaction": "trxn_test",
            "created": "2015-01-26T15:06:16Z"
        }""")

        refund.reload()
        self.assertEqual(refund.transaction, 'trxn_test')
        self.assertRequest(
            api_call,
            'https://api.omise.co/charges/chrg_test/refunds/rfnd_test'
        )
