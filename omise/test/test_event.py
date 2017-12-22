import mock
import unittest

from .helper import _ResourceMixin


class EventTest(_ResourceMixin, unittest.TestCase):
    def _getTargetClass(self):
        from .. import Event
        return Event

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _getChargeClass(self):
        from .. import Charge
        return Charge

    def _getCardClass(self):
        from .. import Card
        return Card

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "event",
            "id": "evnt_test",
            "livemode": false,
            "location": "/events/evnt_test",
            "key": "charge.create",
            "created": "2015-06-02T05:41:53Z",
            "data": {
                "amount": 500000,
                "authorize_uri": "https://example.com/paym_test/authorize",
                "authorized": true,
                "capture": true,
                "captured": true,
                "card": {
                    "bank": "",
                    "brand": "Visa",
                    "city": null,
                    "country": "us",
                    "created": "2015-11-20T04:33:18Z",
                    "expiration_month": 8,
                    "expiration_year": 2016,
                    "financing": "",
                    "fingerprint": "FooBar",
                    "id": "card_test",
                    "last_digits": "4242",
                    "livemode": false,
                    "name": "Foo Bar",
                    "object": "card",
                    "postal_code": null,
                    "security_code_check": true
                },
                "created": "2015-11-20T04:33:19Z",
                "currency": "thb",
                "customer": null,
                "description": "Foo bar",
                "dispute": null,
                "failure_code": null,
                "failure_message": null,
                "id": "chrg_test",
                "ip": null,
                "livemode": false,
                "location": "/charges/chrg_test",
                "object": "charge",
                "reference": "paym_test",
                "refunded": 0,
                "refunds": {
                    "data": [],
                    "from": "1970-01-01T00:00:00+00:00",
                    "limit": 20,
                    "location": "/charges/chrg_test_52322mr6iobyag0omxx/refunds",
                    "object": "list",
                    "offset": 0,
                    "to": "2015-11-20T04:33:19+00:00",
                    "total": 0
                },
                "return_uri": "http://example.com/",
                "status": "successful",
                "transaction": "trxn_test"
            }
        }""")

        event = class_.retrieve('evnt_test')
        self.assertTrue(isinstance(event, class_))
        self.assertFalse(event.livemode)
        self.assertEqual(event.id, 'evnt_test')
        self.assertEqual(event.key, 'charge.create')

        charge = event.data
        self.assertEqual(charge.object, 'charge')
        self.assertEqual(charge.id, 'chrg_test')
        self.assertEqual(charge.amount, 500000)

        card = charge.card
        self.assertEqual(card.object, 'card')
        self.assertEqual(card.id, 'card_test')
        self.assertEqual(card.name, 'Foo Bar')
        self.assertEqual(card.brand, 'Visa')

        self.assertRequest(
            api_call,
            'https://api.omise.co/events/evnt_test')

        event.reload()
        self.assertEqual(event.id, 'evnt_test')

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
                    "object": "event",
                    "id": "evnt_test",
                    "livemode": false,
                    "location": "/events/evnt_test",
                    "key": "charge.create",
                    "created": "2015-06-02T05:41:53Z"
                }
            ]
        }""")

        events = class_.retrieve()
        self.assertTrue(isinstance(events, collection_class_))
        self.assertTrue(isinstance(events[0], class_))
        self.assertTrue(events[0].id, 'evnt_test')
        self.assertTrue(events[0].key, 'charge.create')
        self.assertRequest(api_call, 'https://api.omise.co/events')
