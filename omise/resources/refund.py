from omise import Base, LazyCollection
from .main_resource import _MainResource


class Refund(_MainResource, Base):
    """API class representing refund information.

    This API class represents a refund information returned from the refund API.
    Refunds are not created directly with this class, but instead can be created
    using :meth:`Charge.refund`.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> charge = omise.Charge.retrieve('chrg_test_4xso2s8ivdej29pqnhz')
        >>> refund = charge.refunds.retrieve('rfnd_test_4ypcvo03ktuw0uki7un')
        <Refund id='rfnd_test_4ypcvo03ktuw0uki7un' at 0x7fd6095096f8>
        >>> refund.amount
        10000
    """

    @classmethod
    def list(cls):
        """Return all refunds that belongs to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    @classmethod
    def _collection_path(cls):
        return 'refunds'

    def reload(self):
        """Reload the refund details.

        :rtype: Refund
        """
        return self._reload_data(
            self._request('get',
                          self._attributes['location']))