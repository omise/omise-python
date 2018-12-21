from omise import Base, LazyCollection, _as_object, Card
from .main_resource import _MainResource

class Customer(_MainResource, Base):
    """API class representing a customer in an account.

    This API class is used for retrieving and creating a customer in an
    account. The customer can be used for storing credit card details
    (using token) for later use.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> customer = omise.Customer.retrieve('cust_test_4xtrb759599jsxlhkrb')
        <Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7fb02625f990>
        >>> customer.email
        'john.doe@example.com'
    """

    @classmethod
    def _collection_path(cls):
        return 'customers'

    @classmethod
    def list(cls):
        """Return all customers that belongs to your account

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    @classmethod
    def _instance_path(cls, customer_id):
        return ('customers', customer_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a customer with the given card token.

        See the `create a customer`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> customer = omise.Customer.create(
            ...     description='John Doe (id: 30)',
            ...     email='john.doe@example.com',
            ...     card='tokn_test_4xs9408a642a1htto8z',
            ... )
            <Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7fb02625fab8>

        .. _create a customer:
        ..     https://docs.omise.co/api/customers/#create-a-customer

        :param \*\*kwargs: arguments to create a customer.
        :rtype: Customer
        """
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, customer_id=None):
        """Retrieve the customer details for the given :param:`customer_id`.

        :param customer_id: a customer id to retrieve.
        :type customer_id: str
        :rtype: Customer
        """
        if customer_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(customer_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    def reload(self):
        """Reload the customer details.

        :rtype: Customer
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def update(self, **kwargs):
        """Update the customer details with the given arguments.

        See the `update a customer`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjzx'
            >>> cust = omise.Customer.retrieve('cust_test_4xtrb759599jsxlhkrb')
            >>> cust.update(
            ...     email='john.smith@example.com',
            ...     description='Another description',
            ... )
            <Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7f319de7f990>

        :param \*\*kwargs: arguments to update a customer.
        :rtype: Customer

        .. _update a customer:
        ..     https://docs.omise.co/api/customers/#update-a-customer
        """
        changed = copy.deepcopy(self.changes)
        changed.update(kwargs)
        return self._reload_data(
            self._request('patch',
                          self._instance_path(self._attributes['id']),
                          changed))

    def destroy(self):
        """Delete the customer from the server.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjzx'
            >>> cust = omise.Customer.retrieve('cust_test_4xtrb759599jsxlhkrb')
            >>> cust.destroy()
            <Customer id='cust_test_4xtrb759599jsxlhkrb' at 0x7ff72d8d1990>
            >>> cust.destroyed
            True

        :rtype: Customer
        """
        return self._reload_data(
            self._request('delete',
                          self._instance_path(self._attributes['id'])))

    def list_cards(self):
        """Returns all cards that belong to a given customer.

        :rtype: LazyCollection
        """
        return LazyCollection(self._nested_object_path(Card))

    def list_schedules(self):
        """Returns all charge schedules that belong to a given customer.

        :rtype: LazyCollection
        """
        return LazyCollection(self._nested_object_path(Schedule))

    @property
    def destroyed(self):
        """Returns ``True`` if customer has been deleted.

        :rtype: bool
        """
        return self._attributes.get('deleted', False)

    def schedule(self):
        """Retrieve all charge schedules that belong to customer.

        :rtype: Schedule

        .. _retrieve all charge schedules for a given customer:
        https://docs.omise.co/charge-schedules-api
        """
        path = self._instance_path(self._attributes['id']) + ('schedules',)
        schedules = _as_object(self._request('get', path))
        return schedules