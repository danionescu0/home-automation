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

* config/general.py : you'll find comments inside (soon a large portion of it will be replaced by the configuration UI page)
* in the UI settings/actuators to define actuators configuration
* in the UI settings/actuators to define sensors configuration

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

** Integrate a new device type, example Zwave **

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