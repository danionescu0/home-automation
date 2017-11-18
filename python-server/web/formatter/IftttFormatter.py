from repository.IftttRulesRepository import IftttRulesRepository


class IftttFormatter:
    def __init__(self, rules_repository: IftttRulesRepository) -> None:
        self.__rules_repository = rules_repository

    def get_all(self) -> list:
        rules = self.__rules_repository.get_all()
        formatted = []
        for id, rule in rules.items():
            formatted_rule = {
                'id' : rule.id,
                'name': rule.name,
                'text': rule.text,
                'active' : rule.active,
                'rule_commands': self.__format_commands(rule.rule_commands)
            }
            formatted.append(formatted_rule)

        return formatted

    def __format_commands(self, rule_commands):
        return [
            {
                'actuator_name': command.actuator_name,
                'actuator_state': command.actuator_state,
                'voice_text': command.voice_text,
             }
            for command in rule_commands]