import json
import config

from MqttConnection import MqttConnection


class Multisensor:
    def __init__(self, mqtt_topic: str, mqtt_connection: MqttConnection) -> None:
        self.__sensors = {}
        self.__mqtt_topic = mqtt_topic
        self.__mqtt_connection = mqtt_connection

    def process_sensor(self, data):
        message_components = data[:-1].split(":")
        if message_components[0] not in config.weather_station_mappings:
            return
        self.__sensors[config.weather_station_mappings[message_components[0]]] = int(message_components[1])
        if len(self.__sensors) == len(config.weather_station_mappings):
            message = json.dumps(self.__sensors)
            self.__mqtt_connection.send(self.__mqtt_topic, message)
            self.__sensors = {}