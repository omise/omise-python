import sys
import unittest
import mock


try:
    import json
except ImportError:
    import simplejson as json


try:
    basestring
except NameError:
    basestring = str


if sys.version_info[0] == 2:
    def next(o, **kw):
        return o.next(**kw)


class _MockResponse(object):

    def __init__(self, content):
        self._content = content

    def json(self):
        return json.loads(self._content)


class _RequestAssertable(object):

    def mockResponse(self, api_call, response):
        api_call.return_value = response = _MockResponse(response)
        return response

    def assertRequest(self, api_call, url, data=None, headers=None):
        if data is None:
            data = {}
        if headers is None:
            headers = mock.ANY
        api_call.assert_called_with(
            url,
            data=json.dumps(data, sort_keys=True),
            headers=headers,
            auth=(mock.ANY, ''),
            verify=mock.ANY)


class RequestTest(_RequestAssertable, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Request
        return Request

    def test_init(self):
        class_ = self._getTargetClass()
        request = class_('skey_test', 'https://api.omise.co', '2015-11-01')
        self.assertEqual(request.api_key, 'skey_test')
        self.assertEqual(request.api_base, 'https://api.omise.co')
        self.assertEqual(request.api_version, '2015-11-01')

    def test_init_no_api_key(self):
        class_ = self._getTargetClass()
        def _func():
            class_(None, 'https://api.omise.co', '2015-11-01')
        self.assertRaises(AttributeError, _func)

    @mock.patch('requests.get')
    def test_send(self, api_call):
        from ..version import __VERSION__
        class_ = self._getTargetClass()
        request = class_('skey_test', 'https://api.omise.co', '2015-11-01')
        self.mockResponse(api_call, '{"ping":"pong"}')
        self.assertEqual(request.send('get', 'ping'), {'ping': 'pong'})
        self.assertRequest(api_call, 'https://api.omise.co/ping', headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Omise-Version': '2015-11-01',
            'User-Agent': 'OmisePython/%s' % __VERSION__
        })

    @mock.patch('requests.get')
    def test_send_tuple_url(self, api_call):
        class_ = self._getTargetClass()
        request = class_('skey_test', 'https://api.omise.co', '2015-11-01')
        self.mockResponse(api_call, '{"ping":"pong"}')
        self.assertEqual(request.send('get', ('ping', 1)), {'ping': 'pong'})
        self.assertRequest(api_call, 'https://api.omise.co/ping/1')

    @mock.patch('requests.get')
    def test_send_no_version(self, api_call):
        from ..version import __VERSION__
        class_ = self._getTargetClass()
        request = class_('skey_test', 'https://api.omise.co', None)
        self.mockResponse(api_call, '{"ping":"pong"}')
        self.assertEqual(request.send('get', 'ping'), {'ping': 'pong'})
        self.assertRequest(api_call, 'https://api.omise.co/ping', headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'OmisePython/%s' % __VERSION__
        })

    @mock.patch('requests.post')
    def test_send_post(self, api_call):
        class_ = self._getTargetClass()
        request = class_('skey_test', 'https://api.omise.co', '2015-11-01')
        params = {'test': 'request'}
        self.mockResponse(api_call, '{"ping":"pong"}')
        self.assertEqual(request.send('post', 'ping', params), {'ping': 'pong'})
        self.assertRequest(api_call, 'https://api.omise.co/ping', params)


class _ResourceMixin(_RequestAssertable, unittest.TestCase):

    def setUp(self):
        self._secret_mocker = mock.patch('omise.api_secret', 'skey_test')
        self._public_mocker = mock.patch('omise.api_public', 'pkey_test')
        self._secret_mocker.start()
        self._public_mocker.start()

    def tearDown(self):
        self._secret_mocker.stop()
        self._public_mocker.stop()

    def _getTargetClass(self):
        from .. import Base
        return Base

    def test_from_data(self):
        class_ = self._getTargetClass()
        instance = class_.from_data({'id': 'tst_data', 'description': 'foo'})
        self.assertEqual(instance.id, 'tst_data')
        self.assertEqual(instance.description, 'foo')
        self.assertEqual(instance.changes, {})

    def test_repr(self):
        class_ = self._getTargetClass()
        instance = class_.from_data({'id': 'tst_data'})
        self.assertEqual(
            repr(instance),
            "<%s id='%s' at %s>" % (
                class_.__name__,
                'tst_data',
                hex(id(instance)),
            )
        )

    def test_repr_without_id(self):
        class_ = self._getTargetClass()
        instance = class_.from_data({})
        self.assertEqual(
            repr(instance),
            "<%s at %s>" % (
                class_.__name__,
                hex(id(instance)),
            )
        )

    def test_changes(self):
        class_ = self._getTargetClass()
        instance = class_.from_data({'id': 'tst_data', 'description': 'foo'})
        instance.description = 'foobar'
        instance.email = 'foo@example.com'
        self.assertEqual(instance.changes, {
            'description': 'foobar',
            'email': 'foo@example.com',
        })


class AccountTest(_ResourceMixin):

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


class BalanceTest(_ResourceMixin):

    def _getTargetClass(self):
        from .. import Balance
        return Balance

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "balance",
            "livemode": false,
            "available": 0,
            "total": 0,
            "currency": "thb"
        }""")

        balance = class_.retrieve()
        self.assertTrue(isinstance(balance, class_))
        self.assertEqual(balance.available, 0)
        self.assertEqual(balance.currency, 'thb')
        self.assertEqual(balance.total, 0)
        self.assertRequest(api_call, 'https://api.omise.co/balance')

        self.mockResponse(api_call, """{
            "object": "balance",
            "livemode": false,
            "available": 4294967295,
            "total": 0,
            "currency": "thb"
        }""")

        balance.reload()
        self.assertEqual(balance.available, 4294967295)
        self.assertRequest(api_call, 'https://api.omise.co/balance')


class TokenTest(_ResourceMixin):

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


class CardTest(_ResourceMixin):

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


class ChargeTest(_ResourceMixin):

    def _getTargetClass(self):
        from .. import Charge
        return Charge

    def _getCardClass(self):
        from .. import Card
        return Card

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


class CollectionTest(_ResourceMixin):

    def _getTargetClass(self):
        from .. import Collection
        return Collection

    def _getAccountClass(self):
        from .. import Account
        return Account

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'list',
            'data': [
                {'object': 'account', 'id': 'acct_test_1'},
                {'object': 'account', 'id': 'acct_test_2'},
                {'object': 'account', 'id': 'acct_test_3'},
                {'object': 'account', 'id': 'acct_test_4'},
            ]
        })

    def test_len(self):
        collection = self._makeOne()
        self.assertEqual(len(collection), 4)

    def test_iter(self):
        collection = self._makeOne()
        iterable = iter(collection)
        firstItem = next(iterable)
        self.assertTrue(isinstance(firstItem, self._getAccountClass()))
        self.assertEqual(firstItem.id, 'acct_test_1')
        self.assertEqual(next(iterable).id, 'acct_test_2')
        self.assertEqual(next(iterable).id, 'acct_test_3')
        self.assertEqual(next(iterable).id, 'acct_test_4')
        def _func():
            next(iterable)
        self.assertRaises(StopIteration, _func)

    def test_getitem(self):
        collection = self._makeOne()
        self.assertTrue(isinstance(collection[0], self._getAccountClass()))
        self.assertEqual(collection[0].id, 'acct_test_1')
        self.assertEqual(collection[3].id, 'acct_test_4')
        self.assertEqual(collection[-1].id, 'acct_test_4')

    def test_retrieve(self):
        collection = self._makeOne()
        firstItem = collection.retrieve('acct_test_1')
        self.assertTrue(isinstance(firstItem, self._getAccountClass()))
        self.assertEqual(firstItem.id, 'acct_test_1')
        self.assertEqual(collection.retrieve('acct_test_2').id, 'acct_test_2')
        self.assertEqual(collection.retrieve('acct_test_3').id, 'acct_test_3')
        self.assertEqual(collection.retrieve('acct_test_4').id, 'acct_test_4')
        self.assertEqual(collection.retrieve('acct_test_5'), None)

    def test_retrieve_no_args(self):
        collection = self._makeOne()
        def _extract_id(item):
            return item.id
        firstItem = collection.retrieve()[0]
        self.assertTrue(isinstance(firstItem, self._getAccountClass()))
        self.assertEqual(
            list(map(_extract_id, collection.retrieve())),
            list(map(_extract_id, list(collection)))
        )


class CustomerTest(_ResourceMixin):

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


class DisputeTest(_ResourceMixin):

    def _getTargetClass(self):
        from .. import Dispute
        return Dispute

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'dispute',
            'id': 'dspt_test',
            'livemode': False,
            'location': '/disputes/dspt_test',
            'amount': 100000,
            'currency': 'thb',
            'status': 'pending',
            'message': None,
            'charge': 'chrg_test',
            'created': '2015-03-23T05:24:39Z'
        })

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "dispute",
            "id": "dspt_test",
            "livemode": false,
            "location": "/disputes/dspt",
            "amount": 100000,
            "currency": "thb",
            "status": "pending",
            "message": null,
            "charge": "chrg_test",
            "created": "2015-03-23T05:24:39Z"
        }""")

        dispute = class_.retrieve('dspt_test')
        self.assertTrue(isinstance(dispute, class_))
        self.assertEqual(dispute.id, 'dspt_test')
        self.assertEqual(dispute.amount, 100000)
        self.assertEqual(dispute.currency, 'thb')
        self.assertEqual(dispute.status, 'pending')
        self.assertEqual(dispute.charge, 'chrg_test')
        self.assertEqual(dispute.message, None)

        self.assertRequest(
            api_call,
            'https://api.omise.co/disputes/dspt_test')

        self.mockResponse(api_call, """{
            "object": "dispute",
            "id": "dspt_test",
            "livemode": false,
            "location": "/disputes/dspt_test",
            "amount": 100000,
            "currency": "thb",
            "status": "pending",
            "message": "Foobar Baz",
            "charge": "chrg_test",
            "created": "2015-03-23T05:24:39Z"
        }""")

        dispute.reload()
        self.assertEqual(dispute.message, 'Foobar Baz')

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2015-03-23T05:24:39+07:00",
            "offset": 0,
            "limit": 20,
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
                    "message": "Foobar Baz",
                    "charge": "chrg_test",
                    "created": "2015-03-23T05:24:39Z"
                }
            ]
        }""")

        disputes = class_.retrieve()
        self.assertTrue(isinstance(disputes, collection_class_))
        self.assertTrue(isinstance(disputes[0], class_))
        self.assertTrue(disputes[0].id, 'dspt_test')
        self.assertTrue(disputes[0].amount, 100000)
        self.assertRequest(api_call, 'https://api.omise.co/disputes')

    @mock.patch('requests.get')
    def test_retrieve_kwargs(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2015-03-23T05:24:39+07:00",
            "offset": 0,
            "limit": 20,
            "total": 1,
            "data": [
                {
                    "object": "dispute",
                    "id": "dspt_test",
                    "livemode": false,
                    "location": "/disputes/dspt_test",
                    "amount": 100000,
                    "currency": "thb",
                    "status": "closed",
                    "message": "Foobar Baz",
                    "charge": "chrg_test",
                    "created": "2015-03-23T05:24:39Z"
                }
            ]
        }""")

        disputes = class_.retrieve('closed')
        self.assertTrue(isinstance(disputes, collection_class_))
        self.assertTrue(isinstance(disputes[0], class_))
        self.assertTrue(disputes[0].id, 'dspt_test')
        self.assertTrue(disputes[0].status, 'closed')
        self.assertRequest(api_call, 'https://api.omise.co/disputes/closed')

    @mock.patch('requests.patch')
    def test_update(self, api_call):
        dispute = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "dispute",
            "id": "dspt_test",
            "livemode": false,
            "location": "/disputes/dspt_test",
            "amount": 100000,
            "currency": "thb",
            "status": "pending",
            "message": "Foobar Baz",
            "charge": "chrg_test",
            "created": "2015-03-23T05:24:39Z"
        }""")

        self.assertTrue(isinstance(dispute, class_))
        self.assertEqual(dispute.message, None)
        dispute.message = 'Foobar Baz'
        dispute.update()

        self.assertEqual(dispute.message, 'Foobar Baz')
        self.assertRequest(
            api_call,
            'https://api.omise.co/disputes/dspt_test',
            {'message': 'Foobar Baz'}
        )


class EventTest(_ResourceMixin):
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

        charge_class_ = self._getChargeClass()
        charge = event.data
        self.assertEqual(charge.object, 'charge')
        self.assertEqual(charge.id, 'chrg_test')
        self.assertEqual(charge.amount, 500000)

        card_class_ = self._getCardClass()
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


class ForexTest(_ResourceMixin):

    def _getTargetClass(self):
        from .. import Forex
        return Forex

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "forex",
            "from": "thb",
            "to": "usd",
            "rate": 32.747069,
            "location": "/forex/usd"
        }""")

        forex = class_.retrieve('usd')
        self.assertTrue(isinstance(forex, class_))
        self.assertTrue(forex.to, 'usd')
        self.assertTrue(forex.rate, 32.747069)
        self.assertRequest(api_call, 'https://api.omise.co/forex/usd')


class LinkTest(_ResourceMixin):

    def _getTargetClass(self):
        from .. import Link
        return Link

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    @mock.patch('requests.post')
    def test_create(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "link",
            "id": "link_test",
            "livemode": false,
            "location": "/links/link_test",
            "amount": 10000,
            "currency": "thb",
            "used": false,
            "multiple": false,
            "description": "Description of order-384",
            "title": "Order-384",
            "charges": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2017-03-03T19:22:33+07:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "order": null,
                "location": "/links/link_test/charges",
                "data": []
            },
            "payment_uri": "http://link.example.com/0BB268C6",
            "created": "2017-03-03T12:16:48Z"
        }""")

        link = class_.create(
            amount=10000,
            currency='thb',
            description='Description of order-384',
            title='Order-384',
        )

        self.assertTrue(isinstance(link, class_))
        self.assertEqual(link.id, 'link_test')
        self.assertEqual(link.amount, 10000)
        self.assertEqual(link.currency, 'thb')
        self.assertEqual(link.description, 'Description of order-384')
        self.assertEqual(link.title, 'Order-384')
        self.assertRequest(
            api_call,
            'https://api.omise.co/links',
            {
                'amount': 10000,
                'currency': 'thb',
                'description': 'Description of order-384',
                'title': 'Order-384',
            }
        )

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "link",
            "id": "link_test",
            "livemode": false,
            "location": "/links/link_test",
            "amount": 10000,
            "currency": "thb",
            "used": false,
            "multiple": false,
            "description": "Description of order-384",
            "title": "Order-384",
            "charges": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2017-03-03T19:22:33+07:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "order": null,
                "location": "/links/link_test/charges",
                "data": []
            },
            "payment_uri": "http://link.example.com/0BB268C6",
            "created": "2017-03-03T12:16:48Z"
        }""")

        link = class_.retrieve('link_test')
        self.assertTrue(isinstance(link, class_))
        self.assertEqual(link.id, 'link_test')
        self.assertEqual(link.amount, 10000)
        self.assertEqual(link.currency, 'thb')
        self.assertEqual(link.description, 'Description of order-384')
        self.assertEqual(link.title, 'Order-384')
        self.assertRequest(api_call, 'https://api.omise.co/links/link_test')

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
                    "object": "link",
                    "id": "link_test_1",
                    "livemode": false,
                    "location": "/links/link_test_1",
                    "amount": 10000,
                    "currency": "thb",
                    "used": false,
                    "multiple": false,
                    "description": "Description of order-384",
                    "title": "Order-384",
                    "charges": {
                        "object": "list",
                        "from": "1970-01-01T07:00:00+07:00",
                        "to": "2017-03-03T19:22:33+07:00",
                        "offset": 0,
                        "limit": 20,
                        "total": 0,
                        "order": null,
                        "location": "/links/link_test_1/charges",
                        "data": []
                    },
                    "payment_uri": "http://link.example.com/0BB268C6",
                    "created": "2017-03-03T12:16:48Z"
                },
                {
                    "object": "link",
                    "id": "link_test_2",
                    "livemode": false,
                    "location": "/links/link_test_2",
                    "amount": 20000,
                    "currency": "thb",
                    "used": false,
                    "multiple": false,
                    "description": "Description of order-385",
                    "title": "Order-385",
                    "charges": {
                        "object": "list",
                        "from": "1970-01-01T07:00:00+07:00",
                        "to": "2017-03-03T19:22:33+07:00",
                        "offset": 0,
                        "limit": 20,
                        "total": 0,
                        "order": null,
                        "location": "/links/link_test_2/charges",
                        "data": []
                    },
                    "payment_uri": "http://link.example.com/0BB268C6",
                    "created": "2017-03-03T12:16:48Z"
                }
            ]
        }""")

        links = class_.retrieve()
        self.assertTrue(isinstance(links, collection_class_))
        self.assertTrue(isinstance(links[0], class_))
        self.assertTrue(links[0].id, 'link_test_1')
        self.assertTrue(links[0].amount, 10000)
        self.assertTrue(links[1].id, 'link_test_2')
        self.assertTrue(links[1].amount, 20000)
        self.assertRequest(api_call, 'https://api.omise.co/links')


class OccurrenceTest(_ResourceMixin):
    def _getTargetClass(self):
        from .. import Occurrence
        return Occurrence

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "occurrence",
            "id": "occu_test",
            "location": "/occurrences/occu_test",
            "schedule": "schd_test",
            "schedule_date": "2017-06-05",
            "retry_date": null,
            "processed_at": "2017-06-05T08:29:15Z",
            "status": "successful",
            "message": null,
            "result": "chrg_test",
            "created": "2017-06-05T08:29:13Z"
        }""")

        occurrence = class_.retrieve('occu_test')
        self.assertTrue(isinstance(occurrence, class_))
        self.assertRequest(
            api_call,
            'https://api.omise.co/occurrences/occu_test'
        )


class RecipientTest(_ResourceMixin):

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


class RefundTest(_ResourceMixin):

    def _getTargetClass(self):
        from .. import Refund
        return Refund

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'refund',
            'id': 'rfnd_test',
            'location': '/charges/chrg_test/refunds/rfnd_test',
            'amount': 10000,
            'currency': 'thb',
            'charge': 'chrg_test',
            'transaction': None,
            'created': '2015-01-26T15:06:16Z'
        })

    @mock.patch('requests.get')
    def test_reload(self, api_call):
        refund = self._makeOne()
        class_ = self._getTargetClass()

        self.assertTrue(isinstance(refund, class_))
        self.assertEqual(refund.transaction, None)

        self.mockResponse(api_call, """{
            "object": "refund",
            "id": "rfnd_test",
            "location": "/charges/chrg_test/refunds/rfnd_test",
            "amount": 10000,
            "currency": "thb",
            "charge": "chrg_test",
            "transaction": "trxn_test",
            "created": "2015-01-26T15:06:16Z"
        }""")

        refund.reload()
        self.assertEqual(refund.transaction, 'trxn_test')
        self.assertRequest(
            api_call,
            'https://api.omise.co/charges/chrg_test/refunds/rfnd_test'
        )


class SearchTest(_ResourceMixin):

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


class ScheduleTest(_ResourceMixin):
    def _getTargetClass(self):
        from .. import Schedule
        return Schedule

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            "object": "schedule",
            "id": "schd_test",
            "livemode": False,
            "location": "/schedules/schd_test",
            "status": "active",
            "deleted": False,
            "every": 1,
            "period": "month",
            "on": {
                "days_of_month": [
                    1
                ]
            },
            "in_words": "Every 1 month(s) on the 1st",
            "start_date": "2017-06-02",
            "end_date": "2018-06-02",
            "charge": {
                "amount": 100000,
                "currency": "thb",
                "description": "Charge every month on the first date",
                "customer": "cust_test_58655j2ez4elik6t2xc",
                "card": None
            },
            "occurrences": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2017-06-02T18:52:05+07:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "order": None,
                "location": "/schedules/schd_test/occurrences",
                "data": []
            },
            "next_occurrence_dates": [],
            "created": "2017-06-02T08:28:40Z"
        })

    @mock.patch('requests.post')
    def test_create(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
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
        }""")

        schedule = class_.create(
            every=1,
            period='month',
            on={
                'weekday_of_month': 'second_monday'
            },
            end_date='2018-05-01',
            charge={
                'customer': 'cust_test_58655j2ez4elik6t2xc',
                'amount': 100000,
                'description': 'Membership fee'
            }
        )

        self.assertTrue(isinstance(schedule, class_))
        self.assertEqual(schedule.id, 'schd_test')
        self.assertEqual(schedule.every, 1)
        self.assertEqual(schedule.period, 'month')
        self.assertEqual(schedule.status, 'active')
        self.assertEqual(schedule.start_date, '2017-06-02')
        self.assertEqual(schedule.end_date, '2018-05-01')
        self.assertRequest(
            api_call,
            'https://api.omise.co/schedules',
            {
                'every': 1,
                'period': 'month',
                'on': {
                    'weekday_of_month': 'second_monday'
                },
                'end_date': '2018-05-01',
                'charge': {
                    'customer': 'cust_test_58655j2ez4elik6t2xc',
                    'amount': 100000,
                    'description': 'Membership fee'
                }
            }
        )

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
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
        }""")

        schedule = class_.retrieve('schd_test')
        self.assertTrue(isinstance(schedule, class_))
        self.assertTrue(schedule.id, 'schd_test')
        self.assertEqual(schedule.every, 1)
        self.assertEqual(schedule.period, 'month')
        self.assertEqual(schedule.status, 'active')
        self.assertEqual(schedule.start_date, '2017-06-02')
        self.assertEqual(schedule.end_date, '2018-05-01')
        self.assertRequest(api_call, 'https://api.omise.co/schedules/schd_test')

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
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
            "location": "/schedules",
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

        schedules = class_.retrieve()
        self.assertTrue(isinstance(schedules, collection_class_))
        self.assertTrue(isinstance(schedules[0], class_))
        self.assertTrue(schedules[0].id, 'schd_test')
        self.assertEqual(schedules[0].every, 1)
        self.assertEqual(schedules[0].period, 'month')
        self.assertEqual(schedules[0].status, 'active')
        self.assertEqual(schedules[0].start_date, '2017-06-02')
        self.assertEqual(schedules[0].end_date, '2018-05-01')
        self.assertRequest(api_call, 'https://api.omise.co/schedules')

    @mock.patch('requests.get')
    def test_reload(self, api_call):
        schedule = self._makeOne()
        class_ = self._getTargetClass()

        self.assertTrue(isinstance(schedule, class_))
        self.assertEqual(schedule.every, 1)
        self.assertEqual(schedule.period, "month")

        self.mockResponse(api_call, """{
            "object": "schedule",
            "id": "schd_test",
            "livemode": false,
            "location": "/schedules/schd_test",
            "status": "active",
            "deleted": false,
            "every": 7,
            "period": "week",
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
        }""")

        schedule.reload()
        self.assertEqual(schedule.every, 7)
        self.assertEqual(schedule.period, 'week')
        self.assertRequest(api_call, 'https://api.omise.co/schedules/schd_test')

    @mock.patch('requests.delete')
    def test_destroy(self, api_call):
        schedule = self._makeOne()
        class_ = self._getTargetClass()

        self.mockResponse(api_call, """{
            "object": "schedule",
            "id": "schd_test",
            "livemode": false,
            "location": "/schedules/schd_test",
            "status": "deleted",
            "deleted": true,
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
        }""")

        self.assertTrue(isinstance(schedule, class_))
        self.assertEqual(schedule.status, 'active')
        self.assertEqual(schedule.deleted, False)

        schedule.destroy()
        self.assertTrue(schedule.destroyed)
        self.assertEqual(schedule.status, 'deleted')
        self.assertEqual(schedule.deleted, True)

        self.assertRequest(
            api_call,
            'https://api.omise.co/schedules/schd_test'
        )

    @mock.patch('requests.get')
    def test_occurrence(self, api_call):
        schedule = self._makeOne()
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
                    "object": "occurrence",
                    "id": "occu_test",
                    "location": "/occurrences/occu_test",
                    "schedule": "schd_test",
                    "schedule_date": "2017-06-05",
                    "retry_date": null,
                    "processed_at": "2017-06-05T08:29:15Z",
                    "status": "successful",
                    "message": null,
                    "result": "chrg_test",
                    "created": "2017-06-05T08:29:13Z"
                }
            ]
        }""")

        self.assertTrue(isinstance(schedule, class_))

        occurrences = schedule.occurrence()
        self.assertTrue(isinstance(occurrences, collection_class_))
        self.assertEqual(occurrences.total, 1)
        self.assertEqual(occurrences[0].id, 'occu_test')
        self.assertEqual(occurrences[0].location, '/occurrences/occu_test')
        self.assertEqual(occurrences[0].status, 'successful')
        self.assertEqual(occurrences[0].result, 'chrg_test')

        self.assertRequest(
            api_call,
            'https://api.omise.co/schedules/schd_test/occurrences'
        )


class TransferTest(_ResourceMixin):

    def _getTargetClass(self):
        from .. import Transfer
        return Transfer

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'transfer',
            'created': '2014-11-18T11:31:26Z',
            'livemode': False,
            'failure_message': None,
            'paid': False,
            'currency': 'thb',
            'amount': 100000,
            'transaction': None,
            'location': '/transfers/trsf_test',
            'failure_code': None,
            'id': 'trsf_test',
            'sent': False
        })

    @mock.patch('requests.post')
    def test_create(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "transfer",
            "id": "trsf_test",
            "livemode": false,
            "location": "/transfers/trsf_test",
            "sent": false,
            "paid": false,
            "amount": 100000,
            "currency": "thb",
            "failure_code": null,
            "failure_message": null,
            "transaction": null,
            "created": "2014-11-18T11:31:26Z"
        }""")

        transfer = class_.create(amount=100000)
        self.assertTrue(isinstance(transfer, class_))
        self.assertEqual(transfer.id, 'trsf_test')
        self.assertEqual(transfer.amount, 100000)
        self.assertRequest(
            api_call,
            'https://api.omise.co/transfers',
            {'amount': 100000}
        )

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "transfer",
            "id": "trsf_test",
            "livemode": false,
            "location": "/transfers/trsf_test",
            "sent": false,
            "paid": false,
            "amount": 100000,
            "currency": "thb",
            "failure_code": null,
            "failure_message": null,
            "transaction": null,
            "created": "2014-11-18T11:31:26Z"
        }
        """)

        transfer = class_.retrieve('trsf_test')
        self.assertTrue(isinstance(transfer, class_))
        self.assertFalse(transfer.sent)
        self.assertFalse(transfer.paid)
        self.assertEqual(transfer.id, 'trsf_test')
        self.assertEqual(transfer.amount, 100000)
        self.assertEqual(transfer.transaction, None)
        self.assertRequest(api_call, 'https://api.omise.co/transfers/trsf_test')

        self.mockResponse(api_call, """{
            "object": "transfer",
            "id": "trsf_test",
            "livemode": false,
            "location": "/transfers/trsf_test",
            "sent": true,
            "paid": true,
            "amount": 100000,
            "currency": "thb",
            "failure_code": null,
            "failure_message": null,
            "transaction": null,
            "created": "2014-11-18T11:31:26Z"
        }
        """)

        transfer.reload()
        self.assertTrue(transfer.sent)
        self.assertTrue(transfer.paid)

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
                    "object": "transfer",
                    "id": "trsf_test",
                    "livemode": false,
                    "location": "/transfers/trsf_test",
                    "sent": false,
                    "paid": false,
                    "amount": 96350,
                    "currency": "thb",
                    "failure_code": null,
                    "failure_message": null,
                    "transaction": null,
                    "created": "2014-11-18T11:31:26Z"
                }
            ]
        }""")

        transfers = class_.retrieve()
        self.assertTrue(isinstance(transfers, collection_class_))
        self.assertTrue(isinstance(transfers[0], class_))
        self.assertTrue(transfers[0].id, 'trsf_test')
        self.assertTrue(transfers[0].amount, 96350)
        self.assertRequest(api_call, 'https://api.omise.co/transfers')

    @mock.patch('requests.patch')
    def test_update(self, api_call):
        transfer = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "transfer",
            "id": "trsf_test",
            "livemode": false,
            "location": "/transfers/trsf_test",
            "sent": false,
            "paid": false,
            "amount": 80000,
            "currency": "thb",
            "failure_code": null,
            "failure_message": null,
            "transaction": null,
            "created": "2014-11-18T11:31:26Z"
        }""")

        self.assertTrue(isinstance(transfer, class_))
        self.assertEqual(transfer.amount, 100000)
        transfer.amount = 80000
        transfer.update()

        self.assertEqual(transfer.amount, 80000)
        self.assertRequest(
            api_call,
            'https://api.omise.co/transfers/trsf_test',
            {'amount': 80000}
        )

    @mock.patch('requests.delete')
    def test_destroy(self, api_call):
        transfer = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "transfer",
            "id": "trsf_test",
            "livemode": false,
            "deleted": true
        }""")

        self.assertTrue(isinstance(transfer, class_))
        self.assertEqual(transfer.id, 'trsf_test')

        transfer.destroy()
        self.assertTrue(transfer.destroyed)
        self.assertRequest(
            api_call,
            'https://api.omise.co/transfers/trsf_test'
        )


class TransactionTest(_ResourceMixin):

    def _getTargetClass(self):
        from .. import Transaction
        return Transaction

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "transaction",
            "id": "trxn_test",
            "type": "credit",
            "amount": 9635024,
            "currency": "thb",
            "created": "2014-10-27T06:58:56Z"
        }
        """)

        transaction = class_.retrieve('trxn_test')
        self.assertTrue(isinstance(transaction, class_))
        self.assertEqual(transaction.id, 'trxn_test')
        self.assertEqual(transaction.type, 'credit')
        self.assertEqual(transaction.amount, 9635024)
        self.assertEqual(transaction.currency, 'thb')
        self.assertRequest(
            api_call,
            'https://api.omise.co/transactions/trxn_test'
        )

        transaction.amount = 9635023
        self.assertEqual(transaction.amount, 9635023)
        self.mockResponse(api_call, """{
            "object": "transaction",
            "id": "trxn_test",
            "type": "credit",
            "amount": 9635024,
            "currency": "thb",
            "created": "2014-10-27T06:58:56Z"
        }
        """)

        transaction.reload()
        self.assertEqual(transaction.amount, 9635024)
        self.assertEqual(transaction.currency, 'thb')
        self.assertRequest(
            api_call,
            'https://api.omise.co/transactions/trxn_test'
        )

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2014-10-27T14:55:29+07:00",
            "offset": 0,
            "limit": 20,
            "total": 2,
            "data": [
                {
                    "object": "transaction",
                    "id": "trxn_test_1",
                    "type": "credit",
                    "amount": 9635024,
                    "currency": "thb",
                    "created": "2014-10-27T06:58:56Z"
                },
                {
                    "object": "transaction",
                    "id": "trxn_test_2",
                    "type": "debit",
                    "amount": 100025,
                    "currency": "thb",
                    "created": "2014-10-27T07:02:54Z"
                }
            ]
        }""")

        transactions = class_.retrieve()
        self.assertTrue(isinstance(transactions, collection_class_))
        self.assertTrue(isinstance(transactions[0], class_))
        self.assertTrue(transactions[0].id, 'trxn_test_1')
        self.assertTrue(transactions[0].type, 'credit')
        self.assertTrue(transactions[0].amount, 9635024)
        self.assertTrue(isinstance(transactions[1], class_))
        self.assertTrue(transactions[1].id, 'trxn_test_2')
        self.assertTrue(transactions[1].type, 'debit')
        self.assertTrue(transactions[1].amount, 100025)
        self.assertRequest(api_call, 'https://api.omise.co/transactions')
