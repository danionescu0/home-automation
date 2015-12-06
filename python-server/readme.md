# requirements
* python 2.7
* redis server running

# configuration in config.py
* replace username and password with your own
* static path is the absolute path to /public folder
* bluetooth connection strings for the three devices
* redis port, host and default database nr
* email address and password for notifications

# python libs to install with pip

### sudo pip install pytz, astral, tornado, python-dateutil, redis, pybluez
### for linux pybluez requires the following linux packages: libbluetooth-dev, python-dev

# running
### in a screen or background process run the background process:
### python background.py
### in other screen or bck process run
### python webserver.py