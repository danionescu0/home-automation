import redis
import json
from typeguard import typechecked
from typing import Callable


class AsyncJobs:
    CHANNEL_NAME = 'jobs'

    @typechecked()
    def __init__(self, configuration: dict):
        self.__configuration = configuration

    def connect(self):
        self.client = redis.StrictRedis(**self.__configuration)
        self.pubsub = self.client.pubsub()
        self.pubsub.subscribe(self.CHANNEL_NAME)

    @typechecked()
    def listen(self, callback: Callable[[str], None]) -> None:
        message = self.pubsub.get_message()
        if not message or message['type'] != 'message':
            return
        callback(message['data'].decode('utf-8'))

    def __add_job(self, job_description):
        self.client.publish(self.CHANNEL_NAME, job_description)

    @typechecked()
    def change_actuator(self, name: str, state: bool) -> None:
        self.__add_job(json.dumps({"job_name": "actuators", "actuator": name, "state": state}))