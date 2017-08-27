import json

from typeguard import typechecked

from repository.AbstractRepository import AbstractRepository


class IftttRules(AbstractRepository):
    TRIGGER_RULES = 'trigger-rules'
    ACTIVE = 'active'
    COMMANDS = 'commands'
    COMMAND_ACTUATOR_NAME = 'actuator_name'
    COMMAND_ACTUATOR_STATE = 'actuator_state'
    COMMAND_VOICE = 'voice'
    __REDIS_KEY = 'rules'

    @typechecked()
    def __init__(self, configuration: dict):
        AbstractRepository.__init__(self, configuration)
        self.keys = {self.__REDIS_KEY: {}}

    @typechecked()
    def upsert(self, name: str, trigger_rules: str, active: bool, commands: list):
        rules = self.get(self.__REDIS_KEY)
        rules[name] = {
            self.TRIGGER_RULES : trigger_rules,
            self.ACTIVE: active,
            self.COMMANDS: commands
        }

        return self.client.set(self.__REDIS_KEY, json.dumps(rules))

    @typechecked()
    def delete(self, name: str):
        rules = self.get(self.__REDIS_KEY)
        rules.pop(name, None)

        return self.client.set(self.__REDIS_KEY, json.dumps(rules))

    @typechecked()
    def get_all(self) -> dict:
        rules = self.get(self.__REDIS_KEY)
        if not rules:
            return {}

        return rules

    @typechecked()
    def get_all_active(self) -> dict:
        active = {}
        for key, rule in self.get_all().items():
            if rule[self.ACTIVE]:
                active[key] = rule

        return  active
