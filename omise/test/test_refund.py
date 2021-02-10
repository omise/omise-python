import mock
import unittest

from .helper import _ResourceMixin


class RefundTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Refund
        return Refund

    def _getLazyCollectionClass(self):
        from .. import LazyCollection
        return LazyCollection

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
    def test_list(self, api_call):
        class_ = self._getTargetClass()
        lazy_collection_class_ = self._getLazyCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2015-11-20T14:17:24+07:00",
            "offset": 0,
            "limit": 20,
            "total": 2,
            "data": [
                {
                    "object": "refund",
                    "id": "rfnd_test_1",
                    "livemode": false,
                    "location": "/charges/chrg_test/refunds/rfnd_test_1",
                    "amount": 10000,
                    "currency": "thb",
                    "charge": "chrg_test",
                    "transaction": null,
                    "created": "2015-01-26T15:06:16Z"
                },
                {
                    "object": "refund",
                    "id": "rfnd_test_2",
                    "livemode": false,
                    "location": "/charges/chrg_test/refunds/rfnd_test_2",
                    "amount": 20000,
                    "currency": "thb",
                    "charge": "chrg_test",
                    "transaction": null,
                    "created": "2015-01-27T12:16:48Z"
                }
            ]
        }""")

        refunds = class_.list()
        self.assertTrue(isinstance(refunds, lazy_collection_class_))

        refunds = list(refunds)
        self.assertTrue(isinstance(refunds[0], class_))
        self.assertTrue(refunds[0].id, 'rfnd_test_1')
        self.assertTrue(refunds[0].amount, 10000)
        self.assertTrue(refunds[1].id, 'rfnd_test_2')
        self.assertTrue(refunds[1].amount, 20000)

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
