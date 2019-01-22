import unittest
import responses

from context import draytonwiser
from BaseTest import BaseTest

from draytonwiser import APIException, ObjectNotFoundException

class TestAction(BaseTest):

    def setUp(self):
        super(TestAction, self).setUp()

        self.manager = draytonwiser.Manager(wiser_hub_ip=self.wiser_hub_ip, api_secret=self.token)

    @responses.activate
    def test_room_stat_load_single(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'RoomStat/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        room_stat = self.manager.get_room_stat(34190)

        self.assertEqual(room_stat.id, 34190)

    @responses.activate
    def test_room_stat_load_single_missing(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'RoomStat/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.assertRaises(ObjectNotFoundException, self.manager.get_room_stat, -33)

    @responses.activate
    def test_smart_valve_load_single(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'SmartValve/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        smart_valve = self.manager.get_smart_valve(34191)

        self.assertEqual(smart_valve.id, 34191)

    @responses.activate
    def test_smart_valve_load_single_missing(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'SmartValve/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.assertRaises(ObjectNotFoundException, self.manager.get_smart_valve, -33)

if __name__ == '__main__':
    unittest.main()