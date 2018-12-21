from omise import Base, Request, api_public, api_vault, api_version


class _VaultResource(Base):

    @classmethod
    def _request(cls, *args, **kwargs):
        return Request(api_public, api_vault, api_version).send(*args, **kwargs)