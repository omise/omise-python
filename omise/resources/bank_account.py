from omise import Base


class BankAccount(Base):
    """API class representing bank account details.

    This API class represents a bank account information returned from other
    APIs. Bank accounts are not created directly with this class, but instead
    created with :class:`Recipient`.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> recipient = omise.Recipient.retrieve('recp_test_5086xmr74vxs0ajpo78')
        >>> bank_account = recipient.bank_account
        <BankAccount name='SOMCHAI PRASERT' at 0x7f79c41e9d00>
        >>> bank_account.name
        'SOMCHAI PRASERT'
    """

    def __repr__(self):
        name = self._attributes.get('name')
        return '<%s%s at %s>' % (
            type(self).__name__,
            ' name=%s' % repr(str(name)) if name else '',
            hex(id(self)))