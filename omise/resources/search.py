from omise import Base, _as_object
from .main_resource import _MainResource


class Search(_MainResource, Base):
    """API class for searching.

    This API class is used for retrieving results from your account.
    Currently, Search API is supported to search only Charge, Dispute,
    Recipient and Customer.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> search = omise.Search.execute('charge', **{
            'query': 'thb',
            'filters': {
                'amount': '1000..2000',
                'captured': 'true'
            }
        })
        <Search at 0x1029e57f0>
        >>> search[0]
        <Charge id='chrg_test_58505fmz8hbaln3283s' at 0x10291edd8>
    """

    def __len__(self):
        return len(self._attributes['data'])

    def __iter__(self):
        for obj in self._attributes['data']:
            yield _as_object(obj)

    def __getitem__(self, item):
        return _as_object(self._attributes['data'][item])

    @classmethod
    def execute(cls, scope, **options):
        querystring = ['?scope=%s' % scope]

        for key, val in options.items():
            if isinstance(val, dict):
                for k, v in val.items():
                    querystring.append('%s[%s]=%s' % (key, k, v))
            else:
                querystring.append('%s=%s' % (key, val))

        return _as_object(
            cls._request('get',
                         ('search', '&'.join(querystring))))