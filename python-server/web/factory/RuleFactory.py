from typing import List
import time

from typeguard import typechecked

from model.Rule import Rule
from model.Rule import RuleCommand


class RuleFactory:
    @typechecked()
    def from_request_data(self, data: dict) -> Rule:
        if 'name' not in data or 'text' not in data or 'active' not in data:
            raise Exception('Request data must contain id, name, text and active keys')
        if 'id' not in data:
            rule_id = str(time.time())
        else:
            rule_id = data['id']
        rule = Rule(rule_id, data['name'], data['text'], data['active'], data['lock_after_activation'])
        rule.add_commands(self.__get_rule_commands(data))

        return rule

    @typechecked()
    def __get_rule_commands(self, data: dict) -> List[RuleCommand]:
        commands = []
        email_text = None
        if 'email_text' in data:
            email_text = data['email_text']
        rule_command = RuleCommand(data['actuator_id'], data['actuator_state'], data['voice_text'], email_text)
        commands.append(rule_command)

        return commands