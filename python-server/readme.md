# Requirements
* python 2.7
* redis server running
* bluetooth configured
* festival installed

# Install: 
## python libs  with pip:
* install python packages using "pip install -r requirements.txt"
* tips for installing ouimeaux: http://ouimeaux.readthedocs.io/en/latest/installation.html
* in python server folder run: pip install -e git+https://github.com/mycroftai/adapt#egg=adapt-parser

# Linux packages
* sudo apt-get install screen redis-server festival
* pybluez requires the following linux packages: libbluetooth-dev, python-dev

# Running the servers
* in a screen or background process run: "python background.py"
* in other screen or background process run: "python webserver.py"

# Configuration 
## general.py
* in credentials add as many usernames/passwords as you wish
* webserver.static path is the absolute path to /public folder
* webserver.api_token_secret the token secret(random value) for authorising android app api requests
* in redis_config redis port, host and default database nr
* in email, sending email with password and receiving email for notifications
* path for burgler alarm sounds
## actuators.py
* conf is a dictionary with every available actuator
* an actuator has the following propreties: state, type, device_type, communicator, send_to_device, command
* the 'state' can be True or False, defaults with the given value
* the 'type' can be 'bi', 'single' and it corresponds to the values that an actuator can have
a 'single' type can only have one state: False, the 'bi' type can have True or False
* the 'device_type' can be: door, courtain, light. powerSocket etc
* the 'communicator' can be : 'bluetooht' or 'serial' and it corresopond with the 
communication method
* the 'send_to_device' is the name of the device that the commands will be sent to
* the 'command' is a dictionary with values for each state ex: {False: '3C|', True: '3O|'}
## sensors.py
* the 'type' can be 'humidity', 'temperature', 'presence', 'light', 'rain', 'fingerprint',
'phoneIsHome'
* value is default value
* visible is an array with visible zones: 'homepage', 'graphs'
* location can be any room name
* communication_code is a touple with communication incomming code and
node number
* last_updated is a timestamp and it denotes the last sensor updated time
## communication.py
* bluetooth connection strings for the devices
## bluetooth
* serial: http://www.uugear.com/portfolio/bluetooth-communication-between-raspberry-pi-and-arduino/


# Extending the code

## create a listener to respond to events
* available events to subscribe: ChangeActuatorRequest, Location, SensorUpdate
the events are located in /events folder
* first create a file in /listener folder, the file name should end up in "Listener"
the file name should describe what the listener does not on what it subscribes
* events listner uses "blinker" so we should use the import statement: "from blinker import signal"
* define a class, and in the constructor inject all dependencies needed ex: "actuator_commands"
* in the constructor subscribe to the event like this "signal("sensor_update").connect(self.callback)"
in this exampled we subscribed to "sensor_update" event and we'll receive the event in the "callback" method
inside the class

