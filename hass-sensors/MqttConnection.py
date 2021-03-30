import time
from logging import RootLogger

import paho.mqtt.client as mqtt


class MqttConnection:
    PORT = 1883
    PRINT_HEARTBEAT = 20

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
        self.__client.connect(self.__host, self.PORT, 60)

    def loop(self):
        if int(time.time()) % MqttConnection.PRINT_HEARTBEAT == 0:
            self.__logger.info("Heartbeat: {0}".format(str(int(time.time()))))
        self.__client.loop()

    def send(self, channel: str, message: str):
        result = self.__client.publish(channel, message, qos=2, retain=True)
        self.__logger.info("Mqtt message published with result: {0}".format(result))

