import mock
import unittest

from .helper import _ResourceMixin


class DisputeTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Dispute
        return Dispute

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'dispute',
            'id': 'dspt_test',
            'livemode': False,
            'location': '/disputes/dspt_test',
            'amount': 100000,
            'currency': 'thb',
            'status': 'pending',
            'message': None,
            'charge': 'chrg_test',
            'created': '2015-03-23T05:24:39Z'
        })

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "dispute",
            "id": "dspt_test",
            "livemode": false,
            "location": "/disputes/dspt",
            "amount": 100000,
            "currency": "thb",
            "status": "pending",
            "message": null,
            "charge": "chrg_test",
            "created": "2015-03-23T05:24:39Z"
        }""")

        dispute = class_.retrieve('dspt_test')
        self.assertTrue(isinstance(dispute, class_))
        self.assertEqual(dispute.id, 'dspt_test')
        self.assertEqual(dispute.amount, 100000)
        self.assertEqual(dispute.currency, 'thb')
        self.assertEqual(dispute.status, 'pending')
        self.assertEqual(dispute.charge, 'chrg_test')
        self.assertEqual(dispute.message, None)

        self.assertRequest(
            api_call,
            'https://api.omise.co/disputes/dspt_test')

        self.mockResponse(api_call, """{
            "object": "dispute",
            "id": "dspt_test",
            "livemode": false,
            "location": "/disputes/dspt_test",
            "amount": 100000,
            "currency": "thb",
            "status": "pending",
            "message": "Foobar Baz",
            "charge": "chrg_test",
            "created": "2015-03-23T05:24:39Z"
        }""")

        dispute.reload()
        self.assertEqual(dispute.message, 'Foobar Baz')

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2015-03-23T05:24:39+07:00",
            "offset": 0,
            "limit": 20,
            "total": 1,
            "data": [
                {
                    "object": "dispute",
                    "id": "dspt_test",
                    "livemode": false,
                    "location": "/disputes/dspt_test",
                    "amount": 100000,
                    "currency": "thb",
                    "status": "pending",
                    "message": "Foobar Baz",
                    "charge": "chrg_test",
                    "created": "2015-03-23T05:24:39Z"
                }
            ]
        }""")

        disputes = class_.retrieve()
        self.assertTrue(isinstance(disputes, collection_class_))
        self.assertTrue(isinstance(disputes[0], class_))
        self.assertTrue(disputes[0].id, 'dspt_test')
        self.assertTrue(disputes[0].amount, 100000)
        self.assertRequest(api_call, 'https://api.omise.co/disputes')

    @mock.patch('requests.get')
    def test_retrieve_kwargs(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2015-03-23T05:24:39+07:00",
            "offset": 0,
            "limit": 20,
            "total": 1,
            "data": [
                {
                    "object": "dispute",
                    "id": "dspt_test",
                    "livemode": false,
                    "location": "/disputes/dspt_test",
                    "amount": 100000,
                    "currency": "thb",
                    "status": "closed",
                    "message": "Foobar Baz",
                    "charge": "chrg_test",
                    "created": "2015-03-23T05:24:39Z"
                }
            ]
        }""")

        disputes = class_.retrieve('closed')
        self.assertTrue(isinstance(disputes, collection_class_))
        self.assertTrue(isinstance(disputes[0], class_))
        self.assertTrue(disputes[0].id, 'dspt_test')
        self.assertTrue(disputes[0].status, 'closed')
        self.assertRequest(api_call, 'https://api.omise.co/disputes/closed')

    @mock.patch('requests.patch')
    def test_update(self, api_call):
        dispute = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "dispute",
            "id": "dspt_test",
            "livemode": false,
            "location": "/disputes/dspt_test",
            "amount": 100000,
            "currency": "thb",
            "status": "pending",
            "message": "Foobar Baz",
            "charge": "chrg_test",
            "created": "2015-03-23T05:24:39Z"
        }""")

        self.assertTrue(isinstance(dispute, class_))
        self.assertEqual(dispute.message, None)
        dispute.message = 'Foobar Baz'
        dispute.update()

        self.assertEqual(dispute.message, 'Foobar Baz')
        self.assertRequest(
            api_call,
            'https://api.omise.co/disputes/dspt_test',
            {'message': 'Foobar Baz'}
        )
