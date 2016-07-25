# Home automation project #

Yet another home automation project. The main concern of the project is keeping price down, it's a DIY project for makers and hackers:) it is based on a raspberry pi (or another linux compatible board) and arduinos.

### How cheap it will be  ###

* The PI, case, SD card and power adapter will be around 70 dollars
* Each controller composed of arduino, case, bluetooth device, power adapter, sensors etc will be around 20-30 $ each
* The fingerprind module will make an exception and will cost around 70 dollars.
* A pair of speakers to play the sounds will be 20$

So if you implement all the features the total will be slightly under **300 $**

Note: The RC light switches, wall sockets, electric curtains, and electromagnetic door lock wore not included here.

### What can it do ###

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


### Arduino sketches explained ###

1.  windowSwitchController
* Description: controlls 12 V electric motors that powers electric courtains, the motors go up / down if the polarity is inversed
* parts: case, 12 v 10A power supply, 5A fuse, arduino nano, L298 Dual H-Bridge Motor Driver, HC-05 bluetooth, l7805cv 5V regulator

2. 