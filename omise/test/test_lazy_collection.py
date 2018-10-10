import mock
import unittest

from .helper import _ResourceMixin


class LazyCollectionTest(_ResourceMixin, unittest.TestCase):

    def _getLazyCollectionClass(self):
        from .. import LazyCollection
        return LazyCollection

    def _getCustomerClass(self):
        from .. import Customer
        return Customer

    def _makeOne(self):
        return self._getLazyCollectionClass()(self._getCustomerClass())

    def _mocked_response(self):
        return """{
            "object": "list",
            "from": "1970-01-01T00:00:00Z",
            "to": "2018-04-23T06:13:05Z",
            "offset": 0,
            "limit": 20,
            "total": 2,
            "order": "chronological",
            "location": "/customers",
            "data": [
                {
                    "id": "cust_a",
                    "created": "2018-01-16T08:37:53Z",
                    "object": "customer",
                    "livemode": false,
                    "location": "/customers/cust_a",
                    "description": "John Doe (id: 30)",
                    "email": "john.doe@example.com",
                    "default_card": "card_test_a"
                },
                {
                    "id": "cust_b",
                    "created": "2018-01-16T08:37:53Z",
                    "object": "customer",
                    "livemode": false,
                    "location": "/customers/cust_b",
                    "description": "John Doe (id: 30)",
                    "email": "john.doe@example.com",
                    "default_card": "card_test_b"
                }
            ]
        }"""

    @mock.patch('requests.get')
    def test_len(self, api_call):
        lazy_collection = self._makeOne()
        self.mockResponse(api_call, self._mocked_response())
        self.assertEqual(len(lazy_collection), 2)

    @mock.patch('requests.get')
    def test_iter(self, api_call):
        lazy_collection = self._makeOne()
        self.mockResponse(api_call, self._mocked_response())
        iterable = iter(lazy_collection)
        self.assertTrue(isinstance(iterable, self._getLazyCollectionClass()))

    @mock.patch('requests.get')
    def test_next(self, api_call):
        lazy_collection = self._makeOne()
        self.mockResponse(api_call, self._mocked_response())
        iterable = iter(lazy_collection)
        firstItem = next(iterable)
        self.assertTrue(isinstance(firstItem, self._getCustomerClass()))
        self.assertEqual(firstItem.id, 'cust_a')
        self.assertEqual(next(iterable).id, 'cust_b')

    @mock.patch('requests.get')
    def test_offset(self, api_call):
        lazy_collection = self._makeOne()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T00:00:00Z",
            "to": "2018-04-23T06:13:05Z",
            "offset": 1,
            "limit": 20,
            "total": 2,
            "order": "chronological",
            "location": "/customers",
            "data": [
                {
                    "id": "cust_b",
                    "created": "2018-01-16T08:37:53Z",
                    "object": "customer",
                    "livemode": false,
                    "location": "/customers/cust_b",
                    "description": "John Doe (id: 30)",
                    "email": "john.doe@example.com",
                    "default_card": "card_test_b"
                }
            ]
        }""")
        request = lazy_collection.offset(**{'offset': 1})
        self.assertEqual(request[0].id, 'cust_b')
