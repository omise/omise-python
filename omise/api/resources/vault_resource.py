import omise
from omise.request import Request
from .base import Base


class VaultResource(Base):

    @classmethod
    def _request(cls, *args, **kwargs):
        return Request(omise.api_public, omise.api_vault, omise.api_version).send(*args, **kwargs)
