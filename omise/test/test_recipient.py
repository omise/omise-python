import mock
import unittest

from .helper import _ResourceMixin


class RecipientTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Recipient
        return Recipient

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _getBankAccountClass(self):
        from .. import BankAccount
        return BankAccount

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'recipient',
            'id': 'recp_test',
            'livemode': False,
            'location': '/recipients/recp_test',
            'verified': False,
            'active': False,
            'name': 'James Smith',
            'email': 'secondary@recipient.co',
            'description': 'Secondary recipient',
            'type': 'individual',
            'tax_id': '1234567890',
            'bank_account': {
                'object': 'bank_account',
                'brand': 'test',
                'last_digits': '2345',
                'name': 'James Smith',
                'created': '2015-06-02T05:41:53Z'
            },
            'failure_code': None,
            'created': "2015-06-02T05:41:53Z"
        })

    @mock.patch('requests.post')
    def test_create(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "recipient",
            "id": "recp_test",
            "livemode": false,
            "location": "/recipients/recp_test",
            "verified": false,
            "active": false,
            "name": "James Smith",
            "email": "secondary@recipient.co",
            "description": "Secondary recipient",
            "type": "individual",
            "tax_id": "1234567890",
            "bank_account": {
                "object": "bank_account",
                "brand": "test",
                "last_digits": "2345",
                "name": "James Smith",
                "created": "2015-06-02T05:41:53Z"
            },
            "failure_code": null,
            "created": "2015-06-02T05:41:53Z"
        }""")

        recipient = class_.create(
            name='James Smith',
            email='secondary@recipient.co',
            description='Secondary recipient',
            type='individual',
            bank_account={
                'brand': 'test',
                'name': 'James Smith',
                'number': '012345'
            }
        )

        self.assertTrue(isinstance(recipient, class_))
        self.assertEqual(recipient.id, 'recp_test')
        self.assertEqual(recipient.name, 'James Smith')
        self.assertEqual(recipient.description, 'Secondary recipient')
        self.assertEqual(recipient.type, 'individual')

        bank_account = recipient.bank_account
        bank_account_class_ = self._getBankAccountClass()
        self.assertTrue(isinstance(bank_account, bank_account_class_))
        self.assertEqual(bank_account.brand, 'test')
        self.assertEqual(bank_account.last_digits, '2345')
        self.assertEqual(bank_account.name, 'James Smith')
        self.assertRequest(
            api_call,
            'https://api.omise.co/recipients',
            {
                'name': 'James Smith',
                'email': 'secondary@recipient.co',
                'description': 'Secondary recipient',
                'type': 'individual',
                'bank_account': {
                    'brand': 'test',
                    'name': 'James Smith',
                    'number': '012345'
                }
            }
        )

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "recipient",
            "id": "recp_test",
            "livemode": false,
            "location": "/recipients/recp_test",
            "verified": false,
            "active": false,
            "name": "James Smith",
            "email": "secondary@recipient.co",
            "description": "Secondary recipient",
            "type": "individual",
            "tax_id": "1234567890",
            "bank_account": {
                "object": "bank_account",
                "brand": "test",
                "last_digits": "2345",
                "name": "James Smith",
                "created": "2015-06-02T05:41:53Z"
            },
            "failure_code": null,
            "created": "2015-06-02T05:41:53Z"
        }""")

        recipient = class_.retrieve('recp_test')
        self.assertTrue(isinstance(recipient, class_))
        self.assertFalse(recipient.verified)
        self.assertFalse(recipient.active)
        self.assertEqual(recipient.id, 'recp_test')
        self.assertEqual(recipient.name, 'James Smith')
        self.assertEqual(recipient.description, 'Secondary recipient')
        self.assertEqual(recipient.tax_id, '1234567890')
        self.assertEqual(recipient.type, 'individual')

        bank_account_class_ = self._getBankAccountClass()
        bank_account = recipient.bank_account
        self.assertTrue(isinstance(bank_account, bank_account_class_))
        self.assertEqual(bank_account.brand, 'test')
        self.assertEqual(bank_account.last_digits, '2345')
        self.assertEqual(bank_account.name, 'James Smith')

        self.assertRequest(
            api_call,
            'https://api.omise.co/recipients/recp_test')

        self.mockResponse(api_call, """{
            "object": "recipient",
            "id": "recp_test",
            "livemode": false,
            "location": "/recipients/recp_test",
            "verified": false,
            "active": false,
            "name": "Foobar Baz",
            "email": "secondary@recipient.co",
            "description": "Secondary recipient",
            "type": "individual",
            "tax_id": "1234567890",
            "bank_account": {
                "object": "bank_account",
                "brand": "test",
                "last_digits": "2345",
                "name": "James Smith",
                "created": "2015-06-02T05:41:53Z"
            },
            "failure_code": null,
            "created": "2015-06-02T05:41:53Z"
        }""")

        recipient.reload()
        self.assertEqual(recipient.name, 'Foobar Baz')

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2015-06-02T05:41:53+07:00",
            "offset": 0,
            "limit": 20,
            "total": 1,
            "data": [
                {
                    "object": "recipient",
                    "id": "recp_test",
                    "livemode": false,
                    "location": "/recipients/recp_test",
                    "verified": false,
                    "active": false,
                    "name": "Foobar Baz",
                    "email": "secondary@recipient.co",
                    "description": "Secondary recipient",
                    "type": "individual",
                    "tax_id": "1234567890",
                    "bank_account": {
                        "object": "bank_account",
                        "brand": "test",
                        "last_digits": "2345",
                        "name": "James Smith",
                        "created": "2015-06-02T05:41:53Z"
                    },
                    "failure_code": null,
                    "created": "2015-06-02T05:41:53Z"
                }
            ]
        }""")

        recipients = class_.retrieve()
        self.assertTrue(isinstance(recipients, collection_class_))
        self.assertTrue(isinstance(recipients[0], class_))
        self.assertTrue(recipients[0].id, 'recp_test')
        self.assertTrue(recipients[0].name, 'Foobar Baz')
        self.assertRequest(api_call, 'https://api.omise.co/recipients')

    @mock.patch('requests.patch')
    def test_update(self, api_call):
        recipient = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "recipient",
            "id": "recp_test",
            "livemode": false,
            "location": "/recipients/recp_test",
            "verified": false,
            "active": false,
            "name": "Foobar Baz",
            "email": "secondary@recipient.co",
            "description": "Secondary recipient",
            "type": "individual",
            "tax_id": "1234567890",
            "bank_account": {
                "object": "bank_account",
                "brand": "test",
                "last_digits": "2345",
                "name": "James Smith",
                "created": "2015-06-02T05:41:53Z"
            },
            "failure_code": null,
            "created": "2015-06-02T05:41:53Z"
        }""")

        self.assertTrue(isinstance(recipient, class_))
        self.assertEqual(recipient.name, 'James Smith')
        recipient.name = 'Foobar Baz'
        recipient.update()

        self.assertEqual(recipient.name, 'Foobar Baz')
        self.assertRequest(
            api_call,
            'https://api.omise.co/recipients/recp_test',
            {'name': 'Foobar Baz'}
        )

    @mock.patch('requests.delete')
    def test_destroy(self, api_call):
        recipient = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "recipient",
            "id": "recp_test",
            "livemode": false,
            "deleted": true
        }""")

        self.assertTrue(isinstance(recipient, class_))
        self.assertEqual(recipient.id, 'recp_test')

        recipient.destroy()
        self.assertTrue(recipient.destroyed)
        self.assertRequest(
            api_call,
            'https://api.omise.co/recipients/recp_test'
        )
