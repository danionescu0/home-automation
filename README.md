# Home automation project #

Yet another home automation project. The main concern of the project is keeping price down, it's a DIY project for makers and hackers:) it is based on a raspberry pi (or another linux compatible board) and arduinos.

### The project is composed of three parts:

* First the python server (project brain) located in python-server

* Second the arduino sketches located in arduino-sketches. The sketches are for custom devices that control various actuators and collect data from sensors.

* Third and optional an android application located [here](https://bitbucket.org/danionescu/androidhomeautomation). The application is a webview and besides that it sends from time to time your location the server, which can enable or disables various thisgs like the fingerprint scanner


## First some screenshots ##

### The main menu which contains the sensors listings, and all the "switches" ###
![homepage.png](https://bitbucket.org/repo/GERMME/images/2673176056-homepage.png)

### The sensors graphs menu ###
![sensors.png](https://bitbucket.org/repo/GERMME/images/3652208713-sensors.png)

### If this than that ###
![ifttt.png](https://bitbucket.org/repo/GERMME/images/977083034-ifttt.png)

### How cheap will it be ?  ###

* The PI, case, SD card and power adapter will be around 70 dollars
* Each controller composed of arduino, case, bluetooth device, power adapter, sensors etc will be around 20-30 $ each
* The fingerprind module will make an exception and will cost around 70 dollars.
* A pair of speakers to play the sounds will be 20$

So if you implement all the features the total will be slightly under **300 $**

Note: The RC light switches, wall sockets, electric curtains, and electromagnetic door lock wore not included here.

### What can it do ? ###

* unlock a electromagnetic door through the press of a button on the app or through fingerprint
* control various types of electric curtains (open / close)
* control remote wall sockets (433 mhz versions by clonning their signal)
* toggle lights on / off (Livolo switches (check the product [here](https://www.aliexpress.com/item/Free-Shipping-Livolo-EU-Standard-Remote-Switch-White-Crystal-Glass-Panel-110-250V-Wall-Light-Remote/629004768.html?spm=2114.13010608.0.126.Mt7G6z)))
* toggle all lights off (single action)
* monitor temperature, humidity, light level, air quality, human presence 
* display charts with sensors data
* ability to activate an actuator(light, courtain etc) on a time schedule and based on sensors data and actuators state
* email notifications if the alarm is set and someone enters the house
* burgler mode (lights are randomly toggled on and off and voices are played)

### Project structure ###
* The python code for the raspberry pi is inside python_server folder
* Arduino sketches that communicate through bluetooth and do specfic tasks are located in arduino-sketches folder
* the Android App (webview + reporting location) is [here](https://bitbucket.org/danionescu/androidprojects/src/f9de4cec96bc4720326011c14c9a029436fe1488/HomeAutomation/?at=default), note that the password and username are hardcoded, needs some refactoring to get it from manifest

### Arduino sketches explained ###

**ACMotorCourtains**

* Description: controlls 12 V electric motors that powers electric courtains, the motors go up / down if the polarity is inversed
* Parts: case, 12 v 10A power supply, 5A fuse, arduino nano, L298 Dual H-Bridge Motor Driver, HC-05 bluetooth, l7805cv 5V regulator

**doorController**

* Description: controlls the 12V electromagnetic door lock (sends a current for a short time to unlock the door), also the device has a human presence sensors and report to the main unit 
* Parts: case, 12 V 2 A power supply, arduino nano, HC-05 bluetooth, l7805cv 5V regulator, passive IR presence sensor

**multiSensors** 

* Description: senses light level, air quality, temperature, humidity and reports to the main unit, also it receives commands about light siwtches states and sends the commands through the 433 MHZ Livolo standard
* Parts: case, 5V 1A power supply, arduino nano, HC-05 bluetooth, MQ135 air quality sensor, BH1750 lux sensor, HTU21D temp&humid sensor, 12 V battery holder & battery, 433 MHZ transmitter

**DCMotorCourtains**

* Description: controlls an AC window exterior courtain, the switching is done through relays and it involves switching phase through one of the two wires for either opening and closing the courtains, also it has a rain sensor which can be mounted on the interior or exterior. The sensor will report to the main unit, and the default behavior is close the courtain if the rain is detected
* Parts: case, 5V 1A power supply, arduino nano, HC-05 bluetooth, two relays, rain sensor

**fingerprintScanner**

* Description: will sit outside the apartment and scans the fingerprint, it will report the fingerprint found to the main unit which will eventually open the door
* Parts: 3V 0.5A power supply, arduino nano, HC-05 bluetooth, Fingerprint Scanner - TTL (GT-511C3), case

**weatherStation**

* Description: a mini weather station, low power runs only on batteries. It sends data using HC-12 comm module, the colleted data will be: humidity, temperature, pressure, light, rain
* Parts: arduino pro mini, HC-12 module, BME280 sensors, rain sensor, BH1750 lux sensor, 3x battery holder, battery, a NPN tranzistor, case, wires, PCB

### Limitations ###

* The current bluetooth communication method has a limitation to 7 connected devices, to overcome it a star topology must be implemented or multiple bluetooth dongles might be connected. The limitation can be overcome by using HC-12 long range modules
* Light switches and remote wall socket do not have built in security, the signal can be sniffed and clonned easily

### Further improvements ###
* integrate IOT  wifi devices
* A more easy to use IFTTT interface
* integrate air conditioning system
* water, power consumption sensors
* SMS notifications
* mailbox senzor with email notification
* user permissions, user management from inside the app