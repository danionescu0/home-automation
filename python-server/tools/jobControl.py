import redis

class JobControll:
    CHANNEL_NAME = 'jobs'

    def __init__(self, config):
        self.client = redis.StrictRedis(**config)
        self.pubsub = self.client.pubsub()
        self.pubsub.subscribe(self.CHANNEL_NAME)

    def listen(self):
        return self.pubsub.listen()

    def addJob(self, jobDescription):
        self.client.publish(self.CHANNEL_NAME, jobDescription)