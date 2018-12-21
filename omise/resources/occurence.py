from omise import Base, _as_object, _MainResource


class Occurrence(_MainResource, Base):
    """API class representing occurrence information.

    This API class is used for retrieving a individual occurrence.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> occurrence = omise.Occurrence.retrieve('occu_test_587bugap9mm42nuddig')
        <Occurrence id='occu_test_587bugap9mm42nuddig' at 0x1063b1f98>
    """

    @classmethod
    def _instance_path(cls, occurrence_id):
        return ('occurrences', occurrence_id)

    @classmethod
    def retrieve(cls, occurrence_id):
        """Retrieve the occurrence details for the given :param:`occurrence_id`.

        :param occurrence_id: a occurrence id to retrieve.
        :type occurrence_id: str
        :rtype: Occurrence
        """
        return _as_object(
            cls._request('get',
                         cls._instance_path(occurrence_id)))