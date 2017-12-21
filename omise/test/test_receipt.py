import mock
import unittest

from .helper import _ResourceMixin


class ReceiptTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Receipt
        return Receipt

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'receipt',
            'id': 'rcpt_test',
            'number': 'OMTH201710110001',
            'location': '/receipts/rcpt_test',
            'date': '2017-10-11T16:59:59Z',
            'customer_name': 'John Doe',
            'customer_address': 'Crystal Design Center (CDC)',
            'customer_tax_id': 'Tax ID 1234',
            'customer_email': 'john@omise.co',
            'customer_statement_name': 'John',
            'company_name': 'Omise Company Limited',
            'company_address': 'Crystal Design Center (CDC)',
            'company_tax_id': '0000000000000',
            'charge_fee': 1315,
            'voided_fee': 0,
            'transfer_fee': 0,
            'subtotal': 1315,
            'vat': 92,
            'wht': 0,
            'total': 1407,
            'credit_note': False,
            'currency': 'thb'
        })

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "receipt",
            "id": "rcpt_test",
            "number": "OMTH201710110001",
            "location": "/receipts/rcpt_test",
            "date": "2017-10-11T16:59:59Z",
            "customer_name": "John Doe",
            "customer_address": "Crystal Design Center (CDC)",
            "customer_tax_id": "Tax ID 1234",
            "customer_email": "john@omise.co",
            "customer_statement_name": "John",
            "company_name": "Omise Company Limited",
            "company_address": "Crystal Design Center (CDC)",
            "company_tax_id": "0000000000000",
            "charge_fee": 1315,
            "voided_fee": 0,
            "transfer_fee": 0,
            "subtotal": 1315,
            "vat": 92,
            "wht": 0,
            "total": 1407,
            "credit_note": false,
            "currency": "thb"
        }""")

        receipt = class_.retrieve('rcpt_test')
        self.assertTrue(isinstance(receipt, class_))
        self.assertEqual(receipt.id, 'rcpt_test')
        self.assertEqual(receipt.number, 'OMTH201710110001')
        self.assertEqual(receipt.company_tax_id, '0000000000000')
        self.assertEqual(receipt.charge_fee, 1315)
        self.assertEqual(receipt.voided_fee, 0)
        self.assertEqual(receipt.transfer_fee, 0)
        self.assertEqual(receipt.subtotal, 1315)
        self.assertEqual(receipt.total, 1407)
        self.assertEqual(receipt.currency, 'thb')
        self.assertRequest(
            api_call,
            'https://api.omise.co/receipts/rcpt_test'
        )

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T00:00:00Z",
            "to": "2017-10-11T23:59:59Z",
            "offset": 0,
            "limit": 20,
            "total": 1,
            "order": "chronological",
            "location": "/receipts",
            "data": [
                {
                    "object": "receipt",
                    "id": "rcpt_test",
                    "number": "OMTH201710110001",
                    "location": "/receipts/rcpt_test",
                    "date": "2017-10-11T16:59:59Z",
                    "customer_name": "John Doe",
                    "customer_address": "Crystal Design Center (CDC)",
                    "customer_tax_id": "Tax ID 1234",
                    "customer_email": "john@omise.co",
                    "customer_statement_name": "John",
                    "company_name": "Omise Company Limited",
                    "company_address": "Crystal Design Center (CDC)",
                    "company_tax_id": "0000000000000",
                    "charge_fee": 1315,
                    "voided_fee": 0,
                    "transfer_fee": 0,
                    "subtotal": 1315,
                    "vat": 92,
                    "wht": 0,
                    "total": 1407,
                    "credit_note": false,
                    "currency": "thb"
                }
            ]
        }""")

        receipts = class_.retrieve()
        self.assertTrue(isinstance(receipts, collection_class_))
        self.assertTrue(isinstance(receipts[0], class_))
        self.assertEqual(receipts[0].id, 'rcpt_test')
        self.assertEqual(receipts[0].number, 'OMTH201710110001')
        self.assertEqual(receipts[0].company_tax_id, '0000000000000')
        self.assertEqual(receipts[0].charge_fee, 1315)
        self.assertEqual(receipts[0].voided_fee, 0)
        self.assertEqual(receipts[0].transfer_fee, 0)
        self.assertEqual(receipts[0].subtotal, 1315)
        self.assertEqual(receipts[0].total, 1407)
        self.assertEqual(receipts[0].currency, 'thb')
        self.assertRequest(
            api_call,
            'https://api.omise.co/receipts'
        )
