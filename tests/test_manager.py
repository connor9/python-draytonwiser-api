import unittest
import responses

from context import draytonwiser
from BaseTest import BaseTest

class TestManager(BaseTest):

    def setUp(self):
        super(TestManager, self).setUp()

        self.manager = draytonwiser.Manager(wiser_hub_ip=self.wiser_hub_ip, api_secret=self.token)

    @responses.activate
    def test_get_all_heating_channels(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'HeatingChannel/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        heating_channels = self.manager.get_all_heating_channels()

        # How to handle when request isn't made due to cache?
        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(len(heating_channels), 1)
        self.assertEqual(heating_channels[0].name, "Channel-1")

    @responses.activate
    def test_get_all_rooms(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'Room/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        rooms = self.manager.get_all_rooms()

        # How to handle when request isn't made due to cache?
        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(len(rooms), 3)
        self.assertEqual(rooms[0].name, "Office")

    @responses.activate
    def test_get_all_devices(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'Device/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        devices = self.manager.get_all_devices()

        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(len(devices), 3)

    @responses.activate
    def test_get_all_schedules(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'Device/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        schedules = self.manager.get_all_schedules()

        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(len(schedules), 3)

    @responses.activate
    def test_get_all_room_stats(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'RoomStat/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        room_stats = self.manager.get_all_room_stats()

        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(len(room_stats), 1)

    @responses.activate
    def test_get_all_smart_valves(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'Device/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        smart_valves = self.manager.get_all_smart_valves()

        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(len(smart_valves), 1)

    @responses.activate
    def test_get_system(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'Device/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        system = self.manager.get_system()

        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(system.active_system_version, "2.26.16-6340f5b")

    @responses.activate
    def test_get_cloud(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'Device/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        cloud = self.manager.get_cloud()

        # self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(cloud.wiser_api_host, "api-nl.wiserair.com")

if __name__ == '__main__':
    unittest.main()