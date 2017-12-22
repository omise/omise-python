import mock

try:
    import json
except ImportError:
    import simplejson as json


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


class _ResourceMixin(_RequestAssertable):

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
