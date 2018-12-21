import sys


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

from .api import *

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


