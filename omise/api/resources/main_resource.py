import omise
from omise.api import *
from omise.request import Request


class MainResource(Base):

    @classmethod
    def _request(cls, *args, **kwargs):
        return Request(omise.api_secret, omise.api_main, omise.api_version).send(*args, **kwargs)

    def _nested_object_path(self, association_cls):
        return (
            self.__class__._collection_path(),
            self.id, association_cls._collection_path()
        )