import unittest
import responses
import json

from context import draytonwiser
from BaseTest import BaseTest

from draytonwiser import APIException, ObjectNotFoundException

class TestAction(BaseTest):

    def setUp(self):
        super(TestAction, self).setUp()

        self.manager = draytonwiser.Manager(wiser_hub_ip=self.wiser_hub_ip, api_secret=self.token)

    @responses.activate
    def test_heating_channel_load_single(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'HeatingChannel/1'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        heating_channel = self.manager.get_heating_channel(1)

        self.assertEqual(heating_channel.name, "Channel-1")

    @responses.activate
    def test_heating_channel_load_single_missing(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'HeatingChannel/1'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.assertRaises(ObjectNotFoundException, self.manager.get_heating_channel, -33)

if __name__ == '__main__':
    unittest.main()


