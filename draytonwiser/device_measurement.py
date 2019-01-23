# -*- coding: utf-8 -*-
"""Device Measurement

    This is an abstraction of the RoomStat and SmartValve objects that get attached to Devices. Because the core
    device contains settings and core state properties, these related objects have what are effectively the measurements
    of what the device does. The stateful properties on the core device.

    """

from .wiserapi import WiserBaseAPI

class DeviceMeasurement(WiserBaseAPI):
    def __init__(self, *args, **kwargs):

        self.id = None  # 34190
        self.measured_temperature = None  # 224,

        super(DeviceMeasurement, self).__init__(*args, **kwargs)

    def temperature(self):
        temperature = self.measured_temperature
        if temperature is None:
            temperature = 0
        return temperature/10

class SmartValveMeasurement(DeviceMeasurement):
    def __init__(self, *args, **kwargs):

        # Defining default values

        self.mounting_orientation = None  # Vertical
        self.percentage_demand = None  # 0
        self.window_state = None  # "Closed"

        super(SmartValveMeasurement, self).__init__(*args, **kwargs)

class RoomStatMeasurement(DeviceMeasurement):
    def __init__(self, *args, **kwargs):

        # Defining default values

        self.set_point = None  # 200
        self.measured_humidity = None  # 38

        super(RoomStatMeasurement, self).__init__(*args, **kwargs)