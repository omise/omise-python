from omise.api import *
from omise.api.resources import *


class Link(MainResource, Base):
    """API class representing a link.

    This API class is used for retrieving and creating a link.
    The link can be used for creating a charge for once or multiple times.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xs8breq3htbkj03d2x'
        >>> link = omise.Link.retrieve('link_test_5086xmr74vxs0ajpo78')
        <Link id='link_test_5086xmr74vxs0ajpo78' at 0x7f79c41e9eb8>
        >>> link.amount
        10000
    """

    @classmethod
    def _collection_path(cls):
        return 'links'

    @classmethod
    def _instance_path(cls, link_id):
        return ('links', link_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a link for creating charge once or multiple times.

        See the `create a link`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> link = omise.Link.create(
            ...     amount=100000,
            ...     currency='thb',
            ...     description='Description of order-384',
            ...     title='Order-384',
            ... )
            <Link id='link_test_4xso2s8ivdej29pqnhz' at 0x7fed3241b868>

        .. _create a link: https://docs.omise.co/links-api/#create-a-link

        :param \*\*kwargs: arguments to create a link.
        :rtype: Link
        """
        return as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, link_id=None):
        """Retrieve the link details for the given :param:`link_id`.

        :param link_id: a link id to retrieve.
        :type link_id: str
        :rtype: Link
        """
        if link_id:
            return as_object(
                cls._request('get',
                             cls._instance_path(link_id)))
        return as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all links that belongs to your account.

        :rtype: omise.api.resources.lazy_collection.LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the link details.

        :rtype: Link
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))