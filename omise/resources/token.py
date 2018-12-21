from omise import Base, _as_object, _VaultResource


class Token(_VaultResource, Base):
    """API class for creating and retrieving credit card token with the API.

    Credit card tokens are a unique ID that represents a card that could
    be used in place of where a card is required. Token can be used only
    once and invoked immediately after it is used.

    This API class is used for retrieving and creating token representing
    a card with the vault API. Unlike most other API, this API requires the
    public key to be set in ``omise.api_public``.

    Basic usage::

        >>> import omise
        >>> omise.api_public = 'pkey_test_4xs8breq32civvobx15'
        >>> token = omise.Token.retrieve('tokn_test_4xs9408a642a1htto8z')
        <Token id='tokn_test_4xs9408a642a1htto8z' at 0x7f406b384990>
        >>> token.used
        False
    """

    @classmethod
    def _collection_path(cls):
        return 'tokens'

    @classmethod
    def _instance_path(cls, token_id):
        return ('tokens', token_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a credit card token with the given card details.

        In production environment, the token should be created with
        `Omise.js <https://docs.omise.co/omise-js>`_ and credit card details
        should never go through your server. This method should only be used
        for creating fake data in test mode.

        See the `create a token`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_public = 'pkey_test_4xs8breq32civvobx15'
            >>> token = omise.Token.create(
            ...     name='Somchai Prasert',
            ...     number='4242424242424242',
            ...     expiration_month=10,
            ...     expiration_year=2018,
            ...     city='Bangkok',
            ...     postal_code='10320',
            ...     security_code=123
            ... )
            <Token id='tokn_test_4xs9408a642a1htto8z' at 0x7f406b384990>

        .. _create a token: https://docs.omise.co/api/tokens/#create-a-token

        :param \*\*kwargs: arguments to create a token.
        :rtype: Token
        """
        transformed_args = dict(card=kwargs)
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         transformed_args))

    @classmethod
    def retrieve(cls, token_id):
        """Retrieve the token details for the given :param:`token_id`.

        :param token_id: a token id to retrieve.
        :type token_id: str
        :rtype: Token
        """
        return _as_object(cls._request('get', cls._instance_path(token_id)))

    def reload(self):
        """Reload the token details.

        :rtype: Token
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))