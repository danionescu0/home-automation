import collections
import json

from repository.AbstractRedis import AbstractRedis

class Actuators(AbstractRedis):
    REDIS_KEY = 'actuators'

    def __init__(self, redis_configuration, actuators_config):
        AbstractRedis.__init__(self, redis_configuration)
        self.keys = {self.REDIS_KEY: actuators_config}

    def get_actuators(self, justNames = False):
        if not justNames:
            actuators = self.get(self.REDIS_KEY)
            return collections.OrderedDict(sorted(actuators.items()))

        actuators = self.get(self.REDIS_KEY)
        actuatorNames = []
        for name, data in actuators.iteritems():
            actuatorNames.append(name)

        return actuatorNames

    def set_actuator(self, name, value):
        return self.__set(self.REDIS_KEY, name, value)

    def __set(self, key, name, value):
        data = self.get(key)
        data[name]['state'] = value
        self.client.set(key, json.dumps(data))