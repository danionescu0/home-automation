# Home automation project #

This project will give you more control over your house and you'll going to have fun building it :)
It's strong points are easy integration of very custom hardware which you can build yourself and keep the price down and
integration with ready made devices like ZWave and WeMo.

Also a strong visual rule IFTTT (if this than that) interface that can trigger actuators and emit alerts. (see below)

It's a DIY project for makers and hackers and it's based on a raspberry pi (or another linux compatible board), arduino boards
IOT devices and other electronics.

Some youtube videos of how the project will look like:

Controlling led strips with zwave [here](https://youtu.be/AjYH_NEiPWc)

Automating electric shades [here](https://youtu.be/85ctap3Tpgk)

If you find this project useful in any way i will appreciate it if you give it a star. Thanks.

For those who want to donate something to my effort of developing free software, you can do so using this [ripple](https://ripple.com/) address: 
rNVMinyJysATxyMiFK1Tfnv5mCEk1RAvbT or using this [bitcoin](https://bitcoin.org/en/) address: 1B58XeAJQC3kxBW7DM4TwkoTggvbqTitKt



**Summary**

* Screenshots
* Feature list
* Project overview
* IFTTT (if this than that)
* Estimative component prices


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
* supports voice remote control from the [android](https://github.com/danionescu0/android-home-automation-support) application
* open / close lights
* monitor with different sensors: temperature, humidity, light level, air quality, PIR sensors, air pressure and more
* power consumption monitoring for the house
* display charts with sensors data
* email notifications if the alarm is set and someone enters the house
* burgler mode (lights are randomly toggled on and off and voices are played)


**Project overview:**
This project uses the following technologies, concepts and tools: 

python 3x with tornado web framework, reactJs, coreUI, arduino, redis, pubsub, raspberryPi, bluetooth, raspian (basic linux configuration),
 arduino IDE, electronics

To get started you'll need a background in programming, electronics and thinkering. 
* First the [python server](https://github.com/danionescu0/home-automation/tree/master/python-server) (project brain) located in python-server.
For more technical documentation check the links below.

* Second the [arduino sketches](https://github.com/danionescu0/home-automation/tree/master/arduino-sketches) located in arduino-sketches. 
The sketches are for custom devices that control various actuators and collect data from sensors.
Some sketches have skematics.

* The UI located [here](https://github.com/danionescu0/home-automation/tree/master/ui)

* The android application located [here](https://github.com/danionescu0/android-home-automation-support). 

* A text to speech server [here](https://github.com/danionescu0/home-automation/tree/master/remote-speaker)



**IFTTT**

With this module complex rules can be added in the web-interface to be executed by actuators or / and enable voice alerts.

Expressions:

* Equality: eq(a,b) -> true if a == b
* Greater than: gt(a,b) -> true if a > b
* Less than: lt(a,b) -> true if a < b
* Between: btw(x,a,b) => true if a <= x >= b
* OR: or(a,b) => true if a is true or b is true
* AND: and(a,b) => true if a is true and b is true
* Current time: TIME => returns current time
* Literal time: 14:25 => value of literal time
* True: True => literal true
* False: False => literal false
* Actuator: A(actuator_id) => value of the actuator who's id is actuator_id
* Sensor: A(sensor_id) => value of the sensor who's id is sensor_id
* Literal int: some_int_value => literal int value

Examples:

* The courtains are open and the time is 7:12:
````
and  ( eq(A[livingCourtains], On), eq(TIME, 07:12))
````

* Phone is home sensor is True and pollution sensor is greater than 55.
This can be used to emit a voice alert of the pollution danger.
````
and( eq(S[phoneIsHome], True), gt(S[airPollution_living], 55) )
````

Rules can be more complex than this, they can respond to sensors data, time and actuator states.

* The following rule(fictive) will check if the actuator "livingCourtains" is off, and either 
the time is greater than 8:45 or temperature in living is between 21 and 22 degreeds
````
and  ( eq(A[livingCourtains], False), or(gt(TIME, 08:45), btw(S[temperature:living], 21, 22) )

````

In the following example i'm mixing a block of text with sensors values to announce some sensor data. 
````
Wake up sir, the temperature outside is S[id_of_outside_temp_sensor] and humidity is S[id_of_outside_humid_sensor] 

````



**Estimative component prices:**

* The PI, case, SD card and power adapter will be around 70 dollars
* Custom made. 
Each custom made  controller composed of arduino, case, bluetooth device or HC-12 device, power adapter, sensors etc and will be around 20-30$

- The custom fingerprind sensor will cost around 70 dollars.

* A Livolo light switch will be around 20$ on [here](https://www.aliexpress.com/premium/livolo-eu.html?ltype=wholesale&d=y&origin=y&isViewCP=y&catId=0&initiative_id=SB_20161208130911&SearchText=livolo+eu&blanktest=0)
* An electric strike lock starts from 23$ [here](http://www.ebay.com/sch/i.html?_odkw=electric+door+lock&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xelectric+strike+lock.TRS0&_nkw=electric+strike+lock&_sacat=0)
* A WeMo power socker is about 40$ [here](http://www.belkin.com/us/Products/home-automation/c/wemo-home-automation/) 
* An electric roller blade will start from 50$ [here](http://www.ebay.com/sch/i.html?_odkw=electric+courtains&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xelectric+roller+blinds.TRS0&_nkw=electric+roller+blinds&_sacat=0)
* Some Zwave devices prices [here](http://z-wavelab.com/)
