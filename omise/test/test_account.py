import mock
import unittest

from .helper import _ResourceMixin


class AccountTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Account
        return Account

    def _makeOne(self):
        return self._getTargetClass().from_data({
            "object": "account",
            "location": "/account",
            "id": "acct_test",
            "email": None,
            "created": "2014-10-20T08:21:42Z",
            "chain_enabled": False
        })

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "account",
            "id": "acct_test",
            "email": null,
            "created": "2014-10-20T08:21:42Z"
        }""")

        account = class_.retrieve()
        self.assertTrue(isinstance(account, class_))
        self.assertEqual(account.id, 'acct_test')
        self.assertEqual(account.created, '2014-10-20T08:21:42Z')
        self.assertRequest(api_call, 'https://api.omise.co/account')

        self.mockResponse(api_call, """{
            "object": "account",
            "id": "acct_foo",
            "email": null,
            "created": "2014-10-20T08:21:42Z"
        }""")

        account.reload()
        self.assertEqual(account.id, 'acct_foo')
        self.assertRequest(api_call, 'https://api.omise.co/account')


    @mock.patch('requests.patch')
    def test_update(self, api_call):
        account = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
          "object": "account",
          "id": "account_test_no1t4tnemucod0e51mo",
          "team": "acct_no1t4tnemucod0e51mo",
          "livemode": false,
          "location": "/account",
          "country": "TH",
          "currency": "THB",
          "email": "somchai.prasert@example.com",
          "created_at": "2019-12-31T12:59:59Z",
          "supported_currencies": [
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
          "api_version": "2019-05-29",
          "auto_activate_recipients": true,
          "chain_enabled": true,
          "zero_interest_installments": true,
          "chain_return_uri": "https://omise-flask-example.herokuapp.com",
          "webhook_uri": "https://omise-flask-example.herokuapp.com/webhook",
          "metadata_export_keys": {
            "charge": [
              "color",
              "order_id"
            ]
          }
        }""")

        self.assertTrue(isinstance(account, class_))
        self.assertFalse(account.chain_enabled)
        account.update(chain_enabled=True)
        self.assertTrue(account.chain_enabled)
        self.assertRequest(
            api_call,
            'https://api.omise.co/account',
            {
                'chain_enabled': True,
            }
        )
