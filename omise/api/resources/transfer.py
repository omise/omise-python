from omise.api import *
from omise.api.resources import *


class Transfer(MainResource, Base):
    """API class representing a transfer.

    This API class is used for retrieving a transfer information and create
    a transfer to the bank account given in account settings. The transfer
    amount must always be less than the current balance.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> transfer = omise.Transfer.retrieve('trsf_test_4xs5px8c36dsanuwztf')
        <Transfer id='trsf_test_4xs5px8c36dsanuwztf' at 0x7ff72d8d1868>
        >>> transfer.amount
        50000
    """

    @classmethod
    def _collection_path(cls):
        return 'transfers'

    @classmethod
    def _instance_path(cls, transfer_id):
        return ('transfers', transfer_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a transfer to the bank account.

        See the `create a transfer`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> transfer = omise.Transfer.create(amount=100000)
            <Transfer id='trsf_test_4y3miv1nhy0dceit4w4' at 0x7f6ef55b0990>

        .. _create a transfer:
        ..     https://docs.omise.co/api/transfers/#create-a-transfer

        :param \*\*kwargs: arguments to create a transfer.
        :rtype: Transfer
        """
        return as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, transfer_id=None):
        """Retrieve the transfer details for the given :param:`transfer_id`.
        If :param:`transfer_id` is not given, all transfers will be returned
        instead.

        :param transfer_id: (optional) a transfer id to retrieve.
        :type transfer_id: str
        :rtype: Transfer
        """
        if transfer_id:
            return as_object(
                cls._request('get',
                             cls._instance_path(transfer_id)))
        return as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all transfers that belongs to your account.

        :rtype: omise.api.resources.lazy_collection.LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the transfer details.

        :rtype: Transfer
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def update(self, **kwargs):
        """Update the transfers details with the given arguments.

        This method will update the transfer if it is still in the pending
        state (i.e. not sent or paid.) An attempt to update a non-pending
        transfers will result in an error.

        See the `update a transfer`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> trsf = omise.Transfer.retrieve('trsf_test_4xs5px8c36dsanuwztf')
            >>> trsf.update(amount=50000)
            <Transfer id='trsf_test_4xs5px8c36dsanuwztf' at 0x7f037c6c9f90>

        :param \*\*kwargs: arguments to update the transfer.
        :rtype: Customer

        .. _update a transfer:
        ..     https://docs.omise.co/api/transfers/#update-a-transfer
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._instance_path(self.id),
                          changed))

    def destroy(self):
        """Delete the transfer from the server if it is not yet sent.

        This method will cancel the transfer if it is still in the pending
        state (i.e. not sent or paid.) An attempt to delete a non-pending
        transfers will result in an error.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> trsf = omise.Transfer.retrieve('trsf_test_4y3miv1nhy0dceit4w4')
            >>> trsf.destroy()
            <Transfer id='trsf_test_4y3miv1nhy0dceit4w4' at 0x7f037f8707d0>
            >>> trsf.destroyed
            True

        :rtype: Customer
        """
        return self._reload_data(
            self._request('delete',
                          self._instance_path(self.id)))

    @property
    def destroyed(self):
        """Returns ``True`` if the transfer has been deleted.

        :rtype: bool
        """
        return self._attributes.get('deleted', False)