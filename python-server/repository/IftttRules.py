import json

from repository.AbstractRedis import AbstractRedis

class IftttRules(AbstractRedis):
    DATA = 'data'
    STATE = 'state'
    ACTIVE = 'active'
    ACTUATOR = 'actuator'
    __REDIS_KEY = 'rules'

    def __init__(self, configuration):
        AbstractRedis.__init__(self, configuration)
        self.keys = {self.__REDIS_KEY: {}}

    def upsert(self, name, data, actuator, state, active):
        rules = self.get(self.__REDIS_KEY)
        rules[name] = {
            self.ACTUATOR : actuator,
            self.STATE : state,
            self.DATA : data,
            self.ACTIVE: active,
        }

        return self.client.set(self.__REDIS_KEY, json.dumps(rules))

    def delete(self, name):
        rules = self.get(self.__REDIS_KEY)
        rules.pop(name, None)

        return self.client.set(self.__REDIS_KEY, json.dumps(rules))

    def get_all(self):
        rules = self.get(self.__REDIS_KEY)
        if not rules:
            return {}

        return rules

    def get_all_active(self):
        active = {}
        for key, rule in self.get_all().iteritems():
            if rule[self.ACTIVE]:
                active[key] = rule

        return  active
