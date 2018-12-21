from omise import Base, _as_object, LazyCollection, _MainResource


class Event(_MainResource, Base):
    """API class representing an event in an account.

    This API class is used for retrieving an event in an
    account. The event represents event object from webhooks.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> event = omise.Event.retrieve('evnt_test_5086xmr74vxs0ajpo78')
        <Event id='evnt_test_5086xmr74vxs0ajpo78' at 0x7f79c41e9eb8>
        >>> event.key
        'charge.create'
    """

    @classmethod
    def _collection_path(cls):
        return 'events'

    @classmethod
    def _instance_path(cls, event_id):
        return ('events', event_id)

    @classmethod
    def retrieve(cls, event_id=None):
        """Retrieve the event details for the given :param:`event_id`.
        If :param:`event_id` is not given, all events will be returned
        instead.

        :param event_id: (optional) an event id to retrieve.
        :type event_id: str
        :rtype: Event
        """
        if event_id:
            return _as_object(cls._request('get', cls._instance_path(event_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all events that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the event details.

        :rtype: Event
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))