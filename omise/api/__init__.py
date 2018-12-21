from omise import iteritems


def as_object(data):
    """Returns a Python :type:`object` from API response.

    Accepts a :type:`dict` returned from Omise API and instantiate it as
    Python object using the class returned from :func:`_get_class_for`.

    :type data: dict | list
    :rtype: T <= Base
    """
    if isinstance(data, list):
        return [as_object(i) for i in data]
    elif isinstance(data, dict):
        class_ = get_class_for(data['object'])
        if not class_:
            class_ = Base
        return class_.from_data(data)
    return data


def get_class_for(type):
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
                return as_object(value)
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


from .resources import *
