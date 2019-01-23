# -*- coding: utf-8 -*-
"""Base object for interacting with Wiser Heat Hub API

    The WiseBaseAPI is the root object for all classes that represent a /data/domain/[item] endpoint like
    Room or Device. These inherit from WiserBaseAPI as this allow the base class to handle all the dirty work
    translating queries into HTTP requests.

    The endpoints and manager class can then use simpler notation to get back JSON return objects.
    I.e.
        url = "System/{}".format(id)
        heating_channel_data_json = self.get_data(url)

        heating_channel = HeatingChannel(**heating_channel_data)

    With those calls the HeatingChannel class object is istantiated with the correct values from the JSON object
    via the get_data request.

    Each call to get_data will either send an HTTP request or the cache will return the data for it.
"""

import logging

import requests
import re
import time

from .exceptions import APIException,ObjectNotFoundException

from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

WISER_HUB_URL = "http://{}/data/domain/"

# TODO: Move to helper
# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def _convert_case(name):
    """Converts SomeSpecialVariable type names to some_special_variable
    for JSON to python object translation
    """
    step1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', step1).lower()

class WiserBaseAPI(object):

    # TODO: Implement cache of local response data as Wiser hub often goes unresponsive
    # Static variables for tracking whether or not request should refresh source data
    # Implement internal throttling to the API client library to play nice with the Wiser API.
    # I.e. provide a mechanism so that an unintended script doesn't hammer the controller

    _cache = None
    _cache_refreshed = None
    _data_query_count = 0
    _cache_query_count = 0

    def __init__(self, *args, **kwargs):

        self.api_secret = ""
        self.wiser_hub_ip = ""

        # TODO: Load from config
        self.use_cache = True
        self.refresh_interval = 5

        # Temp
        try:
            self.api_secret = kwargs["api_secret"]  # api_secret
            self.wiser_hub_ip = kwargs["wiser_hub_ip"]  # wiser_hub_ip
        except:
            #logger.warning("No hub IP or secret information provided")
            pass

        self._load_attributes(*args, **kwargs)

    def update_cache(self):
        self.get_data("")

    def get_data(self, item, params=None):
        """GET requests to Wiser Home hub

        Has a simple form of data caching added to handle cases when the Heat Hub is unresponsive.
        TODO: Make this easier to configure and specify how it works.

        """
        WiserBaseAPI._data_query_count += 1

        # Check for data in cache
        if self.use_cache:
            if WiserBaseAPI._cache_refreshed == None:
                WiserBaseAPI._cache_refreshed = time.time()
            else:
                last_update_diff = time.time() - WiserBaseAPI._cache_refreshed
                if last_update_diff <= self.refresh_interval:
                    data = WiserBaseAPI._cache
                    WiserBaseAPI._cache_query_count += 1

                    # TODO: See note below about temporary parsing
                    #   Parse out query for now
                    return self._parse_item_data(item, data)

        # TODO: See note below about temporary parsing
        #   Parse out query for now

        # url = "http://{}/data/domain/{}".format(self.wiser_hub_ip, item)
        url = "http://{}/data/domain/".format(self.wiser_hub_ip)

        logger.info("get_data - " + url)
        logger.info("get_data - item: " + item)

        header = {'Content-Type': 'application/json;charset=UTF-8',
                  'Secret': self.api_secret}

        try:
            logger.info("Querying Wiser Heat Hub")
            request = requests.get(url, headers=header)
        except RequestException:
            raise APIException("Error connecting to Wiser.  Possible connectivity outage.")

        if request.status_code != requests.codes.ok:
            raise APIException("Error connecting to Wiser while attempting to get thermostat data.")

        data = request.json()

        if self.use_cache:
            WiserBaseAPI._cache = data

        logger.info("get_data - query: " + str(WiserBaseAPI._data_query_count))
        logger.info("get_data - cache: " + str(WiserBaseAPI._cache_query_count))

        # TODO: See note below above temporary parsing
        #   Parse out query for now

        return self._parse_item_data(item, data)

    def patch_data(self, item, params=None):
        """PATCH requests to Wiser Home hub"""

        url = "http://{}/data/domain/{}".format(self.wiser_hub_ip, item)

        #print(url)
        header = {'Content-Type': 'application/json;charset=UTF-8',
                  'Secret': self.api_secret}

        try:
            request = requests.patch(url, json=params, headers=header)
        except RequestException:
            logger.warn("Error connecting to Wiser.  Possible connectivity outage.")
            return None

        if request.status_code != requests.codes.ok:
            logger.info("Error connecting to Wiser while attempting to get "
                        "thermostat data.")

        data = request.json()

    def _load_attributes(self, *args, **kwargs):
        # Set attributes of object from CamelCase
        for attr in kwargs.keys():
            setattr(self, _convert_case(attr), kwargs[attr])

    # TODO: For now all get_data requests are just taking the rooot /data/domain/
    #   level query and then parsing out the data as required. In the future
    #   this library may attempt to spread out the get queries as required
    #   but the slight unstability of the wiser hub means trying to reduce the number
    #   of calls for the moment.
    #   This parsing routine will make sure the correct query returns the correct subset
    #   of data like it had been real direct API call.

    def _parse_item_data(self, item, data):
        """Parses data from /data/domain/ call to serve it as if /data/domain/[Item]/[ID] was called

            This has been added to provide compatibility for the library supporting direct restful
            calls to specific endpoints. At the moment each call gets the root /data/domain/ for caching
             but may be split out into separate calls when caching is made more robust.
        """

        if item.startswith('HeatingChannel'):
            data = self._get_item_if_exists(item, data['HeatingChannel'])
        elif item.startswith('HotWater'):
            data = self._get_item_if_exists(item, data['HotWater'])
        elif item.startswith('Device'):
            data = self._get_item_if_exists(item, data['Device'])
        elif item.startswith('RoomStat'):
            data = self._get_item_if_exists(item, data['RoomStat'])
        elif item.startswith('Room'):
            data = self._get_item_if_exists(item, data['Room'])
        elif item.startswith('Cloud'):
            data = data['Cloud']
        elif item.startswith('System'):
            data = data['System']
        elif item.startswith('SmartValve'):
            data = self._get_item_if_exists(item, data['SmartValve'])
        elif item.startswith('Schedule'):
            data = self._get_item_if_exists(item, data['Schedule'])

        return data

    def _get_item_if_exists(self, item, data):
        """Retrieves the JSON object for a specific ID of a /data/domain/[item]/[id] call"""

        item_id = item[item.index('/') + 1:]
        if len(item_id) > 0 and item_id is not None:
            # we have an id
            item_id = int(item_id)
            found = False
            if item_id >= 0:
                for temp_item in data:
                    if temp_item['id'] == item_id:
                        data = temp_item
                        found = True
                        break
            if not found:
                raise ObjectNotFoundException("Item ID not found")

        return data
