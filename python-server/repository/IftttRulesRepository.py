import json
from typing import Dict

from typeguard import typechecked

from repository.AbstractRepository import AbstractRepository
from model.Rule import Rule
from model.RuleCommand import RuleCommand


class IftttRulesRepository(AbstractRepository):
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
    def upsert(self, id: str, trigger_rules: str, active: bool, commands: list):
        rules = self.get(self.__REDIS_KEY)
        rules[id] = {
            self.TRIGGER_RULES : trigger_rules,
            self.ACTIVE: active,
            self.COMMANDS: commands
        }

        return self.client.set(self.__REDIS_KEY, json.dumps(rules))

    @typechecked()
    def delete(self, id: str):
        rules = self.get(self.__REDIS_KEY)
        rules.pop(id, None)

        return self.client.set(self.__REDIS_KEY, json.dumps(rules))

    def get_all(self) -> Dict[str, Rule]:
        rules_data = self.get(self.__REDIS_KEY)
        if not rules_data:
            return {}
        rules = {}
        for id, rule_data in rules_data.items():
            commands = [RuleCommand(data['actuator_name'], data['actuator_state'], data['voice'])
                        for data in rule_data['commands']]
            rule = Rule(id, id, rule_data['trigger-rules'], rule_data['active'])
            rule.add_commands(commands)
            rules[id] = rule

        return rules