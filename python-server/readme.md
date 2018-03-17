# FAQ
* Q: Why python?

  A: It integrates well with raspberry pi and other development boards, 
  easy to code. Also a lot of low level libraries are already written in python like 
  ZWave, WeMo etc etc :) 

* Q: Why python 3.5 with type hinting?

  A: As the project grew larger type hinting proved a big help in a better 
  understanding the project and code with easy debugging

* Q: Why arduino?

  A: Being an open platform it's easy & fun to code and use. Also there are 
     a huge number of sensors and devices that integrates with ease.
     
* Q: What is the best way of communicating between devices?
  
  A: There is no best way. I've started with simple 433 MHZ receivers/transmitters 
  , migrated to bluetooth, then to HC-12 serial module and finally IOT devices like ZWave 
   Wemo and others.
   
   Bluetooth has the limitation of 7 devices connected simoultaneous, 433Mhz receivers
    are easily clonned, IOT devices can be expensive.  
   
  I've tried to abstract the communication part so any device and now be integrated. 

* Q: Why using redis of all the databases out there?

  A: Redis is actually an all in one database, i'm using the key-value storage, 
  the ordered sets (check this [link](https://redis.io/topics/data-types)) and the [pub-sub](https://redis.io/topics/pubsub) 
  to communicate from the web interface to the separate process that controlls 
  all the things. 
  Also redis is very easy to install and configure, just apt-get and it's ready to go.

# Requirements
* python 3.5
* redis server running
* bluetooth configured

# Install: 
## virtual environment
````
virtualenv -p /path/to/python3/executable home
source ./home/bin/activate
pip install -r /home-automation_path/python-server/requirements.txt
cd /home-automation_path/python-server/
pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser
````

## other 
* clone open-zwave repository and modify config/general.py to point to the config path
````
git clone https://github.com/OpenZWave/open-zwave.git
````



# Running the servers
* Start Background process:
````
virtualenv -p /path/to/python3/executable home
source ./home/bin/activate
python /home-automation_path/python-server/background.py
````
* Start webserver process: 
````
virtualenv -p /path/to/python3/executable home
source ./home/bin/activate
python /home-automation_path/python-server/webserver.py
````

# Configuration 

1) config/general.py : you'll find comments inside the file
2) in the UI settings/actuators to define actuators configuration

*Add a zwave node example:*

* "id" -> can be any unique id
* "device_type" -> must be "zwave"
* "any name" -> it will be used in the UI
* "value" -> it's current value, it can be true/false for a switch, it will be updated automatically
* "type" -> can be "switch" or "dimmer"
* "properties" will contain "send_to_device": "the_zwave_node_id"
   and for "dimmer" it will contain  "max_value": a value between 0 and 255
   - if it conatins "shortcut" : true then it will be shown in the UI in the most frequently used
* "room" -> room name

Switch:
````
    {
        "id": "whatever_id",
        "device_type": "zwave",
        "value": false,
        "name": "Power socket (Fibaro ZWAVE)",
        "type": "switch",
        "properties": {
            "send_to_device": "0184f904.7.25.1.0"
            "shortcut": true
        },
        "room": "living"
    },
````
Dimmer:
````
    {
        "id": "fibaroWhite",
        "device_type": "zwave",
        "value": 0,
        "name": "White color",
        "type": "dimmer",
        "properties": {
            "max_value": 150,
            "send_to_device": "0184f904.3.26.6.0"
        },
        "room": "living"
    }
````

*Add a serial device example:*

The serial device sends data over the serial line, where it will be sent by a HC-12 serial communication device,
and will be interpretted by an arduino and perform some commands:

* id, value, room are the same as for zwave switches
* "device_type" -> must be "serial"
* "type" -> can be "switch"
* "name" -> it will be used in the UI
* "properties" will contain:
    - "communicator" -> "serial"
    - "send_to_device" -> the device code (it will be picked up by the arduino with the corresponding code)
    - "command" -> a dictinoary with commands to be send for the true/false states of the switch
    - if it conatins "shortcut" : true then it will be shown in the UI in the most frequently used
    the states will be interpretted by the arduino and perform the corresponding commands
    - "encription" : will be "aes"

````
    {
        "id": "some_unique_id",
        "device_type": "serial",
        "value": false,
        "name": "Main light",
        "type": "switch",
        "properties": {
            "communicator": "serial",
            "send_to_device": "L1",
            "command": {
                "true": "3O|",
                "false": "3C|"
            },
            "encription": "aes"
        },
        "room": "holway"
    }
````

*Add a bluetooth device example:*

Is the same as for serial with the following differences:

* "device_type" -> must be "bluetooth"
* does not have "encription" inside "properties"

*Add a multiple actuator trigger swith:*

It sets all actuators in a list with a value:

Obs: All the actuators must be the same type (switches, pushbuttons)

* "id" -> can be any unique id
* "device_type" -> must be "group"
* "value" -> it's current value
* "type" -> can be "switch"
* "properties" will contain:
    - "actuators" -> with a list of actuator names that will be triggered
    - "future_state" -> each actuator in the list will be set with this value

* "room" -> room name

````
    {
        "id": "some_id",
        "device_type": "group",
        "value": true,
        "name": "Close all lights",
        "type": "pushbutton",
        "properties": {
            "actuators": [
                "livingLight",
                "balconyLight"
            ],
            "future_state": false
        },
        "room": "general"
    },
````

3) in the UI settings/sensors to define sensors configuration


*Adding a Zwave sensor example:*


* "id" -> the Zwave node id
* "location" -> the room name 
* "value" -> it's current value
* "device_type" -> must be "zwave"
* "type" -> can be "humidity", "temperature", "airPressure", "light", "voltage", "rain", "presence", "airPollution",
    "fingerprint", "phoneIsHome", "flood", "power". Currently it's used in the UI 
* "properties" contains:
    - "name" -> A optional name for the actuator (for UI)
    - "polling" -> If the actuator needs to be polled for values (it doesn't emit events) specify the polling interval
* "room" -> room name

````
    {
        "id": "0184f904.4.31.1.3",
        "location": "bedroom",
        "value": 0,
        "device_type": "zwave",
        "type": "light",
        "properties": {
            "name": "Light (bedroom)"
            "polling: 60
        }
    }
````

*Adding a serial/bleutooth sensor example*

* id, location, value, type, name are the same as for the zwave sensor
* "device_type" must be "serial"
* "properties" contains:
    - "name" -> A optional name for the actuator (for UI)
    - "communication_code" -> it contains a list with the first element is sensor type abbreviation "T", "H" etc
    and the second element is it's code (number) 
    The incomming communication from the arduino through serial or bluetooth will look like "T1:30|" which means
    Temperature for sensor "1" is 30 degreeds

````
    {
        "id": "some unique id",
        "location": "holway",
        "value": 0,
        "device_type": "serial",
        "type": "presence",
        "properties": {
            "communication_code": [
                "P",
                false
            ],
            "name": "Presence (holway)"
        }
    },
````
 
4) in the UI settings/configuration you can difine the following:
- serial communication config: port, baud rate; these are used to communicate over serial with the attached HC-12 
wireless serial device, on the other end there will be arduino boards listening and interpretting commands or transmitting
sensors data. This can be deactivated if you don't use custom arduino devices with HC-12
- bluetooth communication config: a dictionary with device name: device address; these are used to communicate over bleutooth with the attached bluetooth 
serial device, on the other end there will be arduino boards listening and interpretting commands or transmitting
sensors data. This can be deactivated if you don't use custom arduino devices with bluetooth HC-05
- email config: sender gmail address, password for the sender email
- zwave communication config: port, openzwave config path; if you are using zwave devices enable this
- home defence config: notified email address, alarm lock seconds (how often you'll get an alert of type intrusion),
burgler light switches (what switches will be toggled on/off), burgler time between actions (how much max time between light toggle)


## bluetooth (optional)
To pair a bluetooth device:
```` 
bluetoothctl
     power on
     discoverable on
     agent on
     default-agent
     pairable on
     scan on
     pair xx:xx:xx:xx:xx:xx (and enter password)
     trust xx:xx:xx:xx:xx:xx 

vim /etc/bluetooth/rfcomm.conf
         rfcomm1 {
            bind yes;
            device xx:xx:xx:xx:xx:xx;
            channel 1;
            comment "Connection to some bluetooth";
         }

sudo rfcomm bind all
sudo /etc/init.d/bluetooth restart

sudo hciconfig hci0 up
````

# Extending the code

**Define a service in service container**

The service container is located in container.py

To define a service you need to import the class, and create a configuration method inside to configure the class, 
for example let's say we need to define the service for class "ActuatorCommands":

````
# import the class
from communication.actuator.ActuatorCommands import ActuatorCommands
......
# configure method inside the "Configuration" class in container.py

@singleton
def actuator_commands(self) -> ActuatorCommands:
    return ActuatorCommands(self.actuator_strategies(), self.actuators_repository(),
                            [Actuator.DeviceType.ACTION.value])

......
````

* "@singleton" is a annotation to mark that we require only one class of type "ActuatorCommands" so if we call actuator_commands
methods multiple times only the same instance will be returned
* "def actuator_commands(self) -> ActuatorCommands:" is the method name, with the specified returned type
* inside the method we configure the class by instantiating it and providing it parameters, in this case an instance of 
"ActuatorStrategies", an instance of "ActuatorsRepository", and a list of strings


**Create a listener to respond to events**

* available events to subscribe: ChangeActuatorRequestEvent, LocationEvent, SensorUpdateEvent
the events are located in /events folder
* first create a file in /listener folder, the file name should end up in "Listener"
the file name should describe what the listener does not on what it subscribes
* events listner uses "blinker" so we should use the import statement: "from blinker import signal"
* define a class, and in the constructor inject all dependencies needed ex: "actuator_commands"
* in the constructor subscribe to the event like this "signal("sensor_update").connect(self.callback)"
in this exampled we subscribed to "sensor_update" event and we'll receive the event in the "callback" method
inside the class
````
# Example:

from typeguard import typechecked
from blinker import signal

from event.SensorUpdateEvent import SensorUpdateEvent

class SomeListener:
    @typechecked()
    def __init__(self):
        signal("sensor_update").connect(self.callback)

    @typechecked()
    def callback(self, sensor_update: SensorUpdateEvent) -> None:
        # do something usefull 
````


**Integrate a new device type, example Zwave**

* define all classes in the container.py
* define an actuator strategy inside communication/actuator/ZWaveStrategy
* define a class or more to implement the low level protocol: communication/ZwaveDevice
* define a thread for listening to incomming communication and update sensors and actuators
/communication/IncommingZwaveCommunicationThread
* register the thread in background.py

# Unit tests
Unittests are using [nose2](http://nose2.readthedocs.io/en/latest/index.html)

In console run with:
````
cd python_server
nose2
````