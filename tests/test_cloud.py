import unittest
import responses

from context import draytonwiser
from BaseTest import BaseTest

class TestManager(BaseTest):

    def setUp(self):
        super(TestManager, self).setUp()

        self.manager = draytonwiser.Manager(wiser_hub_ip=self.wiser_hub_ip, api_secret=self.token)

    @responses.activate
    def test_cloud_status(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'Cloud/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        cloud_info = self.manager.get_cloud()

        # How to handle when request isn't made due to cache?
        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(cloud_info.wiser_api_host, "api-nl.wiserair.com")

if __name__ == '__main__':
    unittest.main()