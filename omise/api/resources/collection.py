from omise.api import *


class Collection(Base):
    """Proxy class representing a collection of items."""

    def __len__(self):
        return len(self._attributes['data'])

    def __iter__(self):
        for obj in self._attributes['data']:
            yield as_object(obj)

    def __getitem__(self, item):
        return as_object(self._attributes['data'][item])

    def retrieve(self, object_id=None):
        """Retrieve the specific :param:`object_id` from the list of objects.

        If no :param:`object_id` is given, a list of all objects will be
        returned instead. This is equivalent of calling ``list(collection)``.

        :param object_id: an object id to retrieve.
        :type object_id: str
        :rtype: T <= Base
        """
        if object_id is None:
            return list(self)
        else:
            for obj in self._attributes['data']:
                if obj['id'] == object_id:
                    return as_object(obj)