import codecs
from typing import Callable
from logging import RootLogger

import paho.mqtt.client as mqtt


class MqttConnection:
    PORT = 1883

    def __init__(self, host: str, logger: RootLogger, user: str = None, password: str = None):
        self.__host = host
        self.__logger = logger
        self.__user = user
        self.__password = password
        self.__callback = None
        self.__client = None
        self.__topics = []

    def connect(self):
        self.__client = mqtt.Client("weather-station-client")
        print(self.__client.connect(self.__host, self.PORT, 60))

    def loop(self):
        self.__client.loop()

    def send(self, channel: str, message: str):
        result = self.__client.publish(channel, message, qos=2)
        self.__logger.info("Mqtt message published with result: {0}".format(result))

