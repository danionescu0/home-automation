# Questions
* Q: Why python?

  A: It integrates well with raspberry pi and other development boards, 
  easy to code 

* Q: Why python 3.5 with type hinting?

  A: As the project grew larger type hinting proved a big help in a better 
  understanding the project and code with easy debugging

* Q: Why arduino?

  A: Being an open platform it's easy & fun to code and use. Also there are 
     a huge number of sensors and devices that integrates with ease.
     
* Q: What is the best way of communicating between devices?
  
  A: There is no best way. I've started with simple 433 MHZ receivers & transmitters 
  , migrated to bluetooth and then added HC-12 serial module and IOT devices. 
  All devices have strong and week points, it's up to you to decide what suits best.
  In the communication part of the project i've tried to abstract things away, so anyonce
  can write a communication adapter for an IOT device or a custom one.

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
## python libs with pip3:
* install python packages using "pip3 install -r requirements.txt"
* tips for installing ouimeaux: http://ouimeaux.readthedocs.io/en/latest/installation.html
* in python server folder run: pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser
* installing Zwave: https://github.com/OpenZWave/python-openzwave/blob/master/INSTALL_ARCH.rst
and https://github.com/OpenZWave/python-openzwave


# Running the servers
* start the virtual environment if you're using that
* Start Background process: "python background.py"
* Start webserver process: "python webserver.py"

# Configuration 

* config/general.py : you'll find comments inside
* config/actuators.py : actuators config, it will be moved to the ui
* config/sensors.py : actuators config, it will be moved to the ui

## bluetooth
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


# Unit tests
Unittests are using [nose2](http://nose2.readthedocs.io/en/latest/index.html)

In console run with:
````
cd python_server
nose2
````

