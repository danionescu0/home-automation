from typeguard import typechecked

from repository.IftttRulesRepository import IftttRulesRepository


class IftttFormatter:
    @typechecked()
    def __init__(self, rules_repository: IftttRulesRepository) -> None:
        self.__rules_repository = rules_repository

    @typechecked()
    def get_all(self) -> list:
        rules = self.__rules_repository.get_all()
        formatted = []
        for id, rule in rules.items():
            rule_command = rule.rule_commands[0]
            formatted_rule = {
                'id' : rule.id,
                'name': rule.name,
                'text': rule.text,
                'active' : rule.active,
                'actuator_id': rule_command.actuator_id,
                'actuator_state': rule_command.actuator_state,
                'voice_text': rule_command.voice_text,
                'email_text': rule_command.email_text
            }
            formatted.append(formatted_rule)

        return formatted