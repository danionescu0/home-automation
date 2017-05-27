import collections
import json
from typeguard import typechecked

from repository.AbstractRedis import AbstractRedis

class Actuators(AbstractRedis):
    REDIS_KEY = 'actuators'

    @typechecked()
    def __init__(self, redis_configuration: dict, actuators_config: dict):
        AbstractRedis.__init__(self, redis_configuration)
        self.keys = {self.REDIS_KEY: actuators_config}

    def get_actuators(self, just_names = False):
        if not just_names:
            actuators = self.get(self.REDIS_KEY)
            return collections.OrderedDict(sorted(actuators.items()))

        actuators = self.get(self.REDIS_KEY)
        actuator_names = [name for name, data in actuators.items()]

        return actuator_names

    @typechecked()
    def set_actuator(self, name: str, value) -> None:
        return self.__set(self.REDIS_KEY, name, value)

    def __set(self, key, name, value):
        data = self.get(key)
        data[name]['state'] = value
        self.client.set(key, json.dumps(data))