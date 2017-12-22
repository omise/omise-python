import mock
import unittest

from .helper import _ResourceMixin


class CustomerTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Customer
        return Customer

    def _getCardClass(self):
        from .. import Card
        return Card

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'customer',
            'description': 'John Doe (id: 30)',
            'created': '2014-10-24T08:26:46Z',
            'livemode': False,
            'email': 'john.doe@example.com',
            'default_card': 'card_test',
            'location': '/customers/cust_test',
            'cards': {
                'from': '1970-01-01T07:00:00+07:00',
                'object': 'list',
                'to': '2014-10-24T15:32:31+07:00',
                'limit': 20,
                'location': '/customers/cust_test/cards',
                'offset': 0,
                'total': 1,
                'data': [
                    {
                        'city': None,
                        'financing': '',
                        'object': 'card',
                        'expiration_year': 2017,
                        'last_digits': '4242',
                        'created': '2014-10-24T08:26:07Z',
                        'country': '',
                        'brand': 'Visa',
                        'livemode': False,
                        'expiration_month': 9,
                        'postal_code': None,
                        'location': '/customers/cust_test/cards/card_test',
                        'fingerprint': '098f6bcd4621d373cade4e832627b4f6',
                        'id': 'card_test',
                        'name': 'Test card'
                    }
                ]
            },
            'id': 'cust_test'
        })

    @mock.patch('requests.post')
    def test_create(self, api_call):
        class_ = self._getTargetClass()
        card_class_ = self._getCardClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
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
         }""")

        customer = class_.create(
            description='John Doe (id: 30)',
            email='john.doe@example.com',
            card='tokn_test',
        )

        self.assertTrue(isinstance(customer, class_))
        self.assertTrue(isinstance(customer.cards, collection_class_))
        self.assertTrue(isinstance(customer.cards[0], card_class_))
        self.assertEqual(customer.id, 'cust_test')
        self.assertEqual(customer.description, 'John Doe (id: 30)')
        self.assertEqual(customer.email, 'john.doe@example.com')
        self.assertEqual(customer.cards[0].id, 'card_test')
        self.assertEqual(customer.cards[0].last_digits, '4242')
        self.assertRequest(
            api_call,
            'https://api.omise.co/customers',
            {
                'description': 'John Doe (id: 30)',
                'email': 'john.doe@example.com',
                'card': 'tokn_test',
            }
        )

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        card_class_ = self._getCardClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "customer",
            "id": "cust_test",
            "livemode": false,
            "location": "/customers/cust_test",
            "default_card": "card_test",
            "email": "john.doe@example.com",
            "description": "John Doe (id: 30)",
            "created": "2014-10-24T08:26:46Z",
            "cards": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2014-10-24T15:32:31+07:00",
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
        }""")

        customer = class_.retrieve('cust_test')
        self.assertTrue(isinstance(customer, class_))
        self.assertTrue(isinstance(customer.cards, collection_class_))
        self.assertTrue(isinstance(customer.cards[0], card_class_))
        self.assertEqual(customer.id, 'cust_test')
        self.assertEqual(customer.description, 'John Doe (id: 30)')
        self.assertEqual(customer.email, 'john.doe@example.com')
        self.assertEqual(customer.cards[0].id, 'card_test')
        self.assertEqual(customer.cards[0].last_digits, '4242')
        self.assertRequest(api_call, 'https://api.omise.co/customers/cust_test')

        self.mockResponse(api_call, """{
            "object": "customer",
            "id": "cust_test",
            "livemode": false,
            "location": "/customers/cust_test",
            "default_card": "card_test",
            "email": "john.smith@example.com",
            "description": "John Doe (id: 30)",
            "created": "2014-10-24T08:26:46Z",
            "cards": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2014-10-24T15:32:31+07:00",
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
        }""")

        customer.reload()
        self.assertEqual(customer.email, 'john.smith@example.com')
        self.assertRequest(api_call, 'https://api.omise.co/customers/cust_test')

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
                    "object": "customer",
                    "id": "cust_test",
                    "livemode": false,
                    "location": "/customers/cust_test",
                    "default_card": "card_test",
                    "email": "john.smith@example.com",
                    "description": "John Doe (id: 30)",
                    "created": "2014-10-24T08:26:46Z",
                    "cards": {
                        "object": "list",
                        "from": "1970-01-01T07:00:00+07:00",
                        "to": "2014-10-24T15:32:31+07:00",
                        "offset": 0,
                        "limit": 20,
                        "total": 1,
                        "order": null,
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

        customers = class_.retrieve()
        self.assertTrue(isinstance(customers, collection_class_))
        self.assertTrue(isinstance(customers[0], class_))
        self.assertTrue(customers[0].email, 'john.smith@example.com')
        self.assertRequest(api_call, 'https://api.omise.co/customers')

    @mock.patch('requests.patch')
    def test_update(self, api_call):
        customer = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "customer",
            "id": "cust_test",
            "livemode": false,
            "location": "/customers/cust_test",
            "default_card": "card_test",
            "email": "john.smith@example.com",
            "description": "Another description",
            "created": "2014-10-24T08:26:46Z",
            "cards": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2014-10-24T15:32:31+07:00",
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
        }""")

        self.assertTrue(isinstance(customer, class_))
        self.assertEqual(customer.description, 'John Doe (id: 30)')
        self.assertEqual(customer.email, 'john.doe@example.com')

        customer.description = 'Another description'
        customer.email = 'john.smith@example.com'
        customer.update()

        self.assertEqual(customer.description, 'Another description')
        self.assertEqual(customer.email, 'john.smith@example.com')
        self.assertRequest(
            api_call,
            'https://api.omise.co/customers/cust_test',
            {
                'description': 'Another description',
                'email': 'john.smith@example.com',
            }
        )

    @mock.patch('requests.delete')
    def test_destroy(self, api_call):
        customer = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "customer",
            "id": "cust_test",
            "livemode": false,
            "deleted": true
        }""")

        self.assertTrue(isinstance(customer, class_))
        self.assertEqual(customer.email, 'john.doe@example.com')

        customer.destroy()
        self.assertTrue(customer.destroyed)
        self.assertRequest(api_call, 'https://api.omise.co/customers/cust_test')

    @mock.patch('requests.get')
    def test_schedule(self, api_call):
        customer = self._makeOne()
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
            "location": "/customers/cust_test/schedules",
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

        self.assertTrue(isinstance(customer, class_))

        schedules = customer.schedule()
        self.assertTrue(isinstance(schedules, collection_class_))
        self.assertEqual(schedules.total, 1)
        self.assertEqual(schedules.location, '/customers/cust_test/schedules')
        self.assertEqual(schedules[0].period, 'month')
        self.assertEqual(schedules[0].status, 'active')
        self.assertEqual(schedules[0].start_date, '2017-06-02')
        self.assertEqual(schedules[0].end_date, '2018-05-01')

        self.assertRequest(
            api_call,
            'https://api.omise.co/customers/cust_test/schedules'
        )
