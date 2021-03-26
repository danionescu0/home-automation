from typing import Callable
import codecs

import paho.mqtt.client as mqtt


class MqttConnection:
    PORT = 1883

    def __init__(self, host: str, user: str = None, password: str = None):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__callback = None
        self.__client = None
        self.__topics = []

    def connect(self):
        self.__client = mqtt.Client()
        def on_connect(client, userdata, flags, rc):
            self.__client.subscribe(self.__topics)

        def on_message(client, userdata, msg):
            if self.__callback is not None:
                self.__callback(msg.payload)

        self.__client.on_connect = on_connect
        self.__client.on_message = on_message
        if self.__user != None:
            self.__client.username_pw_set(self.__user, self.__password)
        self.__client.connect(self.__host, self.PORT, 60)

    def loop(self):
        self.__client.loop()

    def listen(self, topics: list, callback: Callable[[codecs.StreamReader], None]):
        self.__topics = topics
        self.__callback = callback

    def send(self, channel: str, message: str):
        self.__client.publish(topic=channel, payload=message, qos=1)