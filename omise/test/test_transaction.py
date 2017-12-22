import mock
import unittest

from .helper import _ResourceMixin


class TransactionTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Transaction
        return Transaction

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "transaction",
            "id": "trxn_test",
            "type": "credit",
            "amount": 9635024,
            "currency": "thb",
            "created": "2014-10-27T06:58:56Z"
        }
        """)

        transaction = class_.retrieve('trxn_test')
        self.assertTrue(isinstance(transaction, class_))
        self.assertEqual(transaction.id, 'trxn_test')
        self.assertEqual(transaction.type, 'credit')
        self.assertEqual(transaction.amount, 9635024)
        self.assertEqual(transaction.currency, 'thb')
        self.assertRequest(
            api_call,
            'https://api.omise.co/transactions/trxn_test'
        )

        transaction.amount = 9635023
        self.assertEqual(transaction.amount, 9635023)
        self.mockResponse(api_call, """{
            "object": "transaction",
            "id": "trxn_test",
            "type": "credit",
            "amount": 9635024,
            "currency": "thb",
            "created": "2014-10-27T06:58:56Z"
        }
        """)

        transaction.reload()
        self.assertEqual(transaction.amount, 9635024)
        self.assertEqual(transaction.currency, 'thb')
        self.assertRequest(
            api_call,
            'https://api.omise.co/transactions/trxn_test'
        )

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2014-10-27T14:55:29+07:00",
            "offset": 0,
            "limit": 20,
            "total": 2,
            "data": [
                {
                    "object": "transaction",
                    "id": "trxn_test_1",
                    "type": "credit",
                    "amount": 9635024,
                    "currency": "thb",
                    "created": "2014-10-27T06:58:56Z"
                },
                {
                    "object": "transaction",
                    "id": "trxn_test_2",
                    "type": "debit",
                    "amount": 100025,
                    "currency": "thb",
                    "created": "2014-10-27T07:02:54Z"
                }
            ]
        }""")

        transactions = class_.retrieve()
        self.assertTrue(isinstance(transactions, collection_class_))
        self.assertTrue(isinstance(transactions[0], class_))
        self.assertTrue(transactions[0].id, 'trxn_test_1')
        self.assertTrue(transactions[0].type, 'credit')
        self.assertTrue(transactions[0].amount, 9635024)
        self.assertTrue(isinstance(transactions[1], class_))
        self.assertTrue(transactions[1].id, 'trxn_test_2')
        self.assertTrue(transactions[1].type, 'debit')
        self.assertTrue(transactions[1].amount, 100025)
        self.assertRequest(api_call, 'https://api.omise.co/transactions')
