import redis
import calendar
import random
import json
from datetime import datetime

class AbstractRedis:
    def __init__(self, configuration):
        self.client = redis.StrictRedis(**configuration)

    def add_to_list(self, key, data, timeAsTimestamp):
        if timeAsTimestamp == None:
            timeAsTimestamp = calendar.timegm(datetime.now().timetuple())
        data["randomize"] = random.randint(0, 999999999)
        self.client.zadd(key, timeAsTimestamp, json.dumps(data))