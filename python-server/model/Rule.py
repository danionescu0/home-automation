from typing import List

from model.RuleCommand import RuleCommand


class Rule:
    def __init__(self, id: str, name: str, text: str, active: bool) -> None:
        self.id = id
        self.name = name
        self.text = text
        self.active = active
        self._rule_commands = []

    def add_command(self, command: RuleCommand):
        self._rule_commands.append(command)

    def add_commands(self, commands: List[RuleCommand]):
        self._rule_commands.extend(commands)

    @property
    def rule_commands(self) -> List[RuleCommand]:
        return self._rule_commands

    def __repr__(self) -> str:
        commands = [str(command) + ',' for command in self._rule_commands]

        return 'Rule[ id({4}), name({0}), text({1}), active({2}), commands:({3}) ]'\
            .format(self.name, self.text, self.active, commands, self.id)