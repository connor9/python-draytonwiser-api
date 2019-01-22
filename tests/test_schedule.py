import unittest
import responses

from context import draytonwiser
from draytonwiser import APIException, ObjectNotFoundException

from BaseTest import BaseTest

class TestManager(BaseTest):

    def setUp(self):
        super(TestManager, self).setUp()

        self.manager = draytonwiser.Manager(wiser_hub_ip=self.wiser_hub_ip, api_secret=self.token)

    @responses.activate
    def test_schedule_get_all(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'Schedule/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        schedules = self.manager.get_all_schedules()

        # How to handle when request isn't made due to cache?
        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(len(schedules), 3)

    @responses.activate
    def test_schedule_load_single(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'Schedule/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        schedule = self.manager.get_schedule(3)

        # How to handle when request isn't made due to cache?
        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(schedule.id, 3)

    @responses.activate
    def test_schedule_load_single_missing(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'Schedule/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        # How to handle when request isn't made due to cache?
        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertRaises(draytonwiser.exceptions.ObjectNotFoundException, self.manager.get_schedule, -33)


if __name__ == '__main__':
    unittest.main()