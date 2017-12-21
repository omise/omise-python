import mock
import unittest

from .helper import _ResourceMixin


class TokenTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Token
        return Token

    def _getCardClass(self):
        from .. import Card
        return Card

    @mock.patch('requests.post')
    def test_create(self, api_call):
        class_ = self._getTargetClass()
        card_class_ = self._getCardClass()
        self.mockResponse(api_call, """{
            "object": "token",
            "id": "tokn_test",
            "livemode": false,
            "location": "/tokens/tokn_test",
            "used": false,
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
            "created": "2014-10-20T09:41:56Z"
        }""")

        token = class_.create(
            name='Somchai Prasert',
            number='4242424242424242',
            expiration_month=10,
            expiration_year=2018,
            city='Bangkok',
            postal_code='10320',
            security_code=123
        )

        self.assertTrue(isinstance(token, class_))
        self.assertTrue(isinstance(token.card, card_class_))
        self.assertEqual(token.id, 'tokn_test')
        self.assertEqual(token.card.id, 'card_test')
        self.assertEqual(token.card.last_digits, '4242')
        self.assertRequest(api_call, 'https://vault.omise.co/tokens', {
            'card': {
                'name': 'Somchai Prasert',
                'number': '4242424242424242',
                'expiration_month': 10,
                'expiration_year': 2018,
                'city': 'Bangkok',
                'postal_code': '10320',
                'security_code': 123
            }
        })

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        card_class_ = self._getCardClass()
        self.mockResponse(api_call, """{
            "object": "token",
            "id": "tokn_test",
            "livemode": false,
            "location": "/tokens/tokn_test",
            "used": false,
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
            "created": "2014-10-20T09:41:56Z"
        }""")

        token = class_.retrieve('tokn_test')
        self.assertTrue(isinstance(token, class_))
        self.assertTrue(isinstance(token.card, card_class_))
        self.assertFalse(token.used)
        self.assertEqual(token.id, 'tokn_test')
        self.assertEqual(token.card.id, 'card_test')
        self.assertEqual(token.card.last_digits, '4242')
        self.assertRequest(api_call, 'https://vault.omise.co/tokens/tokn_test')

        self.mockResponse(api_call, """{
            "object": "token",
            "id": "tokn_test",
            "livemode": false,
            "location": "/tokens/tokn_test",
            "used": true,
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
            "created": "2014-10-20T09:41:56Z"
        }""")

        token.reload()
        self.assertEqual(token.id, 'tokn_test')
        self.assertTrue(token.used)
        self.assertRequest(api_call, 'https://vault.omise.co/tokens/tokn_test')
