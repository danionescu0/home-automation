import redis
import calendar
import random
import json
from datetime import datetime

class abstractRedis:
    def __init__(self, config):
        self.client = redis.StrictRedis(**config)

    def addToList(self, key, data, timeAsTimestamp):
        if timeAsTimestamp == None:
            timeAsTimestamp = calendar.timegm(datetime.now().timetuple())
        data["randomize"] = random.randint(0, 999999999)
        self.client.zadd(key, timeAsTimestamp, json.dumps(data))