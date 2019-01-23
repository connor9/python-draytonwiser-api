# Drayton Wiser Smart Thermostat Local Python API

This API interacts with the local API for the [Drayton Wiser Smart Thermostat](https://wiser.draytoncontrols.co.uk/).

The Drayton Wiser system provides a great option for a smart thermostat that includes a form
of local API control. 

The API connects through the local Wiser HeatHub which in turn connects to the ZigBee devices (thermostats and iTRVs).

## Table of Contents

- [Setup](#setup)
- [Features](#features)
   - [Caching](#Caching)  
- [Examples](#examples)
- [Testing](#testing)
- [Links](#links)

## Features

TODO: Add information about the features of the library highlighting:

- How WiserBaseAPI abstracts most Restful functions.
- Overview of top level objects (System, Cloud Room, Device, DeviceMeasurements, Schedule, HeatingChannel, HotWater)
- The manager class for retrieving data
- How sending data back to server works on an object by object basis but with the WiserBaseAPI doing the work
- Exceptions and error reporting
- Caching

### Library Design and Caching

The client library takes care of formatting all the remote RESTful calls
from the objects. 

TODO: Explain the caching concept in the backend.

## Setup

### Get your Wiser Hub secret token

Referenced from: https://community.openhab.org/t/drayton-wiser-thermostat-binding/35640/24

- Press the Setup button on the hub. This will start a WiserHeatXXX access point as in the regular setup instructions.
- Connect to this Wifi point with a computer (Win/Linux/Mac).  You should get an IP in the 192.168.8.0/24 range.
- Perform a GET request on the secret endpoint: 
   - Windows - In powershell `Invoke-RestMethod -Method Get -UseBasicParsing -Uri http://192.168.8.1/secret/`
   - Linux/Mac - In terminal `curl http://192.168.8.1/secret`
- The return you get back is your secret token. Keep it secret, keep it safe.
- Press the setup button on the hub and it should stop flashing and return to normal

### Get your Wiser Hub IP address

You'll need your Wiser Hub's IP address to connect to your system. You can
do this by logging into your router or some IP search tool.

TODO: Add mDNS discovery as apparently the Wiser Heat Hub supports it as per the OpenHAB discussion.

### Configure

TODO: Add PyPi instructions after submitting
 
```
pip3 install python-draytonwiser-api
```

```
import draytonwiser
manager = draytonwiser.Manager(wiser_hub_ip=HUB_IP_ADDRESS, api_secret=API_SECRET)
```

## Examples

The library is designed to make it easy to discover what commands and variables
are available in the Drayton Wiser system. If you open the various modules
in the 'draytonwiser' directory you'll see 

Most of the main data retrieval actions with the API are dealt with via the Manager
class. 

### Get basic system info

```
import draytonwiser
manager = draytonwiser.Manager(wiser_hub_ip=HUB_IP_ADDRESS, api_secret=API_SECRET)

system_info = manager.get_system()
print("System Version:" + system_info.active_system_version)
```

### Show information about Devices

This example shows how in the backend the client library will make interconnections
between related objects. Devices, Rooms, RoomStats and iTRVs are all
related and connected but come as separate endpoints in the API. These are separated
to make sending data back to them easier but when retrieving data the client
library will make the interconnections between objects for you.

```
import draytonwiser
manager = draytonwiser.Manager(wiser_hub_ip=HUB_IP_ADDRESS, api_secret=API_SECRET)

devices = manager.get_all_devices()
for device in devices:

    print("Type: " + str(type(device)))
    print("Room ID: " + str(device.get_room_id()))
    print(device.product_type + " ID:[" + str(device.id) + "]")
    print("Battery: " + str(device.get_battery_percentage()))

    # A measurement object is a related RoomStat or SmartValve. To make it
    # easier to iterate the Device class abstracts some of this away for you
    # so you don't have to always care if it's a RoomStat or an iTRV or a SmartPlug
    
    if device.has_measurement():
        print("  Temperature: " + str(device.measurement.temperature()))

        if device.product_type == "RoomStat":
            print("  Humidity: " + str(device.measurement.measured_humidity))
```

### Boost temperature manually in a Room

```
import draytonwiser
manager = draytonwiser.Manager(wiser_hub_ip=HUB_IP_ADDRESS, api_secret=API_SECRET)

room = manager.get_room(3)
room.set_boost(30, 18) # Parameters are: duration in minutes, temperature in celcius
```

### Setup examples

Copy the config.json.template file to config.json. Fill in the IP and Secret as
you retrieved them from the [Setup](#setup) stage.

### Listing all rooms

`python3 list_rooms.py`

### Listing all devices


## Testing

The tests use the responses library to mock returns from the Drayton Wiser hub.

In the tests/data directory are a series of sample returns from a Drayton Wiser Controller
which are then used to run tests.

These allow for easy development without needing to hammer your Drayton Wiser controller or without
needing to be on the same network.
 
Use pytest to run the test library. Use a virtual environment for testing with either venv or virtualenv:

    $ python3 -m venv /tmp/digitalocean_env
    $ source /tmp/digitalocean_env/bin/activate
    $ pip install -r requirements_dev.txt
    
To run all the tests:

    $ python3 -m pytest
    
### Testing with Docker

You can also test this library with docker if you don't have a local copy of python
installed.

To build the container image:

    docker build -t "python-draytonwiser-api-tests" .
    
Then you can run all the tests:

    docker run python-draytonwiser-api-tests
    
You can remove any containers and images created after these tests.    

## Links

A lot of the work in figuring out the Wiser Hub local API was done for the OpenHAB project.
The discussion on the OpenHAB forums provided a lot of insight into the endpoints and overall
architecture for the library. The Pyecobee library also provided some nice insight into a simple
but robust client library architecture. 

  * OpenHAB Discussion - https://community.openhab.org/t/drayton-wiser-thermostat-binding/35640
  * Pyecobee - https://github.com/nkgilley/python-ecobee-api - Useful for seeing different API design

Thanks to these great projects!  

