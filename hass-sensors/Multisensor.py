import config

from MqttConnection import MqttConnection


class Multisensor:
    def __init__(self, mqtt_connection: MqttConnection) -> None:
        self.__sensors = {}
        self.__mqtt_connection = mqtt_connection

    def process_sensor(self, data):
        message_components = data[:-1].split(":")
        if message_components[0] not in config.weather_station_mappings:
            print("{0} not regonized, skipping".format(message_components[0]))
            return
        self.__sensors[message_components[0]] = int(message_components[1])
        if len(self.__sensors) == len(config.weather_station_mappings):
            for sensor_id, sensor_value in self.__sensors.items():
                sensor_data = config.weather_station_mappings[sensor_id]
                self.__mqtt_connection.send(sensor_data['state_topic'], sensor_value)
            self.__sensors = {}

    def init_discovery(self):
        for sensor_it, sensor_data in config.weather_station_mappings.items():
            print(sensor_data["discovery_topic"], sensor_data["discovery_message"])
            self.__mqtt_connection.send(sensor_data["discovery_topic"], sensor_data["discovery_message"])
