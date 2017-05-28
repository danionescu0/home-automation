# Home automation project #

Yet another home automation project. The main concern of the project is keeping price down and maximizing customizability, 
it's a DIY project for makers and hacker and it's based on a raspberry pi (or another linux compatible board), arduino boards
IOT devices and other electronics.


**Summary**

* Feature list ?
* Project review
* IFTTT
* Screenshots
* Component prices
* Limitations
* Technical overwiew
* Further improvements



**Feature list ?**

* (IFTTT) ability to activate an actuator (light, courtain etc) on a time schedule and based on sensors data and actuators states
* unlock a electromagnetic door through the press of a button on the app or through *fingerprint*
* control various types of electric curtains (open / close)
* control remote wall sockets (433 mhz versions by clonning their signal), and WeMo siwtches
* use a speaker to emit alerts and statuses
* supports voice remote controll from the [android](https://github.com/danionescu0/android-home-automation-support) application
* toggle lights on / off (Livolo switches (check the product [here](https://www.aliexpress.com/item/Free-Shipping-Livolo-EU-Standard-Remote-Switch-White-Crystal-Glass-Panel-110-250V-Wall-Light-Remote/629004768.html?spm=2114.13010608.0.126.Mt7G6z)))
* multiple action switches (configurable and extendable) ex: "_toggle all lights off_"
* available environment sensors: temperature, humidity, light level, air quality, air pressure
* presence monitoring with infrared PIR sensors
* power monitoring for the whole house 
* the sensors modules can be installed in many rooms and outside (i also have a special weather sensor module)
* display charts with sensors data
* email notifications if the alarm is set and someone enters the house
* burgler mode (lights are randomly toggled on and off and voices are played)


**Project overview:**

* First the [python server](https://github.com/danionescu0/home-automation/tree/master/python-server) (project brain) located in python-server.
For more configuration of the server check the link.

* Second the [arduino sketches](https://github.com/danionescu0/home-automation/tree/master/arduino-sketches) located in arduino-sketches. 
The sketches are for custom devices that control various actuators and collect data from sensors.
Some sketches have skematics.

* Third and optional an android application located [here](https://github.com/danionescu0/android-home-automation-support). 
The application is a webview and besides that it sends from time to time your location the server, 
which can enable or disables various thisgs like the fingerprint scanner.

**IFTTT**

With this module complex rules can be added in the web-interface to be executed by actuators.

For example, if i want to open the courtains at 7:12 AM only if they are closed the following rule will do:
"_and  ( eq(A[livingCourtains], On), eq(TIME, 07:12))_"

Rules can be more complex than this, they can respond to sensors data, time and actuator states.

For example the following rule(fictive) will check if the actuator "livingCourtains" is off, and one of the following: 
the time is greater than 8:45 or temperature in living is between 21 and 22 degreeds
"_and  ( eq(A[livingCourtains], Off), or(gt(TIME, 08:45), btw(S[temperature:living], 21, 22) )_"


**Screenshots** 

 * The main menu which contains the sensors listings, and all the "switches" 
 
![home_automation_main.png](https://github.com/danionescu0/home-automation/blob/master/screenshots/home_automation_hp.png)

 * The sensors graphs menu 
 
![sensors.png](https://github.com/danionescu0/home-automation/blob/master/screenshots/home_automation_graphs.png)

 * If this than that 
 
![ifttt.png](https://github.com/danionescu0/home-automation/blob/master/screenshots/home_automation_ifttt.png)


**Component prices:**

* The PI, case, SD card and power adapter will be around 70 dollars
* Each controller composed of arduino, case, bluetooth device, power adapter, sensors etc will be around 20-30 $ each
* The fingerprind module will make an exception and will cost around 70 dollars.
* A Livolo ligt switch will be around 20$ on [here](https://www.aliexpress.com/premium/livolo-eu.html?ltype=wholesale&d=y&origin=y&isViewCP=y&catId=0&initiative_id=SB_20161208130911&SearchText=livolo+eu&blanktest=0)
* An electric strike lock starts from 23$ [here](http://www.ebay.com/sch/i.html?_odkw=electric+door+lock&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xelectric+strike+lock.TRS0&_nkw=electric+strike+lock&_sacat=0)
* A WeMo power socker is about 40$ [here](http://www.belkin.com/us/Products/home-automation/c/wemo-home-automation/) 
* An electric roller blade will start from 50$ [here](http://www.ebay.com/sch/i.html?_odkw=electric+courtains&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xelectric+roller+blinds.TRS0&_nkw=electric+roller+blinds&_sacat=0)


**Limitations:**

* The current bluetooth communication method has a limitation to 7 connected devices, 
so i've implemented a communication strategy in paralel using HC-12 serial module
* Light switches and remote wall socket do not have built in security, the signal can be clonned


**Technical overwiew**

This project uses the following technollogies, concepts and tools: 

python 3x with tornado web framework, arduino, redis, pubsub, raspberryPi, bluetooth, raspian (basic linux configuration),
 arduino IDE, electronics

To get started you'll need a background in programming, electronics and thinkering. For more technical configuration
please visit [python server](https://github.com/danionescu0/home-automation/tree/master/python-server), and 
[arduino sketches](https://github.com/danionescu0/home-automation/tree/master/arduino-sketches) folders.


**ToDo list:**

* integrate Z-wave devices
* integrate / build a music & voice player over http to sound alarms, play notifications etc
* more unit tests
* integrate air conditioning system
* integrate more IOT devices available on the market
* water consumption monitoring
* mailbox senzor with email notification
* user permissions, user management
* SMS notifications

