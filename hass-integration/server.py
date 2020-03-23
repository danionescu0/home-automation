from time import sleep

import config
from MqttConnection import MqttConnection
from Multisensor import Multisensor
from Serial import Serial


mqtt_topic = 'ha/weather-station'
serial = Serial(config.serial['port'], config.serial['baud_rate'])
mqtt = MqttConnection(config.mqtt['host'])
multisensor = Multisensor(mqtt_topic, mqtt)
weather_station_data = {}

serial.add_callback(multisensor.process_sensor)
serial.connect()
mqtt.connect()

while True:
    serial.loop()
    mqtt.loop()
    sleep(0.05)