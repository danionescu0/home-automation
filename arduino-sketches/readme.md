### Arduino sketches explained ###

Note: The bluetooth HC-05 device can be replace with any other serial wireless
communication device lice HC-12 with greater range

**WeatherStation**

Description: A low power weather station capable of running completly off grid. It can
collect data about pressure, humidity, temperature, rain and light


External libraries:

[BH1750](https://github.com/claws/BH1750)
[LowPower](https://github.com/rocketscream/Low-Power)
[Adafruit Sensor](https://github.com/adafruit/Adafruit_Sensor)
[Adafruit BME280](https://github.com/adafruit/Adafruit_BME280_Library)
![sketch.png](https://raw.githubusercontent.com/danionescu0/home-automation/master/arduino-sketches/weatherStation/sketch_bb.png)


Parts: 
- arduino pro mini 
- HC-12 module
- BME280 temperature/humidty/pressure sensor
- analog rain sensor 
- BH1750 lux sensor (light)
- 3x AAA battery holder
- a NPN tranzistor and resistor a resistor
- case, wires, glue 
- a 6 V solar pannel, diode

Tips:

- the solar pannel sits outside the case, and it powers the inside circuits through a small hole in the case.

The pannel is attached to the case with glue
 
- the pannel is conencted through the batteries through a small diode to prevent reverse current

- the arduino pro mini must have the small LED removed or one of it's wires cut to prevent battery discharge

- the whole circuitry in idle mode will consume < 50 microamps

How does it work:

The aruino is put into deep sleep mode and one every 10 minutes it does the following:
- it wakes up
- power the peripherials and sensors througn a NPN transistor
- send the data through serial HC-12 
- power off the peripherals and sensors
- puts it's self back to sleep


**ACMotorCourtains**

Description: controlls an AC window exterior courtain, the switching is done through relays and it involves switching phase through one of the two wires for either opening 
and closing the courtains, also it has a rain sensor which can be mounted on the interior or exterior. 

Parts: 
- case
- 5V 2A power supply
- arduino nano
- HC-05 bluetooth
- two relays 

**DoorController**

Description: controlls the 12V electromagnetic door lock (sends a current for a short time to unlock the door), 
also the device senses humain presence, and measures electricity consumption 

Parts
- case
- 12 V 2 A power supply
- arduino nano
- HC-05
- l7805cv 5V regulator
- passive IR presence sensor,
- 10 uF capacitor
- 2 x 470kOhm rezistor
- 33 Ohm rezistor
- 100A SCT-013-000 current senzor

Tips
-  merging the door lock and the sensors togeather was done because the
odds are the main door sits next to the main power supply cable

**MultiSensors** 

Description: sends sensors data, and commands Livolo switches

Parts: 
- case
- 5V 1A power supply
- arduino nano
- HC-12 serial device
- BME680 air quality / humidity / temperature / pressure sensor
- BH1750 lux sensor 
- 5v to 12v regulator
- 433 MHZ transmitter

* External libraries:
[BME680](https://github.com/adafruit/Adafruit_BME680.git)
[Adafruit](https://github.com/adafruit/Adafruit_Sensor.git)
[BH1750](https://github.com/claws/BH1750)
[AESLib](https://github.com/DavyLandman/AESLib)
Livolo will be inside arduino-sketches folder

**DCMotorCourtains**
Check [this](http://www.instructables.com/id/Automated-Windows-Shades/) instructable for more information

Description: controlls 12 V electric motors that powers electric courtains, the motors go up / down if the polarity is inversed

Parts: 

- plastic case
- 12 v 10A power supply
- 5A fuse
- arduino nano
- 2 x 5 v relays
- HC-12
- l7805cv 5V regulator
- Tip142T NPN tranzistor
- a 1 k resitor
- small diode
- 2 x 5.5mm DC Power Plug Jack Socket male and female
![sketch.png](https://raw.githubusercontent.com/danionescu0/home-automation/master/arduino-sketches/DCMotorCourtains/sketch.png)

**FingerprintScanner**

Description: will sit outside the apartment and scans the fingerprint, it will report the fingerprint found to the main unit which will eventually open the door

Parts

- case
- 3V 0.5A power supply
- arduino nano
- HC-05 bluetooth
- Fingerprint Scanner - TTL (GT-511C3)
* External libraries:
[FPS_GT511C3](https://github.com/sparkfun/Fingerprint_Scanner-TTL)
