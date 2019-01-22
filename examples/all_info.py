import sys
sys.path.append('../')
from time import sleep

import logging
#logging.basicConfig(level=logging.INFO)

import json
import draytonwiser

# Simple loading of config data
with open("config.json") as f:
    json_data = json.loads(f.read())

manager = draytonwiser.Manager(wiser_hub_ip=json_data['wiser_hub_ip'], api_secret=json_data['api_secret'])


print("Wiser Home Heat Hub")
print("===================")
system_info = manager.get_system()

print("System Version:" + system_info.active_system_version)
print("Away Mode Set Point Limit:" + str(system_info.away_mode_set_point_limit))
print("Heating Relay State: " + str(manager.get_heating_relay_state()))
print("Hot Water Relay State: " + str(manager.get_hotwater_relay_state()))
print("Hot Water: " + str(manager.has_hot_water()))

print("")

print("Heating Channels")
print("****************")

heating_channels = manager.get_all_heating_channels()
for heating_channel in heating_channels:
    print(heating_channel.name + " [" + str(heating_channel.id) + "]")

print("")

print("Rooms")
print("*****")

rooms = manager.get_all_rooms()
for room in rooms:
    print(room.name + " ID:[" + str(room.id) + "]")

    print("  SetPoint: " + str(room.get_current_set_point()) + " " + room.set_point_origin)
    print("  Temp: " + str(room.get_current_temperature()))
    if room.has_room_stat():
        print("  Thermostat: " + str(room.room_stat.temperature()))

    if room.has_smart_valve():
        for smart_valve in room.smart_valve:
            print(smart_valve)

    # if device.has_measurement():
    #     print("  Temperature: " + str(device.measurement.temperature()))

print("")

print("Devices")
print("*******")

devices = manager.get_all_devices()
for device in devices:

    print("Type: " + str(type(device)))
    print("Room ID: " + str(device.get_room_id()))
    print(device.product_type + " ID:[" + str(device.id) + "]")
    print("Battery: " + str(device.get_battery_percentage()))

    if device.has_measurement():
        print("  Temperature: " + str(device.measurement.temperature()))

        if device.product_type == "RoomStat":
            print("  Humidity: " + str(device.measurement.measured_humidity))



try:
    hotwaters = manager.get_all_hotwater()
except draytonwiser.exceptions.HotWaterNotSupportedException:
    pass

#
#
# rooms = manager.get_all_rooms()
# for room in rooms:
#
#     if room.has_room_stat():
#         print(room.name + " - " + str(room.room_stat.temperature()) + "C")
#     else:
#         print(room.name)
