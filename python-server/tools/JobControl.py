import redis
import json

class JobControll:
    CHANNEL_NAME = 'jobs'

    def __init__(self, configuration):
        self.client = redis.StrictRedis(**configuration)
        self.pubsub = self.client.pubsub()
        self.pubsub.subscribe(self.CHANNEL_NAME)

    def listen(self, callback):
        message = self.pubsub.get_message()
        if not message or message['type'] != 'message':
            return
        callback(message['data'])

    def __add_job(self, jobDescription):
        self.client.publish(self.CHANNEL_NAME, jobDescription)

    def change_actuator(self, name, state):
        self.__add_job(json.dumps({"job_name": "actuators", "actuator": name, "state": state}))
