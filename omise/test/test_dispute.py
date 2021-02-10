import mock
import unittest
import tempfile

from .helper import _ResourceMixin


class DisputeTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Dispute
        return Dispute

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _getLazyCollectionClass(self):
        from .. import LazyCollection
        return LazyCollection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'dispute',
            'id': 'dspt_test',
            'livemode': False,
            'location': '/disputes/dspt_test',
            'amount': 100000,
            'currency': 'thb',
            'status': 'open',
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

    @mock.patch('requests.get')
    def test_list(self, api_call):
        class_ = self._getTargetClass()
        lazy_collection_class_ = self._getLazyCollectionClass()
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

        disputes = class_.list()
        self.assertTrue(isinstance(disputes, lazy_collection_class_))

        disputes = list(disputes)
        self.assertTrue(isinstance(disputes[0], class_))
        self.assertTrue(disputes[0].id, 'dspt_test')
        self.assertTrue(disputes[0].amount, 100000)

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

    @mock.patch('requests.patch')
    def test_accept(self, api_call):
        dispute = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "dispute",
            "id": "dspt_test",
            "livemode": false,
            "status": "lost"
        }""")

        self.assertTrue(isinstance(dispute, class_))
        self.assertEqual(dispute.status, 'open')

        dispute.accept()
        self.assertEqual(dispute.status, 'lost')
        self.assertRequest(
            api_call,
            'https://api.omise.co/disputes/dspt_test/accept'
        )

    @mock.patch('requests.get')
    @mock.patch('requests.post')
    def test_upload_document(self, api_call, reload_call):
        dispute = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "document",
            "livemode": false,
            "id": "docu_test",
            "deleted": false,
            "filename": "evidence.png",
            "location": "/disputes/dspt_test/documents/docu_test",
            "download_uri": null,
            "created_at": "2021-02-05T10:40:32Z"
        }""")

        self.mockResponse(reload_call, """{
            "object": "dispute",
            "id": "dspt_test",
            "livemode": false,
            "location": "/disputes/dspt_test",
            "currency": "THB",
            "amount": 1101000,
            "funding_amount": 1101000,
            "funding_currency": "THB",
            "metadata": {
            },
            "charge": "chrg_test_5m7wj8yi1pa9vlk9bq8",
            "documents": {
            "object": "list",
            "data": [
                {
                "object": "document",
                "livemode": false,
                "id": "docu_test",
                "deleted": false,
                "filename": "evidence.png",
                "location": "/disputes/dspt_test/documents/docu_test",
                "download_uri": null,
                "created_at": "2021-02-05T10:40:32Z"
                }
            ],
            "limit": 20,
            "offset": 0,
            "total": 1,
            "location": "/disputes/dspt_test/documents",
            "order": "chronological",
            "from": "1970-01-01T00:00:00Z",
            "to": "2021-02-05T10:42:02Z"
            },
            "transactions": [
            {
                "object": "transaction",
                "id": "trxn_test",
                "livemode": false,
                "currency": "THB",
                "amount": 1101000,
                "location": "/transactions/trxn_test",
                "direction": "debit",
                "key": "dispute.started.debit",
                "origin": "dspt_test",
                "transferable_at": "2021-02-04T12:08:04Z",
                "created_at": "2021-02-04T12:08:04Z"
            }
            ],
            "admin_message": null,
            "message": null,
            "reason_code": "goods_or_services_not_provided",
            "reason_message": "Services not provided or Merchandise not received",
            "status": "open",
            "closed_at": null,
            "created_at": "2021-02-04T12:08:04Z"
        }""")

        self.assertTrue(isinstance(dispute, class_))

        files = tempfile.TemporaryFile()
        document = dispute.upload_document(files)
        files.close()
        self.assertEqual(dispute.id, 'dspt_test')
        self.assertEqual(document.filename, 'evidence.png')
        self.assertUpload(api_call, 'https://api.omise.co/disputes/dspt_test/documents', files)
