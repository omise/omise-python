import mock
import unittest

from .helper import _ResourceMixin


class TransferTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Transfer
        return Transfer

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'transfer',
            'created': '2014-11-18T11:31:26Z',
            'livemode': False,
            'failure_message': None,
            'paid': False,
            'currency': 'thb',
            'amount': 100000,
            'transaction': None,
            'location': '/transfers/trsf_test',
            'failure_code': None,
            'id': 'trsf_test',
            'sent': False
        })

    @mock.patch('requests.post')
    def test_create(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "transfer",
            "id": "trsf_test",
            "livemode": false,
            "location": "/transfers/trsf_test",
            "sent": false,
            "paid": false,
            "amount": 100000,
            "currency": "thb",
            "failure_code": null,
            "failure_message": null,
            "transaction": null,
            "created": "2014-11-18T11:31:26Z"
        }""")

        transfer = class_.create(amount=100000)
        self.assertTrue(isinstance(transfer, class_))
        self.assertEqual(transfer.id, 'trsf_test')
        self.assertEqual(transfer.amount, 100000)
        self.assertRequest(
            api_call,
            'https://api.omise.co/transfers',
            {'amount': 100000}
        )

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "transfer",
            "id": "trsf_test",
            "livemode": false,
            "location": "/transfers/trsf_test",
            "sent": false,
            "paid": false,
            "amount": 100000,
            "currency": "thb",
            "failure_code": null,
            "failure_message": null,
            "transaction": null,
            "created": "2014-11-18T11:31:26Z"
        }
        """)

        transfer = class_.retrieve('trsf_test')
        self.assertTrue(isinstance(transfer, class_))
        self.assertFalse(transfer.sent)
        self.assertFalse(transfer.paid)
        self.assertEqual(transfer.id, 'trsf_test')
        self.assertEqual(transfer.amount, 100000)
        self.assertEqual(transfer.transaction, None)
        self.assertRequest(api_call, 'https://api.omise.co/transfers/trsf_test')

        self.mockResponse(api_call, """{
            "object": "transfer",
            "id": "trsf_test",
            "livemode": false,
            "location": "/transfers/trsf_test",
            "sent": true,
            "paid": true,
            "amount": 100000,
            "currency": "thb",
            "failure_code": null,
            "failure_message": null,
            "transaction": null,
            "created": "2014-11-18T11:31:26Z"
        }
        """)

        transfer.reload()
        self.assertTrue(transfer.sent)
        self.assertTrue(transfer.paid)

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2014-10-27T11:36:24+07:00",
            "offset": 0,
            "limit": 20,
            "total": 1,
            "data": [
                {
                    "object": "transfer",
                    "id": "trsf_test",
                    "livemode": false,
                    "location": "/transfers/trsf_test",
                    "sent": false,
                    "paid": false,
                    "amount": 96350,
                    "currency": "thb",
                    "failure_code": null,
                    "failure_message": null,
                    "transaction": null,
                    "created": "2014-11-18T11:31:26Z"
                }
            ]
        }""")

        transfers = class_.retrieve()
        self.assertTrue(isinstance(transfers, collection_class_))
        self.assertTrue(isinstance(transfers[0], class_))
        self.assertTrue(transfers[0].id, 'trsf_test')
        self.assertTrue(transfers[0].amount, 96350)
        self.assertRequest(api_call, 'https://api.omise.co/transfers')

    @mock.patch('requests.patch')
    def test_update(self, api_call):
        transfer = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "transfer",
            "id": "trsf_test",
            "livemode": false,
            "location": "/transfers/trsf_test",
            "sent": false,
            "paid": false,
            "amount": 80000,
            "currency": "thb",
            "failure_code": null,
            "failure_message": null,
            "transaction": null,
            "created": "2014-11-18T11:31:26Z"
        }""")

        self.assertTrue(isinstance(transfer, class_))
        self.assertEqual(transfer.amount, 100000)
        transfer.amount = 80000
        transfer.update()

        self.assertEqual(transfer.amount, 80000)
        self.assertRequest(
            api_call,
            'https://api.omise.co/transfers/trsf_test',
            {'amount': 80000}
        )

    @mock.patch('requests.delete')
    def test_destroy(self, api_call):
        transfer = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "transfer",
            "id": "trsf_test",
            "livemode": false,
            "deleted": true
        }""")

        self.assertTrue(isinstance(transfer, class_))
        self.assertEqual(transfer.id, 'trsf_test')

        transfer.destroy()
        self.assertTrue(transfer.destroyed)
        self.assertRequest(
            api_call,
            'https://api.omise.co/transfers/trsf_test'
        )
