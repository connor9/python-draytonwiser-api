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
    def test_room_load_single(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'Room/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        room = self.manager.get_room(3)

        self.assertEqual(room.name, "Living Room")

    @responses.activate
    def test_room_load_single_missing(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'Room/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.assertRaises(ObjectNotFoundException, self.manager.get_room, -33)

    @responses.activate
    def test_room_set_boost(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url # + 'Room/3'

        update_url = self.base_url + 'Room/3'
        update_data = self.load_from_file(self.source_data_file)

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        responses.add(responses.PATCH, update_url,
                      body=update_data,
                      status=200,
                      content_type='application/json')

        room = self.manager.get_room(3)
        room.set_boost(30, 21)

        self.assertEqual(1, 1)

    @responses.activate
    def test_room_cancel_boost(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url # + 'Room/3'

        update_url = self.base_url + 'Room/3'
        update_data = self.load_from_file(self.source_data_file)

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        responses.add(responses.PATCH, update_url,
                      body=update_data,
                      status=200,
                      content_type='application/json')

        room = self.manager.get_room(3)
        room.cancel_boost()

        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()