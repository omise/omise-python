import mock
import unittest

from .helper import _ResourceMixin


class CardTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Card
        return Card

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'city': 'Bangkok',
            'financing': '',
            'object': 'card',
            'expiration_year': 2016,
            'last_digits': '4242',
            'created': '2014-10-21T04:04:12Z',
            'country': '',
            'brand': 'Visa',
            'livemode': False,
            'expiration_month': 10,
            'postal_code': '10320',
            'location': '/customers/cust_test/cards/card_test',
            'fingerprint': '098f6bcd4621d373cade4e832627b4f6',
            'id': 'card_test',
            'name': 'Somchai Prasert'
        })

    @mock.patch('requests.get')
    def test_reload(self, api_call):
        card = self._makeOne()
        class_ = self._getTargetClass()

        self.assertTrue(isinstance(card, class_))
        self.assertEqual(card.id, 'card_test')
        self.assertEqual(card.name, 'Somchai Prasert')

        self.mockResponse(api_call, """{
            "object": "card",
            "id": "card_test",
            "livemode": false,
            "location": "/customers/cust_test/cards/card_test",
            "country": "",
            "city": "Bangkok",
            "postal_code": "10310",
            "financing": "",
            "last_digits": "4242",
            "brand": "Visa",
            "expiration_month": 12,
            "expiration_year": 2018,
            "fingerprint": "098f6bcd4621d373cade4e832627b4f6",
            "name": "S. Prasert",
            "created": "2014-10-21T04:04:12Z"
        }""")

        card.reload()
        self.assertEqual(card.id, 'card_test')
        self.assertEqual(card.name, 'S. Prasert')
        self.assertRequest(
            api_call,
            'https://api.omise.co/customers/cust_test/cards/card_test'
        )

    @mock.patch('requests.patch')
    def test_update(self, api_call):
        card = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "card",
            "id": "card_test",
            "livemode": false,
            "location": "/customers/cust_test/cards/card_test",
            "country": "",
            "city": "Bangkok",
            "postal_code": "10310",
            "financing": "",
            "last_digits": "4242",
            "brand": "Visa",
            "expiration_month": 12,
            "expiration_year": 2018,
            "fingerprint": "098f6bcd4621d373cade4e832627b4f6",
            "name": "Example User",
            "created": "2014-10-21T04:04:12Z"
        }""")

        self.assertTrue(isinstance(card, class_))
        self.assertEqual(card.name, 'Somchai Prasert')
        self.assertEqual(card.expiration_month, 10)
        self.assertEqual(card.expiration_year, 2016)
        card.name = 'Example User'
        card.expiration_month = 12
        card.expiration_year = 2018
        card.update()

        self.assertEqual(card.name, 'Example User')
        self.assertEqual(card.expiration_month, 12)
        self.assertEqual(card.expiration_year, 2018)
        self.assertRequest(
            api_call,
            'https://api.omise.co/customers/cust_test/cards/card_test',
            {
                'name': 'Example User',
                'expiration_month': 12,
                'expiration_year': 2018,
            }
        )

    @mock.patch('requests.delete')
    def test_destroy(self, api_call):
        card = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "card",
            "id": "card_test",
            "livemode": false,
            "deleted": true
        }""")

        self.assertTrue(isinstance(card, class_))
        self.assertEqual(card.name, 'Somchai Prasert')

        card.destroy()
        self.assertTrue(card.destroyed)
        self.assertRequest(
            api_call,
            'https://api.omise.co/customers/cust_test/cards/card_test'
        )
