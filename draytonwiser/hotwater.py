
from .wiserapi import WiserBaseAPI, _convert_case

class HotWater(WiserBaseAPI):
    def __init__(self, *args, **kwargs):

        # Defining default values

        self.id = None # 2

        self.override_type = None # "None",
        self.schedule_id = None # 1000,
        self.mode = None # "Auto",
        self.water_heating_state = None # "Off",
        self.hot_water_relay_state = None # "Off"

        super(HotWater, self).__init__(*args, **kwargs)