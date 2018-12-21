from omise import Base, _as_object, LazyCollection, _MainResource


class Schedule(_MainResource, Base):
    """API class representing schedule information.

    This API class is used for retrieving or creating or deleting a scheduled
    charge.

    Basic usage::

        >>> import omise
        >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
        >>> schedule = omise.Schedule.retrieve('schd_test_4xso2s8ivdej29pqnhz')
        <Schedule id='schd_test_58509af8d7nf901pf91' at 0x1063b1f98>
    """

    @classmethod
    def _collection_path(cls):
        return 'schedules'

    @classmethod
    def _instance_path(cls, schedule_id):
        return ('schedules', schedule_id)

    @classmethod
    def create(cls, **kwargs):
        """Create a schedule charge object to
        the bank account.

        See the `create a schedule`_ section in the API documentation for list
        of available arguments.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> schedule = omise.Schedule.create(
                every=1,
                period='month',
                on={
                    'weekday_of_month': 'second_monday'
                },
                end_date='2018-05-01',
                charge={
                    'customer': 'cust_test_58505eu8s3szip5tzk8',
                    'amount': 100000,
                    'description': 'Membership fee'
                }
            )
            <Schedule id='schd_test_5851n56mg0rg90gvphj' at 0x1031d34e0>

        .. _create a schedule:
        ..     https://docs.omise.co/schedules-api#create-a-schedule

        :param \*\*kwargs: arguments to create a schedule.
        :rtype: Schedule
        """
        return _as_object(
            cls._request('post',
                         cls._collection_path(),
                         kwargs))

    @classmethod
    def retrieve(cls, schedule_id=None):
        """Retrieve the schedule object for the given :param:`schedule_id`.
        If :param:`schedule_id` is not given, all schedules will be returned
        instead.

        :param schedule_id: (optional) a schedule id to retrieve.
        :type schedule_id: str
        :rtype: Schedule
        """
        if schedule_id:
            return _as_object(
                cls._request('get',
                             cls._instance_path(schedule_id)))

        return _as_object(cls._request('get', cls._collection_path()))

    @classmethod
    def list(cls):
        """Returns all schedules that belongs to your account.

        :rtype: LazyCollection
        """
        return LazyCollection(cls._collection_path())

    def reload(self):
        """Reload the schedule details.

        :rtype: Schedule
        """
        return self._reload_data(
            self._request('get',
                          self._instance_path(self._attributes['id'])))

    def destroy(self):
        """Delete the schedule from the server.

        This method will delete the schedule.

        Basic usage::

            >>> import omise
            >>> omise.api_secret = 'skey_test_4xsjvwfnvb2g0l81sjz'
            >>> schd = omise.Schedule.retrieve('schd_test_5851n56mg0rg90gvphj')
            >>> schd.destroy()
            <Schedule id='schd_test_5851n56mg0rg90gvphj' at 0x1063b1f98>
            >>> schd.destroyed
            True
        :rtype: Schedule
        """
        return self._reload_data(
            self._request('delete',
                          self._instance_path(self.id)))

    @property
    def destroyed(self):
        """Returns ``True`` if the schedule has been deleted.

        :rtype: bool
        """
        status = self._attributes.get('status')
        return status == 'deleted'

    def occurrence(self):
        """Retrieve all occurrences for a given schedule.

        :rtype: Occurrence

        https://docs.omise.co/occurrences-api
        """
        path = self._instance_path(self._attributes['id']) + ('occurrences',)
        occurrences = _as_object(self._request('get', path))
        return occurrences