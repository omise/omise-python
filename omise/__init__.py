import sys

from .request import Request


if sys.version_info[0] == 3:
    def iteritems(d, **kw):
        return iter(d.items(**kw))

elif sys.version_info[0] == 2:
    def iteritems(d, **kw):
        return iter(d.iteritems(**kw))


# Settings
api_secret = None
api_public = None
api_version = None


# API constants
api_main = 'https://api.omise.co'
api_vault = 'https://vault.omise.co'


__all__ = [
    'Account',
    'Balance',
    'BankAccount',
    'Card',
    'Charge',
    'Collection',
    'Customer',
    'Dispute',
    'Event',
    'Forex',
    'Link',
    'Occurrence',
    'Receipt',
    'Recipient',
    'Refund',
    'Search',
    'Schedule',
    'Source',
    'Token',
    'Transaction',
    'Transfer',
]


def _get_class_for(type):
    """Returns a :type:`class` corresponding to :param:`type`.

    Used for getting a class from object type in JSON response. Usually, to
    instantiate the Python object from response, this function is called in
    the form of ``_get_class_for(data['object']).from_data(data)``.

    :type type: str
    :rtype: class
    """
    return {
        'account': Account,
        'balance': Balance,
        'bank_account': BankAccount,
        'card': Card,
        'charge': Charge,
        'customer': Customer,
        'dispute': Dispute,
        'event': Event,
        'forex': Forex,
        'link': Link,
        'list': Collection,
        'occurrence': Occurrence,
        'receipt': Receipt,
        'recipient': Recipient,
        'refund': Refund,
        'schedule': Schedule,
        'search': Search,
        'source': Source,
        'token': Token,
        'transfer': Transfer,
        'transaction': Transaction,
    }.get(type)


def _as_object(data):
    """Returns a Python :type:`object` from API response.

    Accepts a :type:`dict` returned from Omise API and instantiate it as
    Python object using the class returned from :func:`_get_class_for`.

    :type data: dict | list
    :rtype: T <= Base
    """
    if isinstance(data, list):
        return [_as_object(i) for i in data]
    elif isinstance(data, dict):
        class_ = _get_class_for(data['object'])
        if not class_:
            class_ = Base
        return class_.from_data(data)
    return data


class Base(object):
    """Provides a base class for all API classes.

    The base class that all API classes inherit from. The instance of
    this class proxies its attributes access to :type:`dict` and also
    track changes made to it.

    Basic usage::

        >>> import omise
        >>> obj = omise.Base.from_data({'id': 'test'})
        <Base id='test' at 0x7f0d931cf740>
        >>> obj.id
        'test'
    """

    def __init__(self):
        super(Base, self).__init__()
        self._attributes = dict()
        self._changes = set()

    def __setattr__(self, key, value):
        if key[0] == '_':
            super(Base, self).__setattr__(key, value)
        else:
            self._changes.add(key)
            self._attributes[key] = value

    def __getattr__(self, key):
        if key[0] == '_':
            raise AttributeError(key)
        try:
            value = self._attributes[key]
            if isinstance(value, dict):
                return _as_object(value)
            return value
        except KeyError as e:
            raise AttributeError(*e.args)

    def __repr__(self):
        id_ = self._attributes.get('id')
        return '<%s%s at %s>' % (
            type(self).__name__,
            ' id=%s' % repr(str(id_)) if id_ else '',
            hex(id(self)))

    @classmethod
    def from_data(cls, data):
        """Instantiate the class with the given data.

        Creates a new instance of this class with :param:`data` assigned to it.
        This method is what is called after the data is retrieved from the API.

        :param data: data to instantiate this class with.
        :type data: dict
        """
        instance = cls()
        instance._reload_data(data)
        return instance

    @classmethod
    def _request(cls):
        return NotImplementedError

    @classmethod
    def _collection_path(cls):
        return NotImplementedError

    @classmethod
    def _instance_path(cls, *args):
        raise NotImplementedError

    def _reload_data(self, data):
        self._attributes = dict()
        for k, v in iteritems(data):
            self._attributes[k] = v
        self._changes = set()
        return self

    @property
    def changes(self):
        """Property that returns a :type:`dict` of attributes pending update.

        This method is used to track changes made to attribute of an instance
        which is often used to determine which attributes to update on the
        server when :method:`update` is called.

        :rtype: dict
        """
        return dict((c, self._attributes.get(c)) for c in self._changes)


class LazyCollection(object):
    """Proxy class representing a lazy collection of items."""
    def __init__(self, collection_path):
        self.collection_path = collection_path
        self._exhausted = False

    def __len__(self):
        return self._fetch_objects(limit=1, offset=0)['total']

    def __iter__(self):
        self.limit = 100
        self.listing = []

        self._list_index = 0

        return self

    def __next__(self):
        if (self.listing is None) or (self._list_index + 1 > len(self.listing)):
            self._next_batch(limit=self.limit, offset=self._list_index)

        self._list_index += 1
        return _as_object(self.listing[self._list_index - 1])

    def next(self):
        return self.__next__()

    def offset(self, **kwargs):
        limit = kwargs.pop('limit', 20)
        offset = kwargs.pop('offset', 0)
        order = kwargs.pop('order', None)

        obj = self._fetch_objects(limit=limit, offset=offset, order=order)
        data = obj['data']

        return [_as_object(item) for item in data]

    def _next_batch(self, **kwargs):
        if self._exhausted:
            raise StopIteration

        obj = self._fetch_objects(limit=kwargs['limit'], offset=kwargs['offset'])
        data = obj['data']

        if len(data) > 0:
            self._add_to_listing(data)
        else:
            raise StopIteration

    def _add_to_listing(self, data):
        for item in data:
            self.listing.append(item)

        if len(data) < self.limit:
            self._exhausted = True

    def _fetch_objects(self, **kwargs):
        order = kwargs.pop('order', None)

        return Request(api_secret, api_main, api_version).send(
            'get',
            self.collection_path,
            payload={
                'limit': kwargs['limit'],
                'offset': kwargs['offset'],
                'order': order
            }
        )


class _MainResource(Base):

    @classmethod
    def _request(cls, *args, **kwargs):
        return Request(api_secret, api_main, api_version).send(*args, **kwargs)

    def _nested_object_path(self, association_cls):
        return (
            self.__class__._collection_path(),
            self.id, association_cls._collection_path()
        )


class _VaultResource(Base):

    @classmethod
    def _request(cls, *args, **kwargs):
        return Request(api_public, api_vault, api_version).send(*args, **kwargs)


from .resources.account import Account
from .resources.charge import Charge
from .resources.balance import Balance
from .resources.card import Card
from .resources.customer import Customer
from .resources.dispute import Dispute
from .resources.event import Event
from .resources.forex import Forex
from .resources.link import Link
from .resources.occurence import Occurrence
from .resources.transaction import Transaction
from .resources.transfer import Transfer
from .resources.source import Source
from .resources.schedule import Schedule
from .resources.search import Search
from .resources.refund import Refund
from .resources.receipt import Receipt
from .resources.recipient import Recipient
from .resources.bank_account import BankAccount
from .resources.token import Token
from .resources.collection import Collection


