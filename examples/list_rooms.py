import sys
sys.path.append('../')
from time import sleep

import logging
logging.basicConfig(level=logging.INFO)

import json
import draytonwiser

# Simple loading of config data
with open("config.json") as f:
    json_data = json.loads(f.read())

manager = draytonwiser.Manager(wiser_hub_ip=json_data['wiser_hub_ip'], api_secret=json_data['api_secret'])

system_info = manager.get_system()
print("System Version:" + system_info.active_system_version)

rooms = manager.get_all_rooms()
for room in rooms:

    if room.has_room_stat():
        print(room.name + " - " + str(room.room_stat.temperature()) + "C")
    else:
        print(room.name)
