from omise import Base, _as_object, LazyCollection
from .main_resource import _MainResource


class Dispute(_MainResource, Base):
    """API class representing a recipient in an account.

    This API class is used for retrieving and updating a dispute in an
    account for charge back handling.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> dispute = omise.Dispute.retrieve('dspt_test_4zgf15h89w8t775kcm8')
        <Recipient id='dspt_test_4zgf15h89w8t775kcm8' at 0x7fd06ce3d5d0>
        >>> dispute.status
        'open'
    """

    @classmethod
    def _collection_path(cls, status=None):
        if status:
            return ('disputes', status)
        return 'disputes'

    @classmethod
    def _instance_path(cls, dispute_id):
        return ('disputes', dispute_id)

    @classmethod
    def retrieve(cls, *args, **kwargs):
        if len(args) > 0:
            return _as_object(cls._request('get', cls._instance_path(args[0])))
        elif 'status' in kwargs:
            return _as_object(
                cls._request('get',
                             cls._collection_path(kwargs['status'])))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all disputes that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    @classmethod
    def list_open_disputes(cls):
        """Return all open disputes that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path("open"))

    @classmethod
    def list_pending_disputes(cls):
        """Return all pending disputes that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path("pending"))

    @classmethod
    def list_closed_disputes(cls):
        """Return all closed disputes that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path("closed"))

    def reload(self):
        """Reload the dispute details.

        :rtype: Dispute
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def update(self, **kwargs):
        """Update the dispute details with the given arguments.

        See the `update a dispute`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
            >>> dspt = omise.Dispute.retrieve('dspt_test_4zgf15h89w8t775kcm8')
            >>> dspt.update(message='Proofs and other information')
            <Dispute id='dspt_test_4zgf15h89w8t775kcm8' at 0x7fd06cd56210>

        :param \*\*kwargs: arguments to update a dispute.
        :rtype: Recipient

        .. _update a dispute:
        ..     https://docs.omise.co/api/recipients/#disputes-update
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._instance_path(self._attributes['id']),
                          changed))