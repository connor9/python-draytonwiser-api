# -*- coding: utf-8 -*-
"""Manager object for retrieving objects from Heat Hub.

    The Heat hub client library is generally meant to be used via the Manager class for retrieving data and setting
    up classes for post backs.

    i.e.
        import draytonwiser
        manager = draytonwiser.Manager(wiser_hub_ip=HUB_IP_ADDRESS, api_secret=API_SECRET)
        devices = manager.get_all_devices()

    TODO: More about this architecture.

"""

from .wiserapi import WiserBaseAPI

from .system import System
from .cloud import Cloud

from .heating_channel import HeatingChannel

from .room import Room
from .hotwater import HotWater
from .schedule import Schedule

from .device import Device, Controller, RoomStat, iTRV
from .device_measurement import SmartValveMeasurement, RoomStatMeasurement

from .exceptions import *

class Manager(WiserBaseAPI):

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)

    def has_hot_water(self):
        try:
            hotwaters = self.get_all_hotwater()

            if len(hotwaters) > 0:
                return True
        except HotWaterNotSupportedException:
            # No worries
            pass

        return False

        # Get hot water status (On/Off)

    def get_heating_relay_state(self):

        status = "Off"

        # There could be multiple heating channels,
        heating_channels = self.get_all_heating_channels()

        for heating_channel in heating_channels:
            if heating_channel.heating_relay_state == "On":
                status = "On"

        return status

        # Get hot water status (On/Off)

    def get_hotwater_relay_state(self):

        status = "Off"

        # There could be multiple heating channels,
        try:
            hotwaters = self.get_all_hotwater()

            for hotwater in hotwaters:
                if hotwater.hot_water_relay_state == "On":
                    status = "On"
        except HotWaterNotSupportedException:
            status = "Off"

        return status

    def get_all_heating_channels(self):

        params = dict()
        data = self.get_data(item="HeatingChannel/", params=params)

        heating_channels = list()

        for jsoned in data:

            heating_channel = HeatingChannel(**jsoned)
            heating_channel.wiser_hub_ip = self.wiser_hub_ip
            heating_channel.api_secret = self.api_secret

            # Load related Room properties and parameters

            heating_channels.append(heating_channel)

        return heating_channels

    def get_heating_channel(self, id):

        url = "HeatingChannel/{}".format(id)
        heating_channel_data = self.get_data(url)

        heating_channel = HeatingChannel(**heating_channel_data)
        heating_channel.wiser_hub_ip = self.wiser_hub_ip
        heating_channel.api_secret = self.api_secret

        return heating_channel

    def get_all_rooms(self):

        params = dict()
        data = self.get_data(item="Room/", params=params)

        rooms = list()

        for jsoned in data:
            room = self.get_room(jsoned['id'])
            rooms.append(room)

        return rooms

    def get_room(self, item_id):

        url = "Room/{}".format(item_id)

        room_data = self.get_data(url)
        room_data['wiser_hub_ip'] = self.wiser_hub_ip
        room_data['api_secret'] = self.api_secret

        room = Room(**room_data)

        # TODO: Need link these in a more clever way

        # Room Stats
        try:
            room.room_stat = self.get_room_stat(room.room_stat_id)
        except ValueError:
            room.room_stat = None

        return room

    def get_all_devices(self):

        params = dict()
        data = self.get_data(item="Device/", params=params)

        devices = list()

        for jsoned in data:
            device = self.get_device(jsoned['id'])
            devices.append(device)

        return devices

    def get_device(self, item_id):

        url = "Device/{}".format(item_id)

        device_data = self.get_data(url)
        device_data['wiser_hub_ip'] = self.wiser_hub_ip
        device_data['api_secret'] = self.api_secret

        device = Device.create(**device_data)

        # TODO: Need to link these in a more clever way.
        if device.measurement_object_name == "SmartValve":
            device.measurement = self.get_smart_valve(device.id)
        elif device.measurement_object_name == "RoomStat":
            device.measurement = self.get_room_stat(device.id)

        # TODO: Find matching room
        rooms = self.get_all_rooms()
        for room in rooms:
            if room.has_device(device.id):
                device.room_id = room.id
                break

        return device

    def get_all_schedules(self):

        params = dict()
        data = self.get_data(item="Schedule/", params=params)

        schedules = list()

        for jsoned in data:

            schedule = Schedule(**jsoned)
            schedule.wiser_hub_ip = self.wiser_hub_ip
            schedule.api_secret = self.api_secret

            schedules.append(schedule)

        return schedules

    def get_schedule(self, id):

        url = "Schedule/{}".format(id)
        schedule_data = self.get_data(url)


        schedule = Schedule(**schedule_data)
        schedule.wiser_hub_ip = self.wiser_hub_ip
        schedule.api_secret = self.api_secret

        return schedule

    def get_all_room_stats(self):

        params = dict()
        data = self.get_data(item="RoomStat/", params=params)

        room_stats = list()

        for jsoned in data:
            room_stat = RoomStatMeasurement(**jsoned)
            room_stat.wiser_hub_ip = self.wiser_hub_ip
            room_stat.api_secret = self.api_secret

            room_stats.append(room_stat)

        return room_stats

    def get_room_stat(self, item_id):

        url = "RoomStat/{}".format(item_id)
        room_stat_data = self.get_data(url)
        room_stat_data['wiser_hub_ip'] = self.wiser_hub_ip
        room_stat_data['api_secret'] = self.api_secret

        room_stat = RoomStatMeasurement(**room_stat_data)

        return room_stat

    def get_all_smart_valves(self):

        params = dict()
        data = self.get_data(item="SmartValve/", params=params)

        smart_valves = list()

        for jsoned in data:

            smart_valve = SmartValveMeasurement(**jsoned)
            smart_valve.wiser_hub_ip = self.wiser_hub_ip
            smart_valve.api_secret = self.api_secret

            smart_valves.append(smart_valve)

        return smart_valves

    def get_smart_valve(self, id):

        url = "SmartValve/{}".format(id)
        smart_valve_data = self.get_data(url)

        smart_valve = SmartValveMeasurement(**smart_valve_data)
        smart_valve.wiser_hub_ip = self.wiser_hub_ip
        smart_valve.api_secret = self.api_secret

        return smart_valve

    def get_system(self):

        params = dict()
        data = self.get_data(item="System/", params=params)

        system = System(**data)
        system.wiser_hub_ip = self.wiser_hub_ip
        system.api_secret = self.api_secret

        return system

    def get_cloud(self):

        params = dict()
        data = self.get_data(item="Cloud/", params=params)

        cloud = Cloud(**data)
        cloud.wiser_hub_ip = self.wiser_hub_ip
        cloud.api_secret = self.api_secret

        return cloud

    def get_all_hotwater(self):

        params = dict()
        try:
            data = self.get_data(item="HotWater/", params=params)
        except KeyError:
            raise HotWaterNotSupportedException

        hotwaters = list()

        for jsoned in data:
            hotwater = HotWater(**jsoned)
            hotwater.wiser_hub_ip = self.wiser_hub_ip
            hotwater.api_secret = self.api_secret

            # Load related Room properties and parameters

            hotwaters.append(hotwater)

        return hotwaters