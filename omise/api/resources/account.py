from .base import Base
from .main_resource import MainResource
from .utils import as_object

class Account(MainResource, Base):
    """API class representing accounts details.

    This API class is used for retrieving account information such as creator
    email or account creation date. The account retrieved by this API is the
    account associated with API secret key.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> account = omise.Account.retrieve()
        <Account id='acct_4xs8bre8a8vhrgijcjg' at 0x7f7410021990>
        >>> account.email
        None
    """

    @classmethod
    def _instance_path(cls, *args):
        return 'account'

    @classmethod
    def retrieve(cls):
        """Retrieve the account details associated with the API key.

        :rtype: Account
        """
        return as_object(cls._request('get', cls._instance_path()))

    def reload(self):
        """Reload the account details.

        :rtype: Account
        """
        return self._reload_data(self._request('get', self._instance_path()))