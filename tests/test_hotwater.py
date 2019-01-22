import unittest
import responses

from context import draytonwiser
from draytonwiser import APIException, ObjectNotFoundException

from BaseTest import BaseTest

class TestManager(BaseTest):

    def setUp(self):
        super(TestManager, self).setUp()

        self.source_data_file = 'all-with-itrv-and-hotwater.json'

        self.manager = draytonwiser.Manager(wiser_hub_ip=self.wiser_hub_ip, api_secret=self.token)
        self.manager.use_cache = False

    @responses.activate
    def test_hotwater_load_all(self):

        data = self.load_from_file(self.source_data_file)
        url = self.base_url #+ 'HotWater/'

        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        hotwaters = self.manager.get_all_hotwater()

        # How to handle when request isn't made due to cache?
        #self.assertEqual(responses.calls[0].request.url, url)
        self.assertEqual(len(hotwaters), 1)

if __name__ == '__main__':
    unittest.main()


