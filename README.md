# Home automation project #

This project will give you more controll over your house and you'll going to have fun building it.
It's strong points are easy integration of very custom hardware which you can build yourself and keep the price down and
Integration with ready made devices like ZWave and WeMo.

Also a strong programming IFTTT interface that can trigger actuators and emit alerts. (see below)

It's a DIY project for makers and hacker and it's based on a raspberry pi (or another linux compatible board), arduino boards
IOT devices and other electronics.


**Summary**

* Screenshots
* Feature list
* Project overview
* IFTTT
* Component prices
* Technical overwiew


**Screenshots** 

 * The rooms page
 
![home_automation_main.png](https://github.com/danionescu0/home-automation/blob/master/screenshots/onepageapp/rooms.png)

 * Sensors graphs 
 
![sensors.png](https://github.com/danionescu0/home-automation/blob/master/screenshots/onepageapp/graphs.png)

 * Rules 
 
![ifttt.png](https://github.com/danionescu0/home-automation/blob/master/screenshots/onepageapp/rules.png)

 * Login 
 
![ifttt.png](https://github.com/danionescu0/home-automation/blob/master/screenshots/onepageapp/login.png)

 * Configuration 
 
![ifttt.png](https://github.com/danionescu0/home-automation/blob/master/screenshots/onepageapp/configuration.png)



**Feature list**

* Supports customizable rules from the UI. For example let's say you want in the morning to open the courtains, and 
if your're home to hear what's the weather outside. Or maybe if the air quality dropped and somebody is home open an
electric fan to get fresh air from outside
* Supports custom hardware (over bluetooth or serial) and commercial hardware: WeMo devices, Zwave devices
* New devices can be added by extending the code
* unlock a electromagnetic door through the press of a button on the app or through *fingerprint*
* open / closes various types of electric curtains 
* control remote wall sockets 
* use a speaker to emit voice alerts
* supports voice remote controll from the [android](https://github.com/danionescu0/android-home-automation-support) application
* open / close lights
* monitor with different sensors: temperature, humidity, light level, air quality, PIR sensors, air pressure and more
* power consumption monitoring for the house
* display charts with sensors data
* email notifications if the alarm is set and someone enters the house
* burgler mode (lights are randomly toggled on and off and voices are played)


**Project overview:**

* First the [python server](https://github.com/danionescu0/home-automation/tree/master/python-server) (project brain) located in python-server.
For more configuration of the server check the link.

* Second the [arduino sketches](https://github.com/danionescu0/home-automation/tree/master/arduino-sketches) located in arduino-sketches. 
The sketches are for custom devices that control various actuators and collect data from sensors.
Some sketches have skematics.

* The UI located [here](https://github.com/danionescu0/home-automation/tree/master/ui)

* The android application located [here](https://github.com/danionescu0/android-home-automation-support). 

* A text to speech server [here](https://github.com/danionescu0/home-automation/tree/master/remote-speaker)



**IFTTT**

With this module complex rules can be added in the web-interface to be executed by actuators or / and enable voice alerts.

For example, if i want to open the courtains at 7:12 AM only if they are closed the following rule will do:
"_and  ( eq(A[livingCourtains], On), eq(TIME, 07:12))_"

Rules can be more complex than this, they can respond to sensors data, time and actuator states.

For example the following rule(fictive) will check if the actuator "livingCourtains" is off, and one of the following: 
the time is greater than 8:45 or temperature in living is between 21 and 22 degreeds
"_and  ( eq(A[livingCourtains], Off), or(gt(TIME, 08:45), btw(S[temperature:living], 21, 22) )_"

Voice alerts are text to speech blocks of text, beside that actuator and sensors values cand be mixer or the current time,
for example : "Wake up sir, the temperature outside is S[temperature:outside] and humidity is S[humidity:outside]" this
block of text will announce the temperature and humidity outside



**Component prices:**

* The PI, case, SD card and power adapter will be around 70 dollars
* Custom made. 
Each custom made  controller composed of arduino, case, bluetooth device or HC-12 device, power adapter, sensors etc and will be around 20-30$

- The custom fingerprind sensor will cost around 70 dollars.

* A Livolo light switch will be around 20$ on [here](https://www.aliexpress.com/premium/livolo-eu.html?ltype=wholesale&d=y&origin=y&isViewCP=y&catId=0&initiative_id=SB_20161208130911&SearchText=livolo+eu&blanktest=0)
* An electric strike lock starts from 23$ [here](http://www.ebay.com/sch/i.html?_odkw=electric+door+lock&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xelectric+strike+lock.TRS0&_nkw=electric+strike+lock&_sacat=0)
* A WeMo power socker is about 40$ [here](http://www.belkin.com/us/Products/home-automation/c/wemo-home-automation/) 
* An electric roller blade will start from 50$ [here](http://www.ebay.com/sch/i.html?_odkw=electric+courtains&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xelectric+roller+blinds.TRS0&_nkw=electric+roller+blinds&_sacat=0)
* Some Zwave devices prices [here](http://z-wavelab.com/)

**Technical overwiew**

This project uses the following technollogies, concepts and tools: 

python 3x with tornado web framework, reactJs, coreUI, arduino, redis, pubsub, raspberryPi, bluetooth, raspian (basic linux configuration),
 arduino IDE, electronics

To get started you'll need a background in programming, electronics and thinkering. 

For more technical configuration please visit:
[New onepageapp User Interface](https://github.com/danionescu0/home-automation/tree/master/ui) 
[Python server](https://github.com/danionescu0/home-automation/tree/master/python-server)
[Arduino sketches](https://github.com/danionescu0/home-automation/tree/master/arduino-sketches)
[Remote speaker](https://github.com/danionescu0/home-automation/tree/master/remote-speaker)

