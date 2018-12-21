from omise import Base, _as_object, LazyCollection, _MainResource


class Recipient(_MainResource, Base):
    """API class representing a recipient in an account.

    This API class is used for retrieving and creating a recipient in an
    account. The recipient can be used to transfer the balance to specific
    bank accounts.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> recipient = omise.Recipient.retrieve('recp_test_5086xmr74vxs0ajpo78')
        <Recipient id='recp_test_5086xmr74vxs0ajpo78' at 0x7f79c41e9eb8>
        >>> recipient.name
        'Foobar Baz'
    """

    @classmethod
    def _collection_path(cls):
        return 'recipients'

    @classmethod
    def _instance_path(cls, recipient_id):
        return ('recipients', recipient_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a recipient with the given parameters.

        See the `create a recipient`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> customer = omise.Recipient.create(
            ...     name='Somchai Prasert',
            ...     email='somchai.prasert@example.com',
            ...     type='individual',
            ...     bank_account=dict(
            ...       brand='bbl',
            ...       number='1234567890',
            ...       name='SOMCHAI PRASERT'
            ...     )
            ... )
            <Recipient id='recp_test_5086xmr74vxs0ajpo78' at 0x7f79c41e9e90>

        .. _create a recipient:
        ..     https://docs.omise.co/api/recipients/#recipients-create

        :param \*\*kwargs: arguments to create a recipient.
        :rtype: Recipient
        """
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, recipient_id=None):
        """Retrieve the recipient details for the given :param:`recipient_id`.
        If :param:`recipient_id` is not given, all recipients will be returned
        instead.

        :param recipient_id: (optional) a recipient id to retrieve.
        :type recipient_id: str
        :rtype: Recipient
        """
        if recipient_id:
            return _as_object(cls._request('get',
                                           cls._instance_path(recipient_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all recipients that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the recipient details.

        :rtype: Recipient
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def update(self, **kwargs):
        """Update the recipient details with the given arguments.

        See the `update a recipient`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> recp = omise.Recipient.retrieve('recp_test_5086xmr74vxs0ajpo78')
            >>> recp.update(
            ...     email='somchai@prasert.com',
            ...     bank_account=dict(
            ...       brand='kbank',
            ...       number='1234567890',
            ...       name='SOMCHAI PRASERT'
            ...     )
            ... )
            <Recipient id='recp_test_5086xmr74vxs0ajpo78' at 0x7f79c41e9d00>

        :param \*\*kwargs: arguments to update a recipient.
        :rtype: Recipient

        .. _update a recipient:
        ..     https://docs.omise.co/api/recipients/#recipients-update
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._instance_path(self._attributes['id']),
                          changed))

    def destroy(self):
        """Delete the recipient from the server.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> recp = omise.Recipient.retrieve('recp_test_5086xmr74vxs0ajpo78')
            >>> recp.destroy()
            <Recipient id='recp_test_5086xmr74vxs0ajpo78' at 0x7f775ff01c60>
            >>> recp.destroyed
            True

        :rtype: Recipient
        """
        return self._reload_data(
            self._request('delete',
                          self._instance_path(self.id)))

    @property
    def destroyed(self):
        """Returns ``True`` if the recipient has been deleted.

        :rtype: bool
        """
        return self._attributes.get('deleted', False)