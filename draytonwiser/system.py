# -*- coding: utf-8 -*-

from .wiserapi import WiserBaseAPI

class System(WiserBaseAPI):
    """Represnts the /System object in the Restful API"""

    def __init__(self, *args, **kwargs):
        # Defining default values

        self.pairing_status = None # ": "Paired",
        self.override_type = None # "Away"
        self.time_zone_offset = None # ": 0,
        self.automatic_daylight_saving = None # ": true,
        self.system_mode = None # ": "Heat",
        self.version = None # ": 6,
        self.fota_enabled = None # ": true,
        self.valve_protection_enabled = None # ": false,
        self.away_mode_affects_hot_water = None # ": true,
        self.away_mode_set_point_limit = None # ": 150,
        self.boiler_settings = None
            # # ": {
            #     "ControlType": "HeatSourceType_RelayControlled",
            #     "FuelType": "Gas",
            #     "CycleRate": "CPH_6",
            #     "OnOffHysteresis": 5
            # },
        self.zigbee_settings = {"SuppressApsAcks": None} # ": {"SuppressApsAcks": true}
        self.cooling_mode_default_setpoint = None # ": 210,
        self.cooling_away_mode_setpoint_limit = None # ": 240,
        self.comfort_mode_enabled = None # ": false,
        self.preheat_time_limit = None # ": 10800,
        self.degraded_mode_setpoint_threshold = None # ": 180,
        self.unix_time = None # ": 1546640700,
        self.active_system_version = None # ": "2.26.16-6340f5b",
        self.cloud_connection_status = None # ": "Connected",
        self.zigbee_module_version = None # ": "R311 B030517",
        self.zigbee_eui = None # ": "90FD9FFFFEAA6AA7",
        self.local_date_and_time = None

            # # ": {
            #         "Year": 2019,
            #         "Month": "January",
            #         "Date": 4,
            #         "Day": "Friday",
            #         "Time": 2225
            #     },
        self.heating_button_override_state = None # ": "Off",
        self.hot_water_button_override_state = None # ": "Off"

        super(System, self).__init__(*args, **kwargs)
