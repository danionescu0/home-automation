from logging import RootLogger

from typeguard import typechecked
from tornado.web import authenticated

from repository.IftttRules import IftttRules
from web.BaseHandler import BaseHandler
from repository.Actuators import Actuators
from ifttt.ExpressionValidator import ExpressionValidator


class IftttHandler(BaseHandler):
    @typechecked()
    def initialize(self, actuators_repo: Actuators, ifttt_rules: IftttRules,
                   ifttt_expression_validator: ExpressionValidator, logging: RootLogger):

        self.__actuators_repo = actuators_repo
        self.__ifttt_rules = ifttt_rules
        self.__ifttt_expression_validator = ifttt_expression_validator
        self.__logging = logging

    @authenticated
    def get(self):
        actuator_list = [name for name, data in self.__actuators_repo.get_actuators().items()]
        all_rules = self.__ifttt_rules.get_all()
        all_rules['test_rule'] =\
            {
                "active" : True,
                "rule_name": "raiseTemperature",
                "trigger-rules": "and  ( eq(A[homeAlarm], False), or(gt(TIME, 08:45), btw(S[temperature:living], 21, 22) )",
                "commands" : [
                    {
                        "actuator_name" : "powerSocket1",
                        "actuator_state" : True,
                        "voice": "Temperature raised"
                    }],
                "template": True
            }

        self.render("./template/ifttt.html",
                    rules = all_rules,
                    selected_menu_item="rules",
                    actuators = actuator_list
                    )

    @authenticated
    def post(self, *args, **kwargs):
        rule_name = self.get_argument("rule_name", None, True)
        if self.get_argument("type", None, True) == 'delete':
            print(rule_name)
            self.__ifttt_rules.delete(rule_name)

        trigger_rules = self.get_argument("trigger_rules", None, True)
        if (not self.__ifttt_expression_validator.is_valid(trigger_rules)):
            self.write(self.__ifttt_expression_validator.get_error(trigger_rules))
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
            IftttRules.COMMAND_ACTUATOR_NAME : actuator_name,
            IftttRules.COMMAND_ACTUATOR_STATE : actuator_state,
            IftttRules.COMMAND_VOICE : voice
        }]
        self.__ifttt_rules.upsert(rule_name, trigger_rules, active, commands)