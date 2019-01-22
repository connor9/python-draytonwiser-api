import unittest
import responses
import json

from context import draytonwiser
from BaseTest import BaseTest

class TestManager(BaseTest):

    def setUp(self):
        super(TestManager, self).setUp()

        self.manager = draytonwiser.Manager(wiser_hub_ip=self.wiser_hub_ip, api_secret=self.token)

    @responses.activate
    def test_system_status(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'System/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        system_info = self.manager.get_system()

        # How to handle when request isn't made due to cache?
        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(system_info.active_system_version, "2.26.16-6340f5b")
        self.assertEqual(system_info.cloud_connection_status, "Connected")

if __name__ == '__main__':
    unittest.main()