import json
from typing import Dict

from typeguard import typechecked

from repository.AbstractRepository import AbstractRepository
from model.Rule import Rule
from model.RuleCommand import RuleCommand


class IftttRulesRepository(AbstractRepository):
    __REDIS_KEY = 'rules'

    @typechecked()
    def __init__(self, configuration: dict):
        AbstractRepository.__init__(self, configuration)
        self.keys = {self.__REDIS_KEY: {}}

    @typechecked()
    def upsert(self, rule: Rule):
        rules = self.get(self.__REDIS_KEY)
        rules[rule.id] = {
            'id' : rule.id,
            'name' : rule.name,
            'text' : rule.text,
            'active': rule.active,
            'rule_commands': [
                {'actuator_id' : command.actuator_id,
                 'actuator_state': command.actuator_state,
                 'voice_text': command.voice_text}
                for command in rule.rule_commands]
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
            commands = [RuleCommand(data['actuator_id'], data['actuator_state'], data['voice_text'])
                        for data in rule_data['rule_commands']]
            rule = Rule(rule_data['id'], rule_data['name'], rule_data['text'], rule_data['active'])
            rule.add_commands(commands)
            rules[id] = rule

        return rules