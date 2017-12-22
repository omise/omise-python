import mock
import unittest

from .helper import _ResourceMixin


class LinkTest(_ResourceMixin, unittest.TestCase):

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
