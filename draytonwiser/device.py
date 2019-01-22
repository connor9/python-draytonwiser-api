from .wiserapi import WiserBaseAPI, _convert_case
from .device_measurement import DeviceMeasurement

FULL_BATTERY_CAPACITY = 32

class Device(WiserBaseAPI):
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

        allowed_devices = ["Controller", "RoomStat", "iTRV"]
        classname = kwargs['ProductType']
        if classname not in allowed_devices:
            raise Exception("Invalid Device")

        cls = globals()[classname]

        return cls(*args, **kwargs)

    def has_measurement(self):
        if self.measurement_object_name is not None:
            return True
        return False

    def get_room_id(self):
        return self.room_id

    def get_battery_percentage(self):
        if self.battery_voltage is None:
            return None
        return (self.battery_voltage/FULL_BATTERY_CAPACITY)*100

class Controller(Device):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)

class RoomStat(Device):
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