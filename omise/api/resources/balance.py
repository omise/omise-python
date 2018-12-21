from omise.api import *
from omise.api.resources import *


class Balance(MainResource, Base):
    """API class representing balance details.

    This API class is used for retrieving current balance of the account.
    Balance do not have ID associated to it and is immutable.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> balance = omise.Balance.retrieve()
        <Balance at 0x7f7410021868>
        >>> balance.total
        0
    """

    @classmethod
    def _instance_path(cls, *args):
        return 'balance'

    @classmethod
    def retrieve(cls):
        """Retrieve the balance details for current account.

        :rtype: Balance
        """
        return as_object(cls._request('get', cls._instance_path()))

    def reload(self):
        """Reload the balance details.

        :rtype: Balance
        """
        return self._reload_data(self._request('get', self._instance_path()))