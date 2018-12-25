def as_object(data):
    from .base import Base
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
    from . import Account, Balance, BankAccount, Card, Charge, Customer, Dispute, Event, Forex, Link, Collection, \
        Occurrence, Receipt, Recipient, Refund, Schedule, Search, Source, Token, Transfer, Transaction
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