from time import sleep
from Crypto.Cipher import AES

import config
from MqttConnection import MqttConnection
from SerialAESDevice import SerialAESDevice
from Multisensor import Multisensor
from Serial import Serial


weather_station_mqtt_topic = 'ha/weather-station'

serial = Serial(config.serial['port'], config.serial['baud_rate'])
mqtt = MqttConnection(config.mqtt['host'])
multisensor = Multisensor(weather_station_mqtt_topic, mqtt)
serial_aes_device = SerialAESDevice(config.serial['aes_key'], serial, config.mqtt_serial_integration)

serial.add_callback(multisensor.process_sensor)
serial.connect()
mqtt.listen([('command/courtains', 0)], serial_aes_device.incomming_message)
mqtt.connect()


while True:
    serial.loop()
    mqtt.loop()
    sleep(0.05)