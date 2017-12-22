import mock
import unittest

from .helper import _ResourceMixin


class SearchTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Search
        return Search

    @mock.patch('requests.get')
    def test_charge(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "search",
            "order": "chronological",
            "scope": "charge",
            "query": "thb",
            "filters": {
                "amount": "1000..2000",
                "captured": "true"
            },
            "page": 1,
            "per_page": 30,
            "location": "/search",
            "total_pages": 1,
            "total": 1,
            "data": [
                {
                    "object": "charge",
                    "id": "chrg_test",
                    "livemode": false,
                    "location": "/charges/chrg_test",
                    "amount": 120000,
                    "currency": "thb",
                    "description": "iTunes Purchase",
                    "metadata": {},
                    "status": "successful",
                    "capture": true,
                    "authorized": true,
                    "reversed": false,
                    "paid": true,
                    "transaction": "trxn_test",
                    "source_of_fund": "card",
                    "refunded": 0,
                    "refunds": {
                        "object": "list",
                        "from": "1970-01-01T07:00:00+07:00",
                        "to": "2017-06-06T12:47:27+07:00",
                        "offset": 0,
                        "limit": 20,
                        "total": 0,
                        "order": null,
                        "location": "/charges/chrg_test/refunds",
                        "data": []
                    },
                    "return_uri": null,
                    "offsite": null,
                    "offline": null,
                    "reference": null,
                    "authorize_uri": null,
                    "failure_code": null,
                    "failure_message": null,
                    "card": {
                        "object": "card",
                        "id": "card_test",
                        "livemode": false,
                        "location": "/customers/cust_test/cards/card_test",
                        "country": "us",
                        "city": "Bangkok",
                        "postal_code": "10240",
                        "financing": "",
                        "bank": "",
                        "last_digits": "4242",
                        "brand": "Visa",
                        "expiration_month": 12,
                        "expiration_year": 2020,
                        "fingerprint": "hWA+g07yu/7ngJfMJJ0ndGFqynzm2nQ3k/yDCofKZBM=",
                        "name": "Somchai Prasert",
                        "security_code_check": true,
                        "created": "2017-05-30T09:49:54Z"
                    },
                    "customer": "cust_test",
                    "ip": null,
                    "dispute": null,
                    "created": "2017-06-05T08:29:14Z"
                }
            ]
        }""")

        querystring = {
            'query': 'thb',
            'filters': {
                'amount': '1000..2000',
                'captured': 'true'
            }
        }

        result = class_.execute('charge', **querystring)
        self.assertTrue(isinstance(result, class_))
        self.assertEqual(result.scope, 'charge')
        self.assertEqual(result.query, 'thb')
        self.assertEqual(result.total, 1)
        self.assertEqual(result._attributes['filters']['amount'], '1000..2000')
        self.assertEqual(result._attributes['filters']['captured'], 'true')
        self.assertEqual(result[0].id, 'chrg_test')
        self.assertEqual(result[0].currency, 'thb')
        self.assertEqual(result[0].amount, 120000)
        self.assertTrue(result[0].capture)

    @mock.patch('requests.get')
    def test_dispute(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "search",
            "order": "chronological",
            "scope": "dispute",
            "query": "dspt_test",
            "filters": {
                "status": "pending"
            },
            "page": 1,
            "per_page": 30,
            "location": "/search",
            "total_pages": 1,
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
                    "message": null,
                    "charge": "chrg_test",
                    "created": "2015-03-23T05:24:39"
                }
            ]
        }""")

        querystring = {
            'query': 'dspt_test',
            'filters': {
                'status': 'pending'
            }
        }

        result = class_.execute('dispute', **querystring)
        self.assertTrue(isinstance(result, class_))
        self.assertEqual(result.scope, 'dispute')
        self.assertEqual(result.query, 'dspt_test')
        self.assertEqual(result.total, 1)
        self.assertEqual(result._attributes['filters']['status'], 'pending')
        self.assertEqual(result[0].id, 'dspt_test')
        self.assertEqual(result[0].status, 'pending')

    @mock.patch('requests.get')
    def test_recipient(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "search",
            "order": "chronological",
            "scope": "recipient",
            "query": "secondary@recipient.co",
            "filters": {
                "type": "individual"
            },
            "page": 1,
            "per_page": 30,
            "location": "/search",
            "total_pages": 1,
            "total": 1,
            "data": [
                {
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
                }
            ]
        }""")

        querystring = {
            'query': 'secondary@recipient.co',
            'filters': {
                'type': 'individual'
            }
        }

        result = class_.execute('recipient', **querystring)
        self.assertTrue(isinstance(result, class_))
        self.assertEqual(result.scope, 'recipient')
        self.assertEqual(result.query, 'secondary@recipient.co')
        self.assertEqual(result.total, 1)
        self.assertEqual(result._attributes['filters']['type'], 'individual')
        self.assertEqual(result[0].id, 'recp_test')
        self.assertEqual(result[0].email, 'secondary@recipient.co')
        self.assertEqual(result[0].type, 'individual')

    @mock.patch('requests.get')
    def test_customer(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "search",
            "order": "chronological",
            "scope": "customer",
            "query": "john.doe@example.com",
            "filters": {
                "created": "2014-10-24"
            },
            "page": 1,
            "per_page": 30,
            "location": "/search",
            "total_pages": 1,
            "total": 1,
            "data": [
                {
                    "object": "customer",
                    "id": "cust_test",
                    "livemode": false,
                    "location": "/customers/cust_test",
                    "default_card": null,
                    "email": "john.doe@example.com",
                    "description": "John Doe (id: 30)",
                    "created": "2014-10-24T06:04:48Z",
                    "cards": {
                        "object": "list",
                        "from": "1970-01-01T07:00:00+07:00",
                        "to": "2014-10-24T13:04:48+07:00",
                        "offset": 0,
                        "limit": 20,
                        "total": 1,
                        "data": [
                            {
                                "object": "card",
                                "id": "card_test",
                                "livemode": false,
                                "location": "/customers/cust_test/cards/card_test",
                                "country": "",
                                "city": null,
                                "postal_code": null,
                                "financing": "",
                                "last_digits": "4242",
                                "brand": "Visa",
                                "expiration_month": 9,
                                "expiration_year": 2017,
                                "fingerprint": "098f6bcd4621d373cade4e832627b4f6",
                                "name": "Test card",
                                "created": "2014-10-24T08:26:07Z"
                            }
                        ],
                        "location": "/customers/cust_test/cards"
                    }
                }
            ]
        }""")

        querystring = {
            'query': 'john.doe@example.com',
            'filters': {
                'created': '2014-10-24'
            }
        }

        result = class_.execute('customer', **querystring)
        self.assertTrue(isinstance(result, class_))
        self.assertEqual(result.scope, 'customer')
        self.assertEqual(result.query, 'john.doe@example.com')
        self.assertEqual(result.total, 1)
        self.assertEqual(result._attributes['filters']['created'], '2014-10-24')
        self.assertEqual(result[0].id, 'cust_test')
        self.assertEqual(result[0].email, 'john.doe@example.com')
        self.assertEqual(result[0].created, '2014-10-24T06:04:48Z')
