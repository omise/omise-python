import logging
import os
import requests
import sys

from . import version
from . import errors


if sys.version_info[0] == 3:
    import urllib.parse as urlparse
elif sys.version_info[0] == 2:
    import urlparse


try:
    basestring
except NameError:
    basestring = str


try:
    import json
except ImportError:
    import simplejson as json


# Logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class Request(object):
    """API requestor that construct and make a request to API endpoint.

    Construct an API endpoint and authentication header using the given
    ``api_key`` and ``api_base`` and allow user to make a request to that
    endpoint.

    Basic usage::

        >>> import omise
        >>> r = omise.Request('skey_test', 'http://api.omise.co/', '2015-11-17')
        >>> r.send('get', 'account')
        {'email': 'foo@example.com', 'object': 'account', ...}
    """

    def __init__(self, api_key, api_base, api_version):
        if api_key is None:
            raise AttributeError('API key is not set.')
        self.api_key = api_key
        self.api_base = api_base
        self.api_version = api_version

    def send(self, method, path, payload=None, headers=None):
        """Make a request to the API endpoint and return a JSON response.

        This method will construct a URL using :param:`path` and make a request
        to that endpoint using HTTP method set in :param:`method` with
        necessary headers set. The JSON returned from the API server will
        be serialized into :type:`dict`.

        If :param:`payload` is given, that payload will be passed alongside
        the request regardless of HTTP method used. Custom headers are
        assignable via :param:`headers`, however please note that ``Accept``,
        ``Content-Type`` and ``User-Agent`` are not overridable.

        In case the response is an error, an appropriate exception from
        :module:`omise.errors` will be raised. The application code is
        responsible for handling these exceptions.

        :param method: method for the request.
        :param path: path components relative to API base to make the request.
        :param payload: (optional) dict containing data to send to the server.
        :param headers: (optional) dict containing custom headers.

        :type method: str
        :type path: str or list or tuple
        :type payload: dict or None
        :type headers: dict or None
        :rtype: dict
        """
        request_path = self._build_path(path)
        request_payload = self._build_payload(payload)
        request_headers = self._build_headers(headers)

        logger.info('Sending HTTP request: %s %s', method.upper(), request_path)
        logger.debug('Authorization: %s', self.api_key)
        logger.debug('Payload: %s', request_payload)
        logger.debug('Headers: %s', request_headers)

        response = getattr(requests, method)(
            request_path,
            data=request_payload,
            headers=request_headers,
            auth=(self.api_key, ''),
            verify=os.path.join(
                os.path.dirname(__file__),
                'data/ca_certificates.pem')
        ).json()

        logger.info('Received HTTP response: %s', response)

        if response.get('object') == 'error':
            errors._raise_from_data(response)
        return response

    def _build_path(self, path):
        if not hasattr(path, '__iter__') or isinstance(path, basestring):
            path = (path,)
        path = map(str, path)
        return urlparse.urljoin(self.api_base, '/'.join(path))

    def _build_payload(self, payload):
        if payload is None:
            payload = {}
        return json.dumps(payload, sort_keys=True)

    def _build_headers(self, headers):
        if headers is None:
            headers = {}
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        if self.api_version is not None:
            headers['Omise-Version'] = self.api_version
        headers['User-Agent'] = 'OmisePython/%s' % version.__VERSION__
        return headers
