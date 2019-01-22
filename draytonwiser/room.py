from .wiserapi import WiserBaseAPI, _convert_case

class Room(WiserBaseAPI):
    def __init__(self, *args, **kwargs):

        # Defining default values

        self.id = None
        self.schedule_id = None  # 3,
        self.heating_rate = None  # 1200,
        self.smart_valve_ids = []
        self.ufh_relay_ids = []  # [],
        self.name = None  # "Bedroom",
        self.mode = None  # "Auto",
        self.window_detection_active = None  # false,
        self.control_sequence_of_operation = None  # "HeatingOnly",
        self.heating_type = None  # "HydronicRadiator",
        self.current_set_point = None  # 210,
        self.set_point_origin = None  # "FromSchedule","FromManualOverride",
        self.displayed_set_point = None  # 210,
        self.scheduled_set_point = None  # 210,
        self.invalid = None  # "NothingAssigned"

        self.window_state = None # "Closed",

        # Properties added once a thermostat is attached
        self.manual_set_point = None  # 210,
        self.override_type = None  # Manual",
        self.override_setpoint = None  # 200,

        self.room_stat_id = None  # 34190,

        self.demand_type = None  # "Modulating",
        self.calculated_temperature = None  # 199,
        self.percentage_demand = None  # 20,
        self.control_output_state = None  # "Off",
        self.away_mode_suppressed = None  # false,
        self.rounded_alexa_temperature = None  # 200

        self.room_stat = None
        self.smart_valves = []

        super(Room, self).__init__(*args, **kwargs)

    def has_room_stat(self):
        if self.room_stat_id is not None and self.room_stat_id >= 0:
            return True
        return False

    def has_smart_valve(self):
        if len(self.smart_valves) > 0:
            return True
        return False

    def get_current_temperature(self):
        if self.has_room_stat():
           return self.room_stat.temperature()

        return None
        # if self.has_smart_valve():
        #     for smart_valve in room.smart_valve:
        #         print(smart_valve)

    def get_current_set_point(self):
        if self.current_set_point is None:
            return 0

        return self.current_set_point/10


    def has_device(self, device_id):

        if self.has_room_stat():
            if self.room_stat.id == device_id:
                return True

        for smart_valve_id in self.smart_valve_ids:
            if device_id == smart_valve_id:
                return True

        return False



    def set_boost(self, duration, temperature):
        if self.id is None:
            # TODO: Exception
            return

        calculated_temperature = int(temperature * 10)
        params = {
            "RequestOverride": {
                "Type": "Manual",
                "Originator": "App",
                "DurationMinutes": str(duration),
                "SetPoint": str(calculated_temperature)
            }
        }

        self.patch_data("Room/{}".format(self.id), params)

    def cancel_boost(self):
        if self.id is None:
            # TODO: Exception
            return

        params = {
            "RequestOverride": {
                "Type": "None",
                "Originator": "App",
                "DurationMinutes": 0,
                "SetPoint": 0
            }
        }

        self.patch_data("Room/{}".format(self.id), params)