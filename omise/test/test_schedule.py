import mock
import unittest

from .helper import _ResourceMixin


class ScheduleTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Schedule
        return Schedule

    def _getCollectionClass(self):
        from .. import Collection
        return Collection

    def _makeOne(self):
        return self._getTargetClass().from_data({
            "object": "schedule",
            "id": "schd_test",
            "livemode": False,
            "location": "/schedules/schd_test",
            "status": "active",
            "deleted": False,
            "every": 1,
            "period": "month",
            "on": {
                "days_of_month": [
                    1
                ]
            },
            "in_words": "Every 1 month(s) on the 1st",
            "start_date": "2017-06-02",
            "end_date": "2018-06-02",
            "charge": {
                "amount": 100000,
                "currency": "thb",
                "description": "Charge every month on the first date",
                "customer": "cust_test_58655j2ez4elik6t2xc",
                "card": None
            },
            "occurrences": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2017-06-02T18:52:05+07:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "order": None,
                "location": "/schedules/schd_test/occurrences",
                "data": []
            },
            "next_occurrence_dates": [],
            "created": "2017-06-02T08:28:40Z"
        })

    @mock.patch('requests.post')
    def test_create(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "schedule",
            "id": "schd_test",
            "livemode": false,
            "location": "/schedules/schd_test",
            "status": "active",
            "deleted": false,
            "every": 1,
            "period": "month",
            "on": {
                "weekday_of_month": "2nd_monday"
            },
            "in_words": "Every 1 month(s) on the 2nd Monday",
            "start_date": "2017-06-02",
            "end_date": "2018-05-01",
            "charge": {
                "amount": 100000,
                "currency": "thb",
                "description": "Membership fee",
                "customer": "cust_test_58655j2ez4elik6t2xc",
                "card": null
            },
            "occurrences": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2017-06-02T19:14:21+07:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "order": null,
                "location": "/schedules/schd_test/occurrences",
                "data": []
            },
            "next_occurrence_dates": [
                "2017-06-12",
                "2017-07-10",
                "2017-08-14",
                "2017-09-11",
                "2017-10-09",
                "2017-11-13",
                "2017-12-11",
                "2018-01-08",
                "2018-02-12",
                "2018-03-12",
                "2018-04-09"
            ],
            "created": "2017-06-02T12:14:21Z"
        }""")

        schedule = class_.create(
            every=1,
            period='month',
            on={
                'weekday_of_month': 'second_monday'
            },
            end_date='2018-05-01',
            charge={
                'customer': 'cust_test_58655j2ez4elik6t2xc',
                'amount': 100000,
                'description': 'Membership fee'
            }
        )

        self.assertTrue(isinstance(schedule, class_))
        self.assertEqual(schedule.id, 'schd_test')
        self.assertEqual(schedule.every, 1)
        self.assertEqual(schedule.period, 'month')
        self.assertEqual(schedule.status, 'active')
        self.assertEqual(schedule.start_date, '2017-06-02')
        self.assertEqual(schedule.end_date, '2018-05-01')
        self.assertRequest(
            api_call,
            'https://api.omise.co/schedules',
            {
                'every': 1,
                'period': 'month',
                'on': {
                    'weekday_of_month': 'second_monday'
                },
                'end_date': '2018-05-01',
                'charge': {
                    'customer': 'cust_test_58655j2ez4elik6t2xc',
                    'amount': 100000,
                    'description': 'Membership fee'
                }
            }
        )

    @mock.patch('requests.get')
    def test_retrieve(self, api_call):
        class_ = self._getTargetClass()
        self.mockResponse(api_call, """{
            "object": "schedule",
            "id": "schd_test",
            "livemode": false,
            "location": "/schedules/schd_test",
            "status": "active",
            "deleted": false,
            "every": 1,
            "period": "month",
            "on": {
                "weekday_of_month": "2nd_monday"
            },
            "in_words": "Every 1 month(s) on the 2nd Monday",
            "start_date": "2017-06-02",
            "end_date": "2018-05-01",
            "charge": {
                "amount": 100000,
                "currency": "thb",
                "description": "Membership fee",
                "customer": "cust_test_58655j2ez4elik6t2xc",
                "card": null
            },
            "occurrences": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2017-06-02T19:14:21+07:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "order": null,
                "location": "/schedules/schd_test/occurrences",
                "data": []
            },
            "next_occurrence_dates": [
                "2017-06-12",
                "2017-07-10",
                "2017-08-14",
                "2017-09-11",
                "2017-10-09",
                "2017-11-13",
                "2017-12-11",
                "2018-01-08",
                "2018-02-12",
                "2018-03-12",
                "2018-04-09"
            ],
            "created": "2017-06-02T12:14:21Z"
        }""")

        schedule = class_.retrieve('schd_test')
        self.assertTrue(isinstance(schedule, class_))
        self.assertTrue(schedule.id, 'schd_test')
        self.assertEqual(schedule.every, 1)
        self.assertEqual(schedule.period, 'month')
        self.assertEqual(schedule.status, 'active')
        self.assertEqual(schedule.start_date, '2017-06-02')
        self.assertEqual(schedule.end_date, '2018-05-01')
        self.assertRequest(api_call, 'https://api.omise.co/schedules/schd_test')

    @mock.patch('requests.get')
    def test_retrieve_no_args(self, api_call):
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2017-06-02T12:34:43+07:00",
            "offset": 0,
            "limit": 20,
            "total": 1,
            "order": "chronological",
            "location": "/schedules",
            "data": [
                {
                    "object": "schedule",
                    "id": "schd_test",
                    "livemode": false,
                    "location": "/schedules/schd_test",
                    "status": "active",
                    "deleted": false,
                    "every": 1,
                    "period": "month",
                    "on": {
                        "weekday_of_month": "2nd_monday"
                    },
                    "in_words": "Every 1 month(s) on the 2nd Monday",
                    "start_date": "2017-06-02",
                    "end_date": "2018-05-01",
                    "charge": {
                        "amount": 100000,
                        "currency": "thb",
                        "description": "Membership fee",
                        "customer": "cust_test_58655j2ez4elik6t2xc",
                        "card": null
                    },
                    "occurrences": {
                        "object": "list",
                        "from": "1970-01-01T07:00:00+07:00",
                        "to": "2017-06-02T19:14:21+07:00",
                        "offset": 0,
                        "limit": 20,
                        "total": 0,
                        "order": null,
                        "location": "/schedules/schd_test/occurrences",
                        "data": []
                    },
                    "next_occurrence_dates": [
                        "2017-06-12",
                        "2017-07-10",
                        "2017-08-14",
                        "2017-09-11",
                        "2017-10-09",
                        "2017-11-13",
                        "2017-12-11",
                        "2018-01-08",
                        "2018-02-12",
                        "2018-03-12",
                        "2018-04-09"
                    ],
                    "created": "2017-06-02T12:14:21Z"
                }
            ]
        }""")

        schedules = class_.retrieve()
        self.assertTrue(isinstance(schedules, collection_class_))
        self.assertTrue(isinstance(schedules[0], class_))
        self.assertTrue(schedules[0].id, 'schd_test')
        self.assertEqual(schedules[0].every, 1)
        self.assertEqual(schedules[0].period, 'month')
        self.assertEqual(schedules[0].status, 'active')
        self.assertEqual(schedules[0].start_date, '2017-06-02')
        self.assertEqual(schedules[0].end_date, '2018-05-01')
        self.assertRequest(api_call, 'https://api.omise.co/schedules')

    @mock.patch('requests.get')
    def test_reload(self, api_call):
        schedule = self._makeOne()
        class_ = self._getTargetClass()

        self.assertTrue(isinstance(schedule, class_))
        self.assertEqual(schedule.every, 1)
        self.assertEqual(schedule.period, "month")

        self.mockResponse(api_call, """{
            "object": "schedule",
            "id": "schd_test",
            "livemode": false,
            "location": "/schedules/schd_test",
            "status": "active",
            "deleted": false,
            "every": 7,
            "period": "week",
            "on": {
                "weekday_of_month": "2nd_monday"
            },
            "in_words": "Every 1 month(s) on the 2nd Monday",
            "start_date": "2017-06-02",
            "end_date": "2018-05-01",
            "charge": {
                "amount": 100000,
                "currency": "thb",
                "description": "Membership fee",
                "customer": "cust_test_58655j2ez4elik6t2xc",
                "card": null
            },
            "occurrences": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2017-06-02T19:14:21+07:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "order": null,
                "location": "/schedules/schd_test/occurrences",
                "data": []
            },
            "next_occurrence_dates": [
                "2017-06-12",
                "2017-07-10",
                "2017-08-14",
                "2017-09-11",
                "2017-10-09",
                "2017-11-13",
                "2017-12-11",
                "2018-01-08",
                "2018-02-12",
                "2018-03-12",
                "2018-04-09"
            ],
            "created": "2017-06-02T12:14:21Z"
        }""")

        schedule.reload()
        self.assertEqual(schedule.every, 7)
        self.assertEqual(schedule.period, 'week')
        self.assertRequest(api_call, 'https://api.omise.co/schedules/schd_test')

    @mock.patch('requests.delete')
    def test_destroy(self, api_call):
        schedule = self._makeOne()
        class_ = self._getTargetClass()

        self.mockResponse(api_call, """{
            "object": "schedule",
            "id": "schd_test",
            "livemode": false,
            "location": "/schedules/schd_test",
            "status": "deleted",
            "deleted": true,
            "every": 1,
            "period": "month",
            "on": {
                "weekday_of_month": "2nd_monday"
            },
            "in_words": "Every 1 month(s) on the 2nd Monday",
            "start_date": "2017-06-02",
            "end_date": "2018-05-01",
            "charge": {
                "amount": 100000,
                "currency": "thb",
                "description": "Membership fee",
                "customer": "cust_test_58655j2ez4elik6t2xc",
                "card": null
            },
            "occurrences": {
                "object": "list",
                "from": "1970-01-01T07:00:00+07:00",
                "to": "2017-06-02T19:14:21+07:00",
                "offset": 0,
                "limit": 20,
                "total": 0,
                "order": null,
                "location": "/schedules/schd_test/occurrences",
                "data": []
            },
            "next_occurrence_dates": [
                "2017-06-12",
                "2017-07-10",
                "2017-08-14",
                "2017-09-11",
                "2017-10-09",
                "2017-11-13",
                "2017-12-11",
                "2018-01-08",
                "2018-02-12",
                "2018-03-12",
                "2018-04-09"
            ],
            "created": "2017-06-02T12:14:21Z"
        }""")

        self.assertTrue(isinstance(schedule, class_))
        self.assertEqual(schedule.status, 'active')
        self.assertEqual(schedule.deleted, False)

        schedule.destroy()
        self.assertTrue(schedule.destroyed)
        self.assertEqual(schedule.status, 'deleted')
        self.assertEqual(schedule.deleted, True)

        self.assertRequest(
            api_call,
            'https://api.omise.co/schedules/schd_test'
        )

    @mock.patch('requests.get')
    def test_occurrence(self, api_call):
        schedule = self._makeOne()
        class_ = self._getTargetClass()
        collection_class_ = self._getCollectionClass()
        self.mockResponse(api_call, """{
            "object": "list",
            "from": "1970-01-01T07:00:00+07:00",
            "to": "2017-06-02T12:34:43+07:00",
            "offset": 0,
            "limit": 20,
            "total": 1,
            "order": "chronological",
            "location": "/customers/cust_test/schedules",
            "data": [
                {
                    "object": "occurrence",
                    "id": "occu_test",
                    "location": "/occurrences/occu_test",
                    "schedule": "schd_test",
                    "schedule_date": "2017-06-05",
                    "retry_date": null,
                    "processed_at": "2017-06-05T08:29:15Z",
                    "status": "successful",
                    "message": null,
                    "result": "chrg_test",
                    "created": "2017-06-05T08:29:13Z"
                }
            ]
        }""")

        self.assertTrue(isinstance(schedule, class_))

        occurrences = schedule.occurrence()
        self.assertTrue(isinstance(occurrences, collection_class_))
        self.assertEqual(occurrences.total, 1)
        self.assertEqual(occurrences[0].id, 'occu_test')
        self.assertEqual(occurrences[0].location, '/occurrences/occu_test')
        self.assertEqual(occurrences[0].status, 'successful')
        self.assertEqual(occurrences[0].result, 'chrg_test')

        self.assertRequest(
            api_call,
            'https://api.omise.co/schedules/schd_test/occurrences'
        )
