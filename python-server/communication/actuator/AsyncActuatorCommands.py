import json
from typing import Callable

import redis
from typeguard import typechecked


class AsyncActuatorCommands:
    __CHANNEL_NAME = 'jobs'

    @typechecked()
    def __init__(self, configuration: dict):
        self.__configuration = configuration

    def connect(self):
        self.client = redis.StrictRedis(**self.__configuration)
        self.pubsub = self.client.pubsub()
        self.pubsub.subscribe(self.__CHANNEL_NAME)

    @typechecked()
    def listen(self, callback: Callable[[str], None]) -> None:
        message = self.pubsub.get_message()
        if not message or message['type'] != 'message':
            return
        callback(json.loads(message['data'].decode('utf-8')))

    @typechecked()
    def change_actuator(self, name: str, value) -> None:
        self.__add_job(json.dumps({'actuator': name, 'value': value}))

    def __add_job(self, job_description):
        self.client.publish(self.__CHANNEL_NAME, job_description)