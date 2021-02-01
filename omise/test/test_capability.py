import mock
import unittest

from .helper import _ResourceMixin


class CapabilityTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Capability
        return Capability

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'capability',
            'location': '/capability',
            'payment_methods': [
                {
                "object": "payment_method",
                "name": "card",
                "currencies": [
                    "THB",
                    "JPY",
                    "USD",
                    "EUR",
                    "GBP",
                    "SGD",
                    "AUD",
                    "CHF",
                    "CNY",
                    "DKK",
                    "HKD"
                ],
                "card_brands": [
                    "JCB",
                    "Visa",
                    "MasterCard"
                ],
                "installment_terms": None
                },
                {
                "object": "payment_method",
                "name": "alipay",
                "currencies": [
                  "THB"
                ],
                "card_brands": None,
                "installment_terms": None
                }
            ],
            'country': 'TH',
            'zero_interest_installments': True
        })

    @mock.patch('requests.get')
    def test_reload(self, api_call):
        capability = self._makeOne()
        class_ = self._getTargetClass()

        self.assertTrue(isinstance(capability, class_))
        self.assertTrue(capability.zero_interest_installments)

        self.mockResponse(api_call, """{
            "zero_interest_installments": false
        }""")

        capability.reload()
        self.assertFalse(capability.zero_interest_installments)
        self.assertRequest(api_call, 'https://api.omise.co/capability')

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "capability",
            "location": "/capability",
            "payment_methods": [
                {
                "object": "payment_method",
                "name": "card",
                "currencies": [
                    "THB",
                    "JPY",
                    "USD",
                    "EUR",
                    "GBP",
                    "SGD",
                    "AUD",
                    "CHF",
                    "CNY",
                    "DKK",
                    "HKD"
                ],
                "card_brands": [
                    "JCB",
                    "Visa",
                    "MasterCard"
                ],
                "installment_terms": null
                },
                {
                "object": "payment_method",
                "name": "alipay",
                "currencies": [
                  "THB"
                ],
                "card_brands": null,
                "installment_terms": null               
                }
            ],
            "country": "TH",
            "zero_interest_installments": true
        }""")

        capability = class_.retrieve()
        self.assertTrue(isinstance(capability, class_))
        self.assertEqual(capability.country, 'TH')
        self.assertTrue(capability.zero_interest_installments)
        self.assertRequest(api_call, 'https://api.omise.co/capability')
