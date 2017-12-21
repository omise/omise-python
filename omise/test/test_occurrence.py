import mock
import unittest

from .helper import _ResourceMixin


class OccurrenceTest(_ResourceMixin, unittest.TestCase):

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
