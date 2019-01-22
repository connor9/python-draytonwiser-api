import unittest
import responses

from context import draytonwiser
from draytonwiser import APIException, ObjectNotFoundException

from BaseTest import BaseTest

class TestAction(BaseTest):

    def setUp(self):
        super(TestAction, self).setUp()

        self.manager = draytonwiser.Manager(wiser_hub_ip=self.wiser_hub_ip, api_secret=self.token)

    @responses.activate
    def test_device_load_single(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'Device/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        device = self.manager.get_device(34190)

        self.assertEqual(device.id, 34190)

    @responses.activate
    def test_device_load_single_2(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'Device/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        device = self.manager.get_device(34191)

        self.assertEqual(device.id, 34191)

    @responses.activate
    def test_device_load_single_missing(self):
        data = self.load_from_file(self.source_data_file)
        url = self.base_url  # + 'Device/3'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        self.assertRaises(draytonwiser.exceptions.ObjectNotFoundException, self.manager.get_device, 3)

if __name__ == '__main__':
    unittest.main()