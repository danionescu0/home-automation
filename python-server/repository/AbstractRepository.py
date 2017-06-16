import redis
import calendar
import random
import json
from datetime import datetime
from typeguard import typechecked

class AbstractRepository:
    @typechecked()
    def __init__(self, configuration: dict):
        self.client = redis.StrictRedis(**configuration)

    @typechecked()
    def add_to_list(self, key: str, data):
        timestamp = calendar.timegm(datetime.now().timetuple())
        data["randomize"] = random.randint(0, 999999999)
        self.client.zadd(key, timestamp, json.dumps(data))

    @typechecked()
    def get(self, key: str):
        result = self.client.get(key)
        if (not result):
            return self.keys[key]

        return json.loads(result.decode("utf-8"))