
from .wiserapi import WiserBaseAPI, _convert_case

class HeatingChannel(WiserBaseAPI):
    def __init__(self, *args, **kwargs):

        # Defining default values

        self.id = None # 1
        self.name = None # "Channel-1",
        self.room_ids = None # "RoomIds": [
                                # 2,
                                # 3,
                                # 4
                                # }
        self.percentage_demand = None # 0
        self.demand_on_off_output = None # "Off",
        self.heating_relay_state = None # "Off",
        self.is_smart_valve_preventing_demand = None # true

        super(HeatingChannel, self).__init__(*args, **kwargs)
