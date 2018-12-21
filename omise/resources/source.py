from omise import Base, _as_object
from .main_resource import _MainResource

class Source(_MainResource, Base):
    """API class for creating Source.

    This API class is used for creating a source which are enabled to the
    following payment methods.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> source = omise.Source.create(
            amount=100000,
            currency='thb',
            type='internet_banking_scb'
        )
        <Source id='src_test_59ldo3ltuz7418db4ol' at 0x106473668>
        >>> charge = omise.Charge.create(
            amount=100000,
            currency='thb',
            source=source.id,
            return_uri='https://www.omise.co'
        )
        <Charge id='chrg_test_4xso2s8ivdej29pqnhz' at 0x7fed3241b990>
        >>> charge.source
        <Source id='src_test_59ldo3ltuz7418db4ol' at 0x1064736a0>

        or

        charge = omise.Charge.create(
            amount=100000,
            currency='thb',
            source={
                'type': 'internet_banking_scb'
            },
            return_uri='https://www.omise.co'
        )
    """

    @classmethod
    def create(cls, **kwargs):
        return _as_object(
            cls._request('post',
                         'sources', kwargs))