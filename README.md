# Home automation project #

Yet another home automation project. The main concern of the project is keeping price down, it's a DIY project for makers and hackers:) it is based on a raspberry pi (or another linux compatible board) and arduinos.

Don't judge by python code too harsh, i am noobie in python but i'm improving, the project will suffer refactors periodically and hopefully it will become more pythonian.

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
* control remote wall sockets
* monitor temperature, humidity, light level, air quality, human presence 
* display charts with sensors data
* ability to activate a switch, light etc on a time schedule
* email notifications if the alarm is set and someone enters the house
* burgler mode (lights are randomly toggled on and off and voices are played)
* Toggle lights on / off
* toggle all lights off button
* ability to react to sensors output (you can easily write a piece of code to react to sensors data)

### Project structure ###
* The python code for the raspberry pi is inside home_automation folder
* The rest of the folders contain arduino sketches that communicate through bluetooth and do specfic tasks
* the Android App (webview + reporting location) is [here](https://bitbucket.org/danionescu/androidprojects/src/f9de4cec96bc4720326011c14c9a029436fe1488/HomeAutomation/?at=default), note that the password and username are hardcoded, needs some refactoring to get it from manifest

### Arduino sketches explained ###

**livingWindowCourtains**

* Description: controlls 12 V electric motors that powers electric courtains, the motors go up / down if the polarity is inversed
* Parts: case, 12 v 10A power supply, 5A fuse, arduino nano, L298 Dual H-Bridge Motor Driver, HC-05 bluetooth, l7805cv 5V regulator

**doorController**

* Description: controlls the 12V electromagnetic door lock (sends a current for a short time to unlock the door), also the device has a human presence sensors and report to the main unit 
* Parts: case, 12 V 2 A power supply, arduino nano, HC-05 bluetooth, l7805cv 5V regulator, passive IR presence sensor

**livingSensors** 

* Description: senses light level, air quality, temperature, humidity and reports to the main unit, also it receives commands about light siwtches states and sends the commands through the 433 MHZ Livolo standard
* Parts: case, 5V 1A power supply, arduino nano, HC-05 bluetooth, MQ135 air quality sensor, BH1750 lux sensor, HTU21D temp&humid sensor, 12 V battery holder & battery, 433 MHZ transmitter

**windowSwitchController**

* Description: controlls an AC window exterior courtain, the switching is done through relays and it involves switching phase through one of the two wires for either opening and closing the courtains, also it has a rain sensor which can be mounted on the interior or exterior. The sensor will report to the main unit, and the default behavior is close the courtain if the rain is detected
* Parts: case, 5V 1A power supply, arduino nano, HC-05 bluetooth, two relays, rain sensor

**fingerprintScanner**

* Description: will sit outside the apartment and scans the fingerprint, it will report the fingerprint found to the main unit which will eventually open the door
* Parts: 3V 0.5A power supply, arduino nano, HC-05 bluetooth, Fingerprint Scanner - TTL (GT-511C3)
* Note. It's still a bit of a work in progress

### Limitations ###

* The current bluetooth communication method has a limitation to 7 connected devices, to overcome it a star topology must be implemented
* Light switches and remote wall socket do not have built in security, the signal can be sniffed and clonned easily

### Further improvements ###
* IFTTT mini system
* add the possibility to connect serial devices
* finish the fingerprint scanner system (with door opening)
* integrate air conditioning system
* water, power consumption sensors
* mailbox senzor with email notification