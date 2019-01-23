# -*- coding: utf-8 -*-

from .wiserapi import WiserBaseAPI, _convert_case

class SetPoint:
    def __init__(self):
        self.time = None
        self.temperature = None

class Schedule(WiserBaseAPI):
    """Represnts the /Schedule object in the Restful API"""

    def __init__(self, *args, **kwargs):

        # Defining default values

        self.id = None
        self.type = None # "Heating"

        self.monday = None
        self.tuesday = None
        self.wednesday = None
        self.thursday = None
        self.friday = None
        self.saturday = None

        # "Sunday": {
        #     "SetPoints": [
        #         {
        #             "Time": 700,
        #             "DegreesC": 200
        #         },
        #         {
        #             "Time": 900,
        #             "DegreesC": 180
        #         },
        #         {
        #             "Time": 1600,
        #             "DegreesC": 210
        #         },
        #         {
        #             "Time": 2300,
        #             "DegreesC": -200
        #         }
        #     ]
        # },

        super(Schedule, self).__init__(*args, **kwargs)

    # def _load_attributes(self, *args, **kwargs):
    #     pass
    #     # Set attributes of object from CamelCase
    #     #print("LOAD custom schedule data!!")
    #     #for attr in kwargs.keys():
    #         #setattr(self, _convert_case(attr), kwargs[attr])
    #