import redis
import calendar
import random
import json
from datetime import datetime

class AbstractRedis:
    def __init__(self, configuration):
        self.client = redis.StrictRedis(**configuration)

    def add_to_list(self, key, data, timestamp):
        if timestamp == None:
            timestamp = calendar.timegm(datetime.now().timetuple())
        data["randomize"] = random.randint(0, 999999999)
        self.client.zadd(key, timestamp, json.dumps(data))

    def get(self, key):
        result = self.client.get(key)
        if (not result):
            return self.keys[key]

        return json.loads(result)