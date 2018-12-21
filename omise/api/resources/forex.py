from omise.api import *
from omise.api.resources import *


class Forex(MainResource, Base):
    """API class retrieves the currency exchange.

    The Forex API retrieves the currency exchange rate used in
    conversions for multi-currency transactions based on account's PSP.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> forex = omise.Forex.retrieve('usd')
        <Forex at 0x10bd794e0>
        >>> forex.rate
        32.747069
    """

    @classmethod
    def retrieve(cls, currency):
        """Retrieve the exchange rate for the given :param:`currency`.

        :param currency: a currency to exchange.
        :type currency: str
        :rtype: Forex
        """
        return as_object(
            cls._request('get', ('forex', currency)))