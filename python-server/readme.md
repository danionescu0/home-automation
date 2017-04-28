# Requirements
* python 3.4
* redis server 
* bluetooth configured

# Install: 
## python libs  with pip3:
* install python packages using "pip3 install -r requirements.txt"
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
* web_server contains a dictionary with: 
  - static path is the absolute path to /public folder
  - api_token_secret the token secret(random value) for authorising android app api requests
  - cookie_secret used for tornado hasing algorithm 
  - application_port: self explanatory
* in redis_config redis port, host and default database nr
* in email, sending email with password and receiving email for notifications
* path for burgler alarm sounds
* in logging_config dictionary you can configure the log file and max entries
## actuators.py
* conf is a dictionary with every available actuator
* an actuator has the following propreties: state, type, device_type, communicator, send_to_device, command
* the 'state' can be True or False, defaults with the given value
* the 'type' can be 'bi', 'single' and it corresponds to the values that an actuator can have
a 'single' type can only have one state: False, the 'bi' type can have True or False
* the 'device_type' can be: door, courtain, light. powerSocket etc
* the 'communicator' can be : 'bluetooth' or 'serial' and it corresopond with the 
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
* serial port and baud rat
* aes key for encripted communication with the serial devices
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

##create a listener to respond to events
* available events to subscribe: ChangeActuatorRequest, Location, SensorUpdate
the events are located in /events folder
* first create a file in /listener folder, the file name should end up in "Listener"
the file name should describe what the listener does not on what it subscribes
* events listner uses "blinker" so we should use the import statement: "from blinker import signal"
* define a class, and in the constructor inject all dependencies needed ex: "actuator_commands"
* in the constructor subscribe to the event like this "signal("sensor_update").connect(self.callback)"
in this exampled we subscribed to "sensor_update" event and we'll receive the event in the "callback" method
inside the class

