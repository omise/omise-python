from omise import Base, _as_object, LazyCollection
from .main_resource import _MainResource


class Transaction(_MainResource, Base):
    """API class representing a transaction.

    This API class is used for retrieving a transaction information for
    bookkeeping such as that made by :class:`Charge` and :class:`Transfer`
    operations.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> omise.Transaction.retrieve()
        <Collection at 0x7f6ef55b0ab8>
        >>> omise.Transaction.retrieve('trxn_test_4xuy2z4w5vmvq4x5pfs')
        <Transaction id='trxn_test_4xuy2z4w5vmvq4x5pfs' at 0x7fd953fa1990>
    """

    @classmethod
    def _collection_path(cls):
        return 'transactions'

    @classmethod
    def _instance_path(cls, transaction_id):
        return ('transactions', transaction_id)

    @classmethod
    def retrieve(cls, transaction_id=None):
        """Retrieve the transaction details for the given
        :param:`transaction_id`. If :param:`transaction_id` is not given, all
        transactions will be returned instead.

        :param transaction_id: (optional) a transaction id to retrieve.
        :type transaction_id: str
        :rtype: Transaction
        """
        if transaction_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(transaction_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all transactions that belongs to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the transaction details.

        :rtype: Transaction
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))