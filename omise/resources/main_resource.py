from omise import Base, Request, api_secret, api_main, api_version

class _MainResource(Base):

    @classmethod
    def _request(cls, *args, **kwargs):
        return Request(api_secret, api_main, api_version).send(*args, **kwargs)

    def _nested_object_path(self, association_cls):
        return (
            self.__class__._collection_path(),
            self.id, association_cls._collection_path()
        )