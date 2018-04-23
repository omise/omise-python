import unittest
import mock
from .. import Customer, LazyCollection

from .helper import _ResourceMixin


class LazyCollectionTest(_ResourceMixin, unittest.TestCase):

    def _makeOne(self):
        return LazyCollection(Customer)


    def _mocked_response(self):
        return """{
                    "offset": 0,
                    "from": "1970-01-01T00:00:00Z",
                    "object": "list",
                    "location": "/customers",
                    "order": "chronological",
                    "to": "2018-04-23T06:13:05Z",
                    "total": 2,
                    "data": [
                        {
                            "id": "cust_a",
                            "created": "2018-01-16T08:37:53Z",
                            "object": "customer", "livemode": false,
                            "location": "/customers/cust_a",
                            "description": "John Doe (id: 30)",
                            "email": "john.doe@example.com",
                            "default_card": "card_test_a"
                        },
                        {
                            "id": "cust_b",
                            "created": "2018-01-16T08:37:53Z",
                            "object": "customer", "livemode": false,
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
        firstItem = next(iterable)
        self.assertTrue(isinstance(firstItem, Customer))
        self.assertEqual(firstItem.id, 'cust_a')
        self.assertEqual(next(iterable).id, 'cust_b')
