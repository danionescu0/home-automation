# requirements
* python 2.7
* redis server running
* bluetooth configured

# configuration in configuration.py
* replace username and password with your own
* static path is the absolute path to /public folder
* bluetooth connection strings for the three devices
* redis port, host and default database nr
* email address and password for notifications
* path for burgler alarm sounds

# configure bluetooth
* serial: http://www.uugear.com/portfolio/bluetooth-communication-between-raspberry-pi-and-arduino/
* audio: http://blog.whatgeek.com.pt/2014/04/raspberry-pi-bluetooth-wireless-speaker/

# python libs to install with pip
* for linux pybluez requires the following linux packages: libbluetooth-dev, python-dev
* sudo pip install pytz astral tornado python-dateutil redis pybluez geopy blinker

# running the servers
* sudo apt-get install screen redis-server
* in a screen or background process run the background process:
* python background.py
* in other screen or background process run
* python webserver.py