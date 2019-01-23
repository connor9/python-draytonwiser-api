# -*- coding: utf-8 -*-
"""Drayton Wiser API Client Library

API library to manage interactions with your Drayton Wiser Home hub.

"""

__version__ = "1.0.0"
__author__ = "David Connor"
__author_email__ = "dconnor@gmail.com"
__license__ = "MIT"

from .wiserapi import WiserBaseAPI
from .exceptions import *

from .manager import Manager

from .system import System
from .cloud import Cloud

from .heating_channel import HeatingChannel

from .room import Room
from .hotwater import HotWater
from .schedule import Schedule

from .device import Controller, RoomStat, iTRV
from .device_measurement import SmartValveMeasurement, RoomStatMeasurement

import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
