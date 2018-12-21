import copy

from omise import Base, _as_object, LazyCollection, _MainResource


class Charge(_MainResource, Base):
    """API class representing a charge.

    This API class is used for retrieving and creating a charge to the
    specific credit card. There are two modes of a charge: authorize and
    capture. Authorize is for holding an amount of a charge in credit card's
    available balance and capture for capturing that authorized amount.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> charge = omise.Charge.retrieve('chrg_test_4xso2s8ivdej29pqnhz')
        <Charge id='chrg_test_4xso2s8ivdej29pqnhz' at 0x7fed3241b990>
        >>> charge.amount
        100000
    """

    @classmethod
    def _collection_path(cls):
        return 'charges'

    @classmethod
    def _instance_path(cls, charge_id):
        return ('charges', charge_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a charge to the given card details.

        See the `create a charge`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> charge = omise.Charge.create(
            ...     amount=100000,
            ...     currency='thb',
            ...     description='Order-384',
            ...     ip='127.0.0.1',
            ...     card='tokn_test_4xs9408a642a1htto8z',
            ... )
            <Charge id='chrg_test_4xso2s8ivdej29pqnhz' at 0x7fed3241b868>

        .. _create a charge: https://docs.omise.co/api/charges/#create-a-charge

        :param \*\*kwargs: arguments to create a charge.
        :rtype: Charge
        """
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, charge_id=None):
        """Retrieve the charge details for the given :param:`charge_id`.

        :param charge_id: a charge id to retrieve.
        :type charge_id: str
        :rtype: Charge
        """
        if charge_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(charge_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all charges that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the charge details.

        :rtype: Charge
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def update(self, **kwargs):
        """Update the charge details with the given arguments.

        See the `update a charge`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> charge = omise.Charge.retrieve('chrg_test_4xso2s8ivdej29pqnhz')
            >>> charge.update(description='Another description')
            <Charge id='chrg_test_4xso2s8ivdej29pqnhz' at 0x7fed3241bab8>

        :param \*\*kwargs: arguments to update a charge.
        :rtype: Charge

        .. _update a charge: https://docs.omise.co/api/charges/#update-a-charge
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._instance_path(self._attributes['id']),
                          changed))

    def capture(self):
        """Capture an authorized charge.

        :rtype: Charge
        """
        path = self._instance_path(self._attributes['id']) + ('capture',)
        return self._reload_data(self._request('post', path))

    def reverse(self):
        """Reverse an uncaptured charge.

        :rtype: Charge
        """
        path = self._instance_path(self._attributes['id']) + ('reverse',)
        return self._reload_data(self._request('post', path))

    def refund(self, **kwargs):
        """Refund a refundable charge.

        See the `create a refund`_ section in the API documentation for list of
        available arguments.

        :rtype: Refund

        .. _create a refund: https://docs.omise.co/api/refunds/#create-a-refund
        """
        path = self._instance_path(self._attributes['id']) + ('refunds',)
        refund = _as_object(self._request('post', path, kwargs))
        self.reload()
        return refund

    def list_refunds(self):
        """Return all refund that belongs to the charge

        :rtype: LazyCollection
        """
        return LazyCollection(self._nested_object_path(Refund))

    @classmethod
    def schedule(cls):
        """Retrieve all charge schedules.

        :rtype: Schedule

        .. _retrieve all charge schedules:
        https://docs.omise.co/charge-schedules-api
        """
        return _as_object(
            cls._request('get',
                         ('charges', 'schedules',)))