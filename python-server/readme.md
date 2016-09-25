# requirements
* python 2.7
* redis server running
* bluetooth configured
* festival installed

# configuration 
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
## communication.py
* bluetooth connection strings for the devices

# configure bluetooth
* serial: http://www.uugear.com/portfolio/bluetooth-communication-between-raspberry-pi-and-arduino/
* audio: http://blog.whatgeek.com.pt/2014/04/raspberry-pi-bluetooth-wireless-speaker/

# python libs to install with pip
* sudo pip install pytz astral tornado python-dateutil redis pybluez geopy blinker

# linux packages
* sudo apt-get install screen redis-server festival
* pybluez requires the following linux packages: libbluetooth-dev, python-dev

# running the servers
* in a screen or background process run: "python background.py"
* in other screen or background process run: "python webserver.py"