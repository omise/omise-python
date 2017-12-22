import mock
import unittest

from .helper import _ResourceMixin


class SourceTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Source
        return Source

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'source',
            'id': 'src_test',
            'type': 'internet_banking_test',
            'flow': 'redirect',
            'amount': 100000,
            'currency': 'thb'
        })

    @mock.patch('requests.post')
    def test_create_offsite(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "source",
            "id": "src_test",
            "type": "internet_banking_test",
            "flow": "redirect",
            "amount": 100000,
            "currency": "thb"
        }""")

        source = class_.create(
            amount=100000,
            currency='thb',
            type='internet_banking_test'
        )
        self.assertTrue(isinstance(source, class_))
        self.assertEqual(source.id, 'src_test')
        self.assertEqual(source.amount, 100000)
        self.assertRequest(
            api_call,
            'https://api.omise.co/sources',
            {
                'amount': 100000,
                'currency': 'thb',
                'type': 'internet_banking_test'
            }
        )

    @mock.patch('requests.post')
    def test_create_offline(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "source",
            "id": "src_test",
            "type": "tesco_lotus",
            "flow": "offline",
            "amount": 100000,
            "currency": "thb"
        }""")

        source = class_.create(
            amount=100000,
            currency='thb',
            type='tesco_lotus'
        )
        self.assertTrue(isinstance(source, class_))
        self.assertEqual(source.id, 'src_test')
        self.assertEqual(source.amount, 100000)
        self.assertRequest(
            api_call,
            'https://api.omise.co/sources',
            {
                'amount': 100000,
                'currency': 'thb',
                'type': 'tesco_lotus'
            }
        )
