import omise
from .utils import as_object
from omise.request import Request


class LazyCollection(object):
    """Proxy class representing a lazy collection of items."""
    def __init__(self, collection_path):
        self.collection_path = collection_path
        self._exhausted = False

    def __len__(self):
        return self._fetch_objects(limit=1, offset=0)['total']

    def __iter__(self):
        self.limit = 100
        self.listing = []

        self._list_index = 0

        return self

    def __next__(self):
        if (self.listing is None) or (self._list_index + 1 > len(self.listing)):
            self._next_batch(limit=self.limit, offset=self._list_index)

        self._list_index += 1
        return as_object(self.listing[self._list_index - 1])

    def next(self):
        return self.__next__()

    def offset(self, **kwargs):
        limit = kwargs.pop('limit', 20)
        offset = kwargs.pop('offset', 0)
        order = kwargs.pop('order', None)

        obj = self._fetch_objects(limit=limit, offset=offset, order=order)
        data = obj['data']

        return [as_object(item) for item in data]

    def _next_batch(self, **kwargs):
        if self._exhausted:
            raise StopIteration

        obj = self._fetch_objects(limit=kwargs['limit'], offset=kwargs['offset'])
        data = obj['data']

        if len(data) > 0:
            self._add_to_listing(data)
        else:
            raise StopIteration

    def _add_to_listing(self, data):
        for item in data:
            self.listing.append(item)

        if len(data) < self.limit:
            self._exhausted = True

    def _fetch_objects(self, **kwargs):
        order = kwargs.pop('order', None)

        return Request(omise.api_secret, omise.api_main, omise.api_version).send(
            'get',
            self.collection_path,
            payload={
                'limit': kwargs['limit'],
                'offset': kwargs['offset'],
                'order': order
            }
        )