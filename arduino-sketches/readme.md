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
* Parts: arduino pro mini, HC-12 module, BME280 sensors, rain sensor, BH1750 lux sensor, 3x battery holder, battery, a NPN tranzistor, case, wires, PCB, a solar pannel, diode