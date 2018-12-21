from omise.api import *
from omise.api.resources import *


class Card(MainResource, Base):
    """API class representing card details.

    This API class represents a card information returned from other APIs.
    Cards are not created directly with this class, but instead created with
    :class:`Token`.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> customer = omise.Customer.retrieve('cust_test_4xsjvylia03ur542vn6')
        >>> card = customer.cards.retrieve('card_test_4xsjw0t21xaxnuzi9gs')
        <Card id='card_test_4xsjw0t21xaxnuzi9gs' at 0x7f406b384ab8>
        >>> card.last_digits
        '4242'
    """


    @classmethod
    def _collection_path(cls):
        return 'cards'

    def reload(self):
        """Reload the card details.

        :rtype: Card
        """
        return self._reload_data(
            self._request('get',
                          self._attributes['location']))

    def update(self, **kwargs):
        """Update the card information with the given card details.

        See the `update a card`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> cust = omise.Customer.retrieve('cust_test_4xsjvylia03ur542vn6')
            >>> card = cust.cards.retrieve('card_test_4xsjw0t21xaxnuzi9gs')
            >>> card.update(
            ...     expiration_month=11,
            ...     expiration_year=2017,
            ...     name='Somchai Praset',
            ...     postal_code='10310'
            ... )
            <Card id='card_test_4xsjw0t21xaxnuzi9gs' at 0x7f7911746ab8>

        :param \*\*kwargs: arguments to update a card.
        :rtype: Card

        .. _update a card: https://docs.omise.co/api/cards/#update-a-card
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._attributes['location'],
                          changed))

    def destroy(self):
        """Delete the card and unassociated it from the customer.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> cust = omise.Customer.retrieve('cust_test_4xsjvylia03ur542vn6')
            >>> card = cust.cards.retrieve('card_test_4xsjw0t21xaxnuzi9gs')
            >>> card.destroy()
            <Card id='card_test_4xsjw0t21xaxnuzi9gs' at 0x7f7911746868>
            >>> card.destroyed
            True

        :rtype: Card
        """
        return self._reload_data(
            self._request('delete',
                          self._attributes['location']))

    @property
    def destroyed(self):
        """Returns ``True`` if card has been deleted.

        :rtype: bool
        """
        return self._attributes.get('deleted', False)