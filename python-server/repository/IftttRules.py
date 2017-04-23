import json

from repository.AbstractRedis import AbstractRedis

class IftttRules(AbstractRedis):
    TRIGGER_RULES = 'trigger-rules'
    ACTIVE = 'active'
    COMMANDS = 'commands'
    COMMAND_ACTUATOR_NAME = 'actuator_name'
    COMMAND_ACTUATOR_STATE = 'actuator_state'
    COMMAND_VOICE = 'voice'
    __REDIS_KEY = 'rules'

    def __init__(self, configuration):
        AbstractRedis.__init__(self, configuration)
        self.keys = {self.__REDIS_KEY: {}}

    def upsert(self, name, trigger_rules, active, commands):
        rules = self.get(self.__REDIS_KEY)
        rules[name] = {
            self.TRIGGER_RULES : trigger_rules,
            self.ACTIVE: active,
            self.COMMANDS: commands
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
        for key, rule in self.get_all().items():
            if rule[self.ACTIVE]:
                active[key] = rule

        return  active
