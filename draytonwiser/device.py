# -*- coding: utf-8 -*-

from .wiserapi import WiserBaseAPI, _convert_case
from .device_measurement import DeviceMeasurement

FULL_BATTERY_CAPACITY = 32

class Device(WiserBaseAPI):
    """Base class to represent objects in /Device

        The /Device endpoint supports different types of devices (iTRV, RoomStat, Controller, SmartPlug) that
        have common properties but specific properties as well. These properties listed can change depending on
        state of the device.

        This setup is being implemente with a base Device class that the others will inherit from to make it easier
        to handle the cases where objects have properties in common. It will also allow custom PATCH methods if these
        turn out to be different per device setting.

        Functions are created on the base object to make it easier to infer the state or capabilities of an object.

        When iterating through lots of objects the same function calls can be used and depending on if the device supports
        that function you'll get a correct response. See the all_info.py example in the /examples folder for the use
        of device.measurement() on any type of device.

        """
    def __init__(self, *args, **kwargs):

        # Base Properties
        self.id = None
        self.node_id = 0

        self.product_type = None
        self.product_identifier = None
        self.active_firmware_version = None
        self.model_identifier = None

        self.battery_voltage = None  #  31,
        self.battery_level = None  # "Normal",

        self.device_lock_enabled = None
        self.displayed_signal_strength = None  # "Good",
        self.reception_of_controller = {"Rssi": None, "Lqi": None}

        self.measurement = DeviceMeasurement()
        self.measurement_object_name = None

        self.room_id = None

        super(Device, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, *args, **kwargs):
        """Create factory method for instantiating devices. Takes the source JSON object
        and figures out which type of class it should make and then calls the constructor.
        """

        allowed_devices = ["Controller", "RoomStat", "iTRV"]
        classname = kwargs['ProductType']
        if classname not in allowed_devices:
            raise Exception("Invalid Device")

        cls = globals()[classname]

        return cls(*args, **kwargs)

    def has_measurement(self):
        """Determines if Device supports measurement"""
        if self.measurement_object_name is not None:
            return True
        return False

    def get_room_id(self):
        """Retrieves the room id"""

        # TODO: Better error checking
        return self.room_id

    def get_battery_percentage(self):
        """Returns the percentage battery remmaining for a device, if supported"""
        if self.battery_voltage is None:
            return None
        return (self.battery_voltage/FULL_BATTERY_CAPACITY)*100

class Controller(Device):
    """Implements a Controller type from /Device

    Inherits from the base Device object
    """


    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)

class RoomStat(Device):
    """Implements a RoomStat type from /Device

    Inherits from the base Device object
    """


    def __init__(self, *args, **kwargs):

        self.parent_node_id = None  # 0,

        self.hardware_version = None  # "1",
        self.serial_number = None  # "D0CF5EFFFE36D105",
        self.product_model = None  # "Thermostat",

        self.reception_of_device = {"Rssi": None, "Lqi": None}

        self.ota_image_query_count = 0  # 1,
        self.last_ota_image_query_count = 0  # 1,
        self.ota_last_image_sent_bytes = None  # 313162

        super(RoomStat, self).__init__(*args, **kwargs)

        self.measurement_object_name = "RoomStat"

class iTRV(Device):
    """Implements a iTRV type from /Device

    Inherits from the base Device object
    """


    def __init__(self, *args, **kwargs):
        self.parent_node_id = None  # 65534,

        self.hardware_version = None  # "0",
        self.serial_number = None  # "90FD9FFFFEC39AA8",
        self.product_model = None  # "ProductModel": "iTRV",

        self.reception_of_device = {"Rssi": None, "Lqi": None}

        self.ota_image_query_count = 0  # 1,
        self.last_ota_image_query_count = 0  # 1,
        self.ota_last_image_sent_bytes = None  # 313162

        self.pending_zigbee_message_mask = None  # 0

        super(iTRV, self).__init__(*args, **kwargs)

        self.measurement_object_name = "SmartValve"
