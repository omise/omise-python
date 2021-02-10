import mock
import unittest

from .helper import _ResourceMixin


class DocumentTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Document
        return Document

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'document',
            'id': 'docu_test',
            'livemode': False,
            'location': '/disputes/dspt_test/documents/docu_test',
            'deleted': False,
            'filename': 'evidence.png',
            'created': '2021-02-04T03:12:43Z'
        })

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "document",
            "id": "docu_test",
            "livemode": false,
            "location": "/disputes/dspt_test/documents/docu_test",
            "deleted": false,
            "filename": "evidence.png",
            "created": "2021-02-04T03:12:43Z"
        }""")

        document = class_.retrieve('dspt_test', 'docu_test')
        self.assertTrue(isinstance(document, class_))
        self.assertEqual(document.id, 'docu_test')
        self.assertEqual(document.filename, 'evidence.png')
        self.assertFalse(document.deleted)
        self.assertRequest(api_call, 'https://api.omise.co/disputes/dspt_test/documents/docu_test')

    @mock.patch('requests.get')
    def test_reload(self, api_call):
        document = self._makeOne()
        class_ = self._getTargetClass()

        self.assertTrue(isinstance(document, class_))
        self.assertEqual(document.id, 'docu_test')
        self.assertFalse(document.deleted)

        self.mockResponse(api_call, """{
            "object": "document",
            "id": "docu_test",
            "livemode": false,
            "location": "/disputes/dspt_test/documents/docu_test",
            "deleted": true,
            "filename": "evidence.png",
            "created": "2021-02-04T03:12:43Z"
        }""")

        document.reload()
        self.assertEqual(document.id, 'docu_test')
        self.assertTrue(document.deleted)
        self.assertRequest(
            api_call,
            'https://api.omise.co/disputes/dspt_test/documents/docu_test'
        )

    @mock.patch('requests.delete')
    def test_destroy(self, api_call):
        document = self._makeOne()
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "document",
            "id": "docu_test",
            "livemode": false,
            "location": "/disputes/dspt_test/documents/docu_test",
            "deleted": true,
            "filename": "evidence.png",
            "created": "2021-02-04T03:12:43Z"
        }""")

        self.assertTrue(isinstance(document, class_))
        self.assertEqual(document.id, 'docu_test')

        document.destroy()
        self.assertTrue(document.destroyed)
        self.assertRequest(
            api_call,
            'https://api.omise.co/disputes/dspt_test/documents/docu_test'
        )