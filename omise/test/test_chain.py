import mock
import unittest

from .helper import _ResourceMixin


class ChainTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Chain
        return Chain

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _getLazyCollectionClass(self):
        from .. import LazyCollection
        return LazyCollection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'chain',
            'id': 'acch_test',
            'livemode': False,
            'location': '/chains/acch_test',
            'revoked': False,
            'email': 'john.doe@example.com',
            'key': 'ckey_test',
            'created': '2021-02-02T03:12:43Z'
        })

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "chain",
            "id": "acch_test",
            "livemode": false,
            "location": "/chains/acch_test",
            "revoked": false,
            "email": "john.doe@example.com",
            "key": "ckey_test",
            "created": "2021-02-02T03:12:43Z"
        }""")

        chain = class_.retrieve('acch_test')
        self.assertTrue(isinstance(chain, class_))
        self.assertEqual(chain.id, 'acch_test')
        self.assertEqual(chain.email, 'john.doe@example.com')
        self.assertEqual(chain.key, 'ckey_test')
        self.assertFalse(chain.revoked)
        self.assertRequest(api_call, 'https://api.omise.co/chains/acch_test')

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "data": [
              {
                "object": "chain",
                "id": "acch_test_1",
                "livemode": false,
                "location": "/chains/acch_test_1",
                "revoked": true,
                "email": "jenny.doe@example.com",
                "key": "",
                "created_at": "2020-09-22T06:08:38Z"
              },
              {
                "object": "chain",
                "id": "acch_test_2",
                "livemode": false,
                "location": "/chains/acch_test_2",
                "revoked": false,
                "email": "john.doe@example.com",
                "key": "ckey_test",
                "created_at": "2021-02-02T03:12:43Z"
              }
            ],
            "limit": 20,
            "offset": 0,
            "total": 2,
            "location": null,
            "order": "chronological",
            "from": "1970-01-01T00:00:00Z",
            "to": "2021-02-02T03:16:57Z"
        }""")

        chains = class_.retrieve()
        self.assertTrue(isinstance(chains, collection_class_))
        self.assertTrue(isinstance(chains[0], class_))
        self.assertTrue(chains[0].id, 'acch_test_1')
        self.assertTrue(chains[0].email, 'jenny.doe@example.com')
        self.assertTrue(chains[1].id, 'acch_test_2')
        self.assertTrue(chains[1].email, 'john.doe@example.com')
        self.assertRequest(api_call, 'https://api.omise.co/chains')

    @mock.patch('requests.get')
    def test_list(self, api_call):
        class_ = self._getTargetClass()
        lazy_collection_class_ = self._getLazyCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "data": [
              {
                "object": "chain",
                "id": "acch_test_1",
                "livemode": false,
                "location": "/chains/acch_test_1",
                "revoked": true,
                "email": "jenny.doe@example.com",
                "key": "",
                "created_at": "2020-09-22T06:08:38Z"
              },
              {
                "object": "chain",
                "id": "acch_test_2",
                "livemode": false,
                "location": "/chains/acch_test_2",
                "revoked": false,
                "email": "john.doe@example.com",
                "key": "ckey_test",
                "created_at": "2021-02-02T03:12:43Z"
              }
            ],
            "limit": 20,
            "offset": 0,
            "total": 2,
            "location": null,
            "order": "chronological",
            "from": "1970-01-01T00:00:00Z",
            "to": "2021-02-02T03:16:57Z"
        }""")

        chains = class_.list()
        self.assertTrue(isinstance(chains, lazy_collection_class_))

        chains = list(chains)
        self.assertTrue(isinstance(chains[0], class_))
        self.assertTrue(chains[0].id, 'acch_test_1')
        self.assertTrue(chains[0].email, 'jenny.doe@example.com')
        self.assertTrue(chains[1].id, 'acch_test_2')
        self.assertTrue(chains[1].email, 'john.doe@example.com')

    @mock.patch('requests.get')
    def test_reload(self, api_call):
        chain = self._makeOne()
        class_ = self._getTargetClass()

        self.assertTrue(isinstance(chain, class_))
        self.assertEqual(chain.id, 'acch_test')
        self.assertFalse(chain.revoked)

        self.mockResponse(api_call, """{
            "object": "chain",
            "id": "acch_test",
            "livemode": false,
            "location": "/chains/acch_test",
            "revoked": true,
            "email": "john.doe@example.com",
            "key": "ckey_test",
            "created": "2021-02-02T03:12:43Z"
        }""")

        chain.reload()
        self.assertEqual(chain.id, 'acch_test')
        self.assertTrue(chain.revoked)
        self.assertRequest(
            api_call,
            'https://api.omise.co/chains/acch_test'
        )

    @mock.patch('requests.post')
    def test_revoke(self, api_call):
        chain = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "chain",
            "id": "acch_test",
            "livemode": false,
            "revoked": true
        }""")

        self.assertTrue(isinstance(chain, class_))
        self.assertEqual(chain.id, 'acch_test')

        chain.revoke()
        self.assertTrue(chain.revoked)
        self.assertRequest(
            api_call,
            'https://api.omise.co/chains/acch_test/revoke'
        )