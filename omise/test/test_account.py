import mock
import unittest

from .helper import _ResourceMixin


class AccountTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Account
        return Account

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
