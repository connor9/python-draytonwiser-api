import sys
sys.path.append('../')
from time import sleep

import json
import draytonwiser

# Simple loading of config data
with open("config.json") as f:
    json_data = json.loads(f.read())

manager = draytonwiser.Manager(wiser_hub_ip=json_data['wiser_hub_ip'], api_secret=json_data['api_secret'])

room = manager.get_room(3)

room.set_boost(30, 18)
sleep(10)
room.cancel_boost()