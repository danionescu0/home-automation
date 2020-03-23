import json
from time import sleep

import config
from MqttConnection import MqttConnection
from Serial import Serial


serial = Serial(config.serial['port'], config.serial['baud_rate'])
mqtt_connection = MqttConnection(config.mqtt['host'])

def incoming_serial(data):
    message_components = data[:-1].split(":")
    print(message_components)
    if message_components[0] not in config.weather_station_mappings:
        return
    message = json.dumps(
        {config.weather_station_mappings[message_components[0]]: float(message_components[1])}
    )
    print(message)
    mqtt_connection.send(MqttConnection.CHANNEL, message)

serial.add_callback(incoming_serial)
serial.connect()
mqtt_connection.connect()


while True:
    serial.loop()
    sleep(0.05)