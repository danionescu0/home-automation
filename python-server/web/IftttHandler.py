from typing import Dict

from typeguard import typechecked
from tornado.web import authenticated

from repository.IftttRulesRepository import IftttRulesRepository
from web.BaseHandler import BaseHandler
from repository.ActuatorsRepository import ActuatorsRepository
from ifttt.ExpressionValidator import ExpressionValidator
from model.Rule import Rule
from model.RuleCommand import RuleCommand


class IftttHandler(BaseHandler):
    @typechecked()
    def initialize(self, actuators_repo: ActuatorsRepository, rules_repository: IftttRulesRepository,
                   expression_validator: ExpressionValidator):

        self.__actuators_repo = actuators_repo
        self.__rules_repository = rules_repository
        self.__expression_validator = expression_validator

    @authenticated
    def get(self):
        actuator_list = [name for name, data in self.__actuators_repo.get_actuators().items()]
        rules = self.__rules_repository.get_all()
        rules['demo_rule'] = self.__get_demo_rule()

        self.render("./template/ifttt.html",
                    rules = self.__convert_to_view_data(rules),
                    selected_menu_item="rules",
                    actuators = actuator_list
                    )

    @authenticated
    def post(self, *args, **kwargs):
        rule_name = self.get_argument("rule_name", None, True)
        if self.get_argument("type", None, True) == 'delete':
            self.__rules_repository.delete(rule_name)

        trigger_rules = self.get_argument("trigger_rules", None, True)
        if (not self.__expression_validator.is_valid(trigger_rules)):
            self.write(self.__expression_validator.get_error(trigger_rules))
            self.set_status(406)
            return
        if (self.get_argument("type", None, True) == 'update'):
            self.__update_rules(rule_name, trigger_rules)

        self.set_status(200, 'OK')

    def __update_rules(self, rule_name, trigger_rules):
        actuator_name = self.get_argument("actuator_name", None, True)
        active = (False, True)[self.get_argument("active", None, True) == 'True']
        actuator_state = (False, True)[self.get_argument("actuator_state", None, 'On') == 'On']
        voice = self.get_argument("voice", "", True)
        commands = [{
            IftttRulesRepository.COMMAND_ACTUATOR_NAME : actuator_name,
            IftttRulesRepository.COMMAND_ACTUATOR_STATE : actuator_state,
            IftttRulesRepository.COMMAND_VOICE : voice
        }]
        self.__rules_repository.upsert(rule_name, trigger_rules, active, commands)

    def __get_demo_rule(self):
        rule = Rule('demo_rule',
                    'and  ( eq(A[homeAlarm], False), or(gt(TIME, 08:45), btw(S[temperature:living], 21, 22) )',
                    True)
        rule.add_command(RuleCommand('powerSocket1', True, 'Demo voice'))

        return rule

    def __convert_to_view_data(self, rules: Dict[str, Rule]) -> list:
        view_data = []
        for name, rule in rules.items():
            view_data.append({
                'name' : rule.name,
                'text' : rule.text,
                'active' : rule.active,
                'actuator_name': rule.rule_commands[0].actuator_name,
                'actuator_state': rule.rule_commands[0].actuator_state,
                'voice_text': rule.rule_commands[0].voice_text
            })

        return view_data