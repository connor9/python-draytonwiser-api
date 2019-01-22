import os
import unittest

import logging
#logging.basicConfig(level=logging.INFO)

class BaseTest(unittest.TestCase):

    def setUp(self):

        self.wiser_hub_ip = '192.168.1.171'
        self.base_url = url = "http://{}/data/domain/".format(self.wiser_hub_ip)
        self.token = "afaketokenthatwillworksincewemockthings"
        self.source_data_file = "all-with-itrv.json"
        #self.source_data_file = "all-with-itrv-and-hotwater.json"


    def load_from_file(self, json_file):
        filename = os.path.dirname(__file__)
        with open(os.path.join(filename, 'data/%s' % json_file), 'r') as f:
            return f.read()