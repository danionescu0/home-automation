import redis
import json

class JobControll:
    CHANNEL_NAME = 'jobs'

    def __init__(self, configuration):
        self.client = redis.StrictRedis(**configuration)
        self.pubsub = self.client.pubsub()
        self.pubsub.subscribe(self.CHANNEL_NAME)

    def listen(self, callback):
        while True:
            for job in self.pubsub.listen():
                if job["data"] == 1:
                    continue
                callback(job["data"])

    def __add_job(self, jobDescription):
        self.client.publish(self.CHANNEL_NAME, jobDescription)

    def change_actuator(self, name, value):
        self.__add_job(json.dumps({"job_name": "actuators", "actuator": name, "state": value}))
