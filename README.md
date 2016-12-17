# Home automation project #

Yet another home automation project. The main concern of the project is keeping price down and maximizing customizability, it's a DIY project for makers and hackers
it is based on a raspberry pi (or another linux compatible board) and arduino boards.

# Summary
* [First what can it do ?](#first-what-can-it-do)
* [Project review](#project-review)
* [IFTTT](#ifttt)
* [Screenshots](#screenshots)
* [Components prices](#components-prices)
* [Limitations](#limitations)
* [First what can it do ?](#further-improvements)



###First what can it do ? 

* unlock a electromagnetic door through the press of a button on the app or through fingerprint
* control various types of electric curtains (open / close)
* control remote wall sockets (433 mhz versions by clonning their signal), and WeMo siwtches
* use a speaker to emit alerts and statuses
* supports voice remote controll from the [android](https://bitbucket.org/danionescu/androidhomeautomation) application
* toggle lights on / off (Livolo switches (check the product [here](https://www.aliexpress.com/item/Free-Shipping-Livolo-EU-Standard-Remote-Switch-White-Crystal-Glass-Panel-110-250V-Wall-Light-Remote/629004768.html?spm=2114.13010608.0.126.Mt7G6z)))
* multiple action switches ex: toggle all lights off
* monitor temperature, humidity, light level, air quality, human presence inside and outside
* display charts with sensors data
* (IFTTT) ability to activate an actuator(light, courtain etc) on a time schedule and based on sensors data and actuators state
* email notifications if the alarm is set and someone enters the house
* burgler mode (lights are randomly toggled on and off and voices are played)

###Project review:

* First the [python server](https://bitbucket.org/danionescu/home-automation/src/a36e18c64b764421f40b6aa6b0157a047b61e5a4/python-server/?at=default) (project brain) located in python-server

* Second the [arduino sketches](https://bitbucket.org/danionescu/home-automation/src/a36e18c64b764421f40b6aa6b0157a047b61e5a4/arduino-sketches/?at=default) located in arduino-sketches. The sketches are for custom devices that control various actuators and collect data from sensors.

* Third and optional an android application located [here](https://bitbucket.org/danionescu/androidhomeautomation). The application is a webview and besides that it sends from time to time your location the server, which can enable or disables various thisgs like the fingerprint scanner

##IFTTT
This is a work in progress

##Screenshots 

### The main menu which contains the sensors listings, and all the "switches" ###
![home_automation_main.png](https://bitbucket.org/repo/GERMME/images/2704480034-home_automation_main.png)

### The sensors graphs menu 
![sensors.png](https://bitbucket.org/repo/GERMME/images/3652208713-sensors.png)

### If this than that 
![ifttt.png](https://bitbucket.org/repo/GERMME/images/977083034-ifttt.png)

###Components prices 

* The PI, case, SD card and power adapter will be around 70 dollars
* Each controller composed of arduino, case, bluetooth device, power adapter, sensors etc will be around 20-30 $ each
* The fingerprind module will make an exception and will cost around 70 dollars.
* A pair of speakers to play the sounds will be 20$

So if you implement all the features the total will be slightly under **300 $**

* A Livolo ligt switch will be around 20$ on [here](https://www.aliexpress.com/premium/livolo-eu.html?ltype=wholesale&d=y&origin=y&isViewCP=y&catId=0&initiative_id=SB_20161208130911&SearchText=livolo+eu&blanktest=0)
* An electric strike lock starts from 23$ [here](http://www.ebay.com/sch/i.html?_odkw=electric+door+lock&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xelectric+strike+lock.TRS0&_nkw=electric+strike+lock&_sacat=0)
* A WeMo power socker is about 40$ [here](http://www.belkin.com/us/Products/home-automation/c/wemo-home-automation/) 
* An electric roller blade will start from 50$ [here](http://www.ebay.com/sch/i.html?_odkw=electric+courtains&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.Xelectric+roller+blinds.TRS0&_nkw=electric+roller+blinds&_sacat=0)

###Limitations

* The current bluetooth communication method has a limitation to 7 connected devices, the limitation can be overcome by using HC-12 long range modules
* Light switches and remote wall socket do not have built in security, the signal can be sniffed and clonned easily

###Further improvements

* integrate more IOT devices
* integrate air conditioning system
* water, power consumption sensors
* SMS notifications
* mailbox senzor with email notification
* user permissions, user management from inside the app