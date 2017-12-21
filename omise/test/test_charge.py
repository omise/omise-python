import mock
import unittest

from .helper import _ResourceMixin


class ChargeTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Charge
        return Charge

    def _getCardClass(self):
        from .. import Card
        return Card

    def _getSourceClass(self):
        from .. import Source
        return Source

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'card': {
                'city': 'Bangkok',
                'financing': 'credit',
                'object': 'card',
                'expiration_year': 2018,
                'last_digits': '4242',
                'created': '2014-10-20T09:41:56Z',
                'country': 'th',
                'brand': 'Visa',
                'livemode': False,
                'expiration_month': 10,
                'postal_code': '10320',
                'fingerprint': '098f6bcd4621d373cade4e832627b4f6',
                'id': 'card_test',
                'name': 'Somchai Prasert'
            },
            'capture': False,
            'object': 'charge',
            'description': 'Order-384',
            'created': '2014-10-21T11:12:28Z',
            'ip': '127.0.0.1',
            'livemode': False,
            'currency': 'thb',
            'amount': 100000,
            'transaction': None,
            'refunded': 0,
            'refunds': {
                'object': 'list',
                'from': '1970-01-01T00:00:00+00:00',
                'to': '2015-01-26T16:20:43+00:00',
                'offset': 0,
                'limit': 20,
                'total': 0,
                'data': [],
                'location': '/charges/chrg_test/refunds',
            },
            'failure_code': None,
            'failure_message': None,
            'location': '/charges/chrg_test',
            'customer': None,
            'id': 'chrg_test',
            'captured': False,
            'authorized': True,
            'reversed': False
        })

    @mock.patch('requests.post')
    def test_create(self, api_call):
        class_ = self._getTargetClass()
        card_class_ = self._getCardClass()
        self.mockResponse(api_call, """{
            "object": "charge",
            "id": "chrg_test",
            "livemode": false,
            "location": "/charges/chrg_test",
            "amount": 100000,
            "currency": "thb",
            "description": "Order-384",
            "capture": false,
            "authorized": false,
            "reversed": false,
            "captured": false,
            "transaction": null,
            "refunded": 0,
            "refunds": {
                "object": "list",
                "from": "1970-01-01T00:00:00+00:00",
                "to": "2015-01-26T16:20:43+00:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "data": [],
                "location": "/charges/chrg_test/refunds"
            },
            "failure_code": null,
            "failure_message": null,
            "card": {
                "object": "card",
                "id": "card_test",
                "livemode": false,
                "country": "th",
                "city": "Bangkok",
                "postal_code": "10320",
                "financing": "credit",
                "last_digits": "4242",
                "brand": "Visa",
                "expiration_month": 10,
                "expiration_year": 2018,
                "fingerprint": "098f6bcd4621d373cade4e832627b4f6",
                "name": "Somchai Prasert",
                "created": "2014-10-20T09:41:56Z"
            },
            "customer": null,
            "ip": "127.0.0.1",
            "created": "2014-10-21T11:12:28Z"
        }""")

        charge = class_.create(
            amount=100000,
            currency='thb',
            description='Order-384',
            ip='127.0.0.1',
            card='tokn_test',
        )

        self.assertTrue(isinstance(charge, class_))
        self.assertTrue(isinstance(charge.card, card_class_))
        self.assertEqual(charge.id, 'chrg_test')
        self.assertEqual(charge.amount, 100000)
        self.assertEqual(charge.currency, 'thb')
        self.assertEqual(charge.description, 'Order-384')
        self.assertEqual(charge.ip, '127.0.0.1')
        self.assertEqual(charge.card.id, 'card_test')
        self.assertEqual(charge.card.last_digits, '4242')
        self.assertRequest(
            api_call,
            'https://api.omise.co/charges',
            {
                'amount': 100000,
                'currency': 'thb',
                'description': 'Order-384',
                'ip': '127.0.0.1',
                'card': 'tokn_test',
            }
        )

    @mock.patch('requests.post')
    def test_create_with_source(self, api_call):
        class_ = self._getTargetClass()
        source_class_ = self._getSourceClass()
        self.mockResponse(api_call, """{
            "object": "charge",
            "id": "chrg_test",
            "livemode": false,
            "location": "/charges/chrg_test",
            "amount": 100000,
            "currency": "thb",
            "description": null,
            "metadata": {},
            "status": "pending",
            "capture": true,
            "authorized": false,
            "reversed": false,
            "paid": false,
            "transaction": null,
            "refunded": 0,
            "refunds": {
                "object": "list",
                "from": "1970-01-01T00:00:00+00:00",
                "to": "2015-01-26T16:20:43+00:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "location": "/charges/chrg_test/refunds",
                "data": []
            },
            "return_uri": "http://www.google.com",
            "reference": "ofsp_test",
            "authorize_uri": "https://pay.omise.co/offsites/ofsp_test/pay",
            "failure_code": null,
            "failure_message": null,
            "card": null,
            "customer": null,
            "ip": null,
            "dispute": null,
            "created": "2014-10-21T11:12:28Z",
            "source": {
                "object": "source",
                "id": "src_test",
                "type": "internet_banking_test",
                "flow": "redirect",
                "amount": 100000,
                "currency": "thb"
            }
        }""")

        charge = class_.create(
            amount=100000,
            currency='thb',
            source='src_test',
            return_uri='http://www.google.com'
        )

        self.assertTrue(isinstance(charge, class_))
        self.assertTrue(isinstance(charge.source, source_class_))
        self.assertEqual(charge.id, 'chrg_test')
        self.assertEqual(charge.amount, 100000)
        self.assertEqual(charge.currency, 'thb')
        self.assertEqual(charge.source.id, 'src_test')
        self.assertRequest(
            api_call,
            'https://api.omise.co/charges',
            {
                'amount': 100000,
                'currency': 'thb',
                'source': 'src_test',
                'return_uri': 'http://www.google.com'
            }
        )

        charge = class_.create(
            amount=100000,
            currency='thb',
            source={
                'type': 'internet_banking_test'
            },
            return_uri='http://www.google.com'
        )

        self.assertTrue(isinstance(charge, class_))
        self.assertTrue(isinstance(charge.source, source_class_))
        self.assertEqual(charge.id, 'chrg_test')
        self.assertEqual(charge.amount, 100000)
        self.assertEqual(charge.currency, 'thb')
        self.assertEqual(charge.source.id, 'src_test')
        self.assertRequest(
            api_call,
            'https://api.omise.co/charges', {
                'amount': 100000,
                'currency': 'thb',
                'source': {
                    'type': 'internet_banking_test'
                },
                'return_uri': 'http://www.google.com'
            }
        )

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        card_class_ = self._getCardClass()
        self.mockResponse(api_call, """{
            "object": "charge",
            "id": "chrg_test",
            "livemode": false,
            "location": "/charges/chrg_test",
            "amount": 100000,
            "currency": "thb",
            "description": "Order-384",
            "capture": false,
            "authorized": true,
            "reversed": false,
            "captured": false,
            "transaction": null,
            "refunded": 0,
            "refunds": {
                "object": "list",
                "from": "1970-01-01T00:00:00+00:00",
                "to": "2015-01-26T16:20:43+00:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "data": [],
                "location": "/charges/chrg_test/refunds"
            },
            "failure_code": null,
            "failure_message": null,
            "card": {
                "object": "card",
                "id": "card_test",
                "livemode": false,
                "country": "th",
                "city": "Bangkok",
                "postal_code": "10320",
                "financing": "credit",
                "last_digits": "4242",
                "brand": "Visa",
                "expiration_month": 10,
                "expiration_year": 2018,
                "fingerprint": "098f6bcd4621d373cade4e832627b4f6",
                "name": "Somchai Prasert",
                "created": "2014-10-20T09:41:56Z"
            },
            "customer": null,
            "ip": "127.0.0.1",
            "created": "2014-10-21T11:12:28Z"
        }""")

        charge = class_.retrieve('chrg_test')
        self.assertTrue(isinstance(charge, class_))
        self.assertTrue(isinstance(charge.card, card_class_))
        self.assertEqual(charge.id, 'chrg_test')
        self.assertEqual(charge.amount, 100000)
        self.assertEqual(charge.currency, 'thb')
        self.assertEqual(charge.description, 'Order-384')
        self.assertEqual(charge.ip, '127.0.0.1')
        self.assertEqual(charge.card.id, 'card_test')
        self.assertEqual(charge.card.last_digits, '4242')
        self.assertRequest(api_call, 'https://api.omise.co/charges/chrg_test')

        self.mockResponse(api_call, """{
            "object": "charge",
            "id": "chrg_test",
            "livemode": false,
            "location": "/charges/chrg_test",
            "amount": 120000,
            "currency": "thb",
            "description": "Order-384",
            "capture": false,
            "authorized": true,
            "reversed": false,
            "captured": false,
            "transaction": null,
            "refunded": 0,
            "refunds": {
                "object": "list",
                "from": "1970-01-01T00:00:00+00:00",
                "to": "2015-01-26T16:20:43+00:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "data": [],
                "location": "/charges/chrg_test/refunds"
            },
            "failure_code": null,
            "failure_message": null,
            "card": {
                "object": "card",
                "id": "card_test",
                "livemode": false,
                "country": "th",
                "city": "Bangkok",
                "postal_code": "10320",
                "financing": "credit",
                "last_digits": "4242",
                "brand": "Visa",
                "expiration_month": 10,
                "expiration_year": 2018,
                "fingerprint": "098f6bcd4621d373cade4e832627b4f6",
                "name": "Somchai Prasert",
                "created": "2014-10-20T09:41:56Z"
            },
            "customer": null,
            "ip": "127.0.0.1",
            "created": "2014-10-21T11:12:28Z"
        }""")

        charge.reload()
        self.assertEqual(charge.amount, 120000)
        self.assertEqual(charge.currency, 'thb')
        self.assertRequest(api_call, 'https://api.omise.co/charges/chrg_test')

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2014-11-20T14:17:24+07:00",
            "offset": 0,
            "limit": 20,
            "total": 2,
            "data": [
                {
                    "object": "charge",
                    "id": "chrg_test_1",
                    "livemode": false,
                    "location": "/charges/chrg_test_1",
                    "amount": 200000,
                    "currency": "thb",
                    "description": "on Johns mastercard",
                    "capture": true,
                    "authorized": false,
                    "captured": false,
                    "transaction": null,
                    "failure_code": null,
                    "failure_message": null,
                    "refunded": 0,
                    "refunds": {
                        "object": "list",
                        "from": "1970-01-01T00:00:00+00:00",
                        "to": "2015-01-26T16:20:43+00:00",
                        "offset": 0,
                        "limit": 20,
                        "total": 0,
                        "data": [],
                        "location": "/charges/chrg_test_1/refunds"
                    },
                    "card": {
                        "object": "card",
                        "id": "card_test_1",
                        "livemode": false,
                        "location": "/customers/cust_test/cards/card_test_1",
                        "country": "us",
                        "city": null,
                        "postal_code": null,
                        "financing": "debit",
                        "last_digits": "4242",
                        "brand": "Visa",
                        "expiration_month": 10,
                        "expiration_year": 2018,
                        "fingerprint": null,
                        "name": "john_mastercard",
                        "security_code_check": false,
                        "created": "2014-11-20T01:30:37Z"
                    },
                    "customer": "cust_test",
                    "ip": "133.71.33.7",
                    "created": "2014-11-20T01:32:07Z"
                },
                {
                    "object": "charge",
                    "id": "chrg_test_2",
                    "livemode": false,
                    "location": "/charges/chrg_test_2",
                    "amount": 100000,
                    "currency": "thb",
                    "description": "on Johns personal visa",
                    "capture": true,
                    "authorized": false,
                    "captured": false,
                    "transaction": null,
                    "failure_code": null,
                    "failure_message": null,
                    "refunded": 0,
                    "refunds": {
                        "object": "list",
                        "from": "1970-01-01T00:00:00+00:00",
                        "to": "2015-01-26T16:20:43+00:00",
                        "offset": 0,
                        "limit": 20,
                        "total": 0,
                        "data": [],
                        "location": "/charges/chrg_test_2/refunds"
                    },
                    "card": {
                        "object": "card",
                        "id": "card_test_2",
                        "livemode": false,
                        "location": "/customers/cust_test/cards/card_test_2",
                        "country": "us",
                        "city": "Dunkerque",
                        "postal_code": "59140",
                        "financing": "debit",
                        "last_digits": "4242",
                        "brand": "Visa",
                        "expiration_month": 10,
                        "expiration_year": 2015,
                        "fingerprint": null,
                        "name": "john_personal_visa",
                        "security_code_check": false,
                        "created": "2014-11-20T01:30:27Z"
                    },
                    "customer": "cust_test",
                    "ip": "133.71.33.7",
                    "created": "2014-11-20T01:32:07Z"
                }
            ]
        }""")

        charges = class_.retrieve()
        self.assertTrue(isinstance(charges, collection_class_))
        self.assertTrue(isinstance(charges[0], class_))
        self.assertTrue(charges[0].id, 'chrg_test_1')
        self.assertTrue(charges[0].amount, 200000)
        self.assertTrue(charges[1].id, 'chrg_test_2')
        self.assertTrue(charges[1].amount, 100000)
        self.assertRequest(api_call, 'https://api.omise.co/charges')

    @mock.patch('requests.patch')
    def test_update(self, api_call):
        charge = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "charge",
            "id": "chrg_test",
            "livemode": false,
            "location": "/charges/chrg_test",
            "amount": 100000,
            "currency": "thb",
            "description": "New description",
            "capture": false,
            "authorized": true,
            "reversed": false,
            "captured": false,
            "transaction": null,
            "failure_code": null,
            "failure_message": null,
            "refunded": 0,
            "refunds": {
                "object": "list",
                "from": "1970-01-01T00:00:00+00:00",
                "to": "2015-01-26T16:20:43+00:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "data": [],
                "location": "/charges/chrg_test/refunds"
            },
            "card": {
                "object": "card",
                "id": "card_test",
                "livemode": false,
                "country": "th",
                "city": "Bangkok",
                "postal_code": "10320",
                "financing": "credit",
                "last_digits": "4242",
                "brand": "Visa",
                "expiration_month": 10,
                "expiration_year": 2018,
                "fingerprint": "098f6bcd4621d373cade4e832627b4f6",
                "name": "Somchai Prasert",
                "created": "2014-10-20T09:41:56Z"
            },
            "customer": null,
            "ip": "127.0.0.1",
            "created": "2014-10-21T11:12:28Z"
        }""")

        self.assertTrue(isinstance(charge, class_))
        self.assertEqual(charge.description, 'Order-384')
        charge.description = 'New description'
        charge.update()

        self.assertEqual(charge.description, 'New description')
        self.assertRequest(
            api_call,
            'https://api.omise.co/charges/chrg_test',
            {'description': 'New description'}
        )

    @mock.patch('requests.post')
    def test_capture(self, api_call):
        charge = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "charge",
            "id": "chrg_test",
            "livemode": false,
            "location": "/charges/chrg_test",
            "amount": 100000,
            "currency": "thb",
            "description": "New description",
            "capture": false,
            "authorized": true,
            "reversed": false,
            "captured": true,
            "transaction": null,
            "failure_code": null,
            "failure_message": null,
            "refunded": 0,
            "refunds": {
                "object": "list",
                "from": "1970-01-01T00:00:00+00:00",
                "to": "2015-01-26T16:20:43+00:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "data": [],
                "location": "/charges/chrg_test/refunds"
            },
            "card": {
                "object": "card",
                "id": "card_test",
                "livemode": false,
                "country": "th",
                "city": "Bangkok",
                "postal_code": "10320",
                "financing": "credit",
                "last_digits": "4242",
                "brand": "Visa",
                "expiration_month": 10,
                "expiration_year": 2018,
                "fingerprint": "098f6bcd4621d373cade4e832627b4f6",
                "name": "Somchai Prasert",
                "created": "2014-10-20T09:41:56Z"
            },
            "customer": null,
            "ip": "127.0.0.1",
            "created": "2014-10-21T11:12:28Z"
        }""")

        self.assertTrue(isinstance(charge, class_))
        self.assertFalse(charge.captured)
        charge.capture()

        self.assertTrue(charge.captured)
        self.assertRequest(
            api_call,
            'https://api.omise.co/charges/chrg_test/capture',
        )

    @mock.patch('requests.post')
    def test_reverse(self, api_call):
        charge = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "charge",
            "id": "chrg_test",
            "livemode": false,
            "location": "/charges/chrg_test",
            "amount": 100000,
            "currency": "thb",
            "description": "New description",
            "capture": false,
            "authorized": true,
            "reversed": true,
            "captured": false,
            "transaction": null,
            "failure_code": null,
            "failure_message": null,
            "refunded": 0,
            "refunds": {
                "object": "list",
                "from": "1970-01-01T00:00:00+00:00",
                "to": "2015-01-26T16:20:43+00:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "data": [],
                "location": "/charges/chrg_test/refunds"
            },
            "card": {
                "object": "card",
                "id": "card_test",
                "livemode": false,
                "country": "th",
                "city": "Bangkok",
                "postal_code": "10320",
                "financing": "credit",
                "last_digits": "4242",
                "brand": "Visa",
                "expiration_month": 10,
                "expiration_year": 2018,
                "fingerprint": "098f6bcd4621d373cade4e832627b4f6",
                "name": "Somchai Prasert",
                "created": "2014-10-20T09:41:56Z"
            },
            "customer": null,
            "ip": "127.0.0.1",
            "created": "2014-10-21T11:12:28Z"
        }""")

        self.assertTrue(isinstance(charge, class_))
        self.assertFalse(charge.reversed)
        charge.reverse()

        self.assertTrue(charge.reversed)
        self.assertRequest(
            api_call,
            'https://api.omise.co/charges/chrg_test/reverse',
        )

    @mock.patch('requests.get')
    @mock.patch('requests.post')
    def test_refund(self, api_call, reload_call):
        charge = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "refund",
            "id": "rfnd_test",
            "location": "/charges/chrg_test/refunds/rfnd_test",
            "amount": 10000,
            "currency": "thb",
            "charge": "chrg_test",
            "transaction": null,
            "created": "2015-01-26T16:17:26Z"
        }""")

        self.mockResponse(reload_call, """{
            "object": "charge",
            "id": "chrg_test",
            "livemode": false,
            "location": "/charges/chrg_test",
            "amount": 100000,
            "currency": "thb",
            "description": "New description",
            "capture": true,
            "authorized": true,
            "reversed": false,
            "captured": true,
            "transaction": null,
            "failure_code": null,
            "failure_message": null,
            "refunded": 10000,
            "refunds": {
                "object": "list",
                "from": "1970-01-01T00:00:00+00:00",
                "to": "2015-01-26T16:20:43+00:00",
                "offset": 0,
                "limit": 20,
                "total": 1,
                "data": [
                    {
                        "object": "refund",
                        "id": "rfnd_test_1",
                        "location": "/charges/chrg_test/refunds/rfnd_test_1",
                        "amount": 10000,
                        "currency": "thb",
                        "charge": "chrg_test",
                        "transaction": null,
                        "created": "2015-01-26T15:06:16Z"
                    }
                ],
                "location": "/charges/chrg_test/refunds"
            },
            "card": {
                "object": "card",
                "id": "card_test",
                "livemode": false,
                "country": "th",
                "city": "Bangkok",
                "postal_code": "10320",
                "financing": "credit",
                "last_digits": "4242",
                "brand": "Visa",
                "expiration_month": 10,
                "expiration_year": 2018,
                "fingerprint": "098f6bcd4621d373cade4e832627b4f6",
                "name": "Somchai Prasert",
                "created": "2014-10-20T09:41:56Z"
            },
            "customer": null,
            "ip": "127.0.0.1",
            "created": "2014-10-21T11:12:28Z"
        }""")

        self.assertTrue(isinstance(charge, class_))

        refund = charge.refund(amount=10000)
        self.assertEqual(refund.amount, 10000)
        self.assertEqual(charge.refunded, 10000)

        self.assertRequest(
            api_call,
            'https://api.omise.co/charges/chrg_test/refunds',
            {'amount': 10000}
        )

    @mock.patch('requests.get')
    def test_schedule(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2017-06-02T12:34:43+07:00",
            "offset": 0,
            "limit": 20,
            "total": 1,
            "order": "chronological",
            "location": "/charges/schedules",
            "data": [
                {
                    "object": "schedule",
                    "id": "schd_test",
                    "livemode": false,
                    "location": "/schedules/schd_test",
                    "status": "active",
                    "deleted": false,
                    "every": 1,
                    "period": "month",
                    "on": {
                        "weekday_of_month": "2nd_monday"
                    },
                    "in_words": "Every 1 month(s) on the 2nd Monday",
                    "start_date": "2017-06-02",
                    "end_date": "2018-05-01",
                    "charge": {
                        "amount": 100000,
                        "currency": "thb",
                        "description": "Membership fee",
                        "customer": "cust_test_58655j2ez4elik6t2xc",
                        "card": null
                    },
                    "occurrences": {
                        "object": "list",
                        "from": "1970-01-01T07:00:00+07:00",
                        "to": "2017-06-02T19:14:21+07:00",
                        "offset": 0,
                        "limit": 20,
                        "total": 0,
                        "order": null,
                        "location": "/schedules/schd_test/occurrences",
                        "data": []
                    },
                    "next_occurrence_dates": [
                        "2017-06-12",
                        "2017-07-10",
                        "2017-08-14",
                        "2017-09-11",
                        "2017-10-09",
                        "2017-11-13",
                        "2017-12-11",
                        "2018-01-08",
                        "2018-02-12",
                        "2018-03-12",
                        "2018-04-09"
                    ],
                    "created": "2017-06-02T12:14:21Z"
                }
            ]
        }""")

        schedules = class_.schedule()
        self.assertTrue(isinstance(schedules, collection_class_))
        self.assertEqual(schedules.total, 1)
        self.assertEqual(schedules.location, '/charges/schedules')
        self.assertEqual(schedules[0].period, 'month')
        self.assertEqual(schedules[0].status, 'active')
        self.assertEqual(schedules[0].start_date, '2017-06-02')
        self.assertEqual(schedules[0].end_date, '2018-05-01')
        self.assertRequest(api_call, 'https://api.omise.co/charges/schedules')
