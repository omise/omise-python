from omise import Base, _as_object, LazyCollection, _MainResource


class Receipt(_MainResource, Base):
    @classmethod
    def _collection_path(cls):
        return 'receipts'

    @classmethod
    def _instance_path(cls, receipt_id):
        return ('receipts', receipt_id)

    @classmethod
    def retrieve(cls, receipt_id=None):
        """Retrieve the receipt details for the given :param:`receipt_id`.

        :param receipt_id: a receipt id to retrieve.
        :type receipt_id: str
        :rtype: Receipt
        """
        if receipt_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(receipt_id)))
        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Return all receipts that belongs to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())