This is the integration between https://www.home-assistant.io/ platform and custom sensors and automations through MQTT

1. Integration is between a serial device and Home Asistant. 

The serial device in our case is the HC-10 serial adapter, on the other end we have a arduino that's publishing events through the air
using another HC-10 adapter: https://github.com/danionescu0/home-automation/tree/master/arduino-sketches/weatherStation

Our python scripts listens and decodes the serial comunication, and publish the sensor data through a MQTT topic.

On the other side home asistant listens to the topic and updates sensors data in the UI, you can check more about this here: https://www.home-assistant.io/integrations/mqtt/

2. A serial actuator (DC motor courtains) using AES encription and this sketch: https://github.com/danionescu0/home-automation/tree/master/arduino-sketches/DCMotorCourtains

MQTT switch: https://www.home-assistant.io/integrations/switch.mqtt/

Instalation:

- install Mosquitto server: https://mosquitto.org/
- install python3 
- install requirements.txt

````
pip3 install -r requirements.txt
````

Configure:

In config.py change:

- serial port if your HC-10 is on a different port
- the MQTT server IP


Start:

````
python3 server.py /dev/ttyACM0
````