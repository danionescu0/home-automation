from web.BaseHandler import BaseHandler
from tornado.web import authenticated

class IftttHandler(BaseHandler):
    def initialize(self, actuators_repo, ifttt_rules, ifttt_expression_validator, logging):
        self.__actuators_repo = actuators_repo
        self.__ifttt_rules = ifttt_rules
        self.__ifttt_expression_validator = ifttt_expression_validator
        self.__logging = logging

    @authenticated
    def get(self):
        actuator_list = self.__actuators_repo.get_actuators(True)
        all_rules = self.__ifttt_rules.get_all()
        all_rules['test'] =\
            {
                "active" : True,
                "actuator": "livingLight",
                "state"  : True,
                "data" : "and  ( eq(A[homeAlarm], False), or(lt(TIME, 20:45), btw(S[temperature], 21, 24) )",
                "template": True
            }

        self.render("./template/ifttt.html",
                    rules = all_rules,
                    selected_menu_item="rules",
                    actuators = actuator_list
                    )

    @authenticated
    def post(self, *args, **kwargs):
        rule_name = self.get_argument("rule", None, True)
        if (self.get_argument("type", None, True) == 'delete'):
            self.__ifttt_rules.delete(rule_name)

        actuator_name = self.get_argument("actuator", None, True)
        rule_data = self.get_argument("data", None, True)
        active = (False, True)[self.get_argument("active", None, True) == 'True']
        actuator_state = (False, True)[self.get_argument("state", None, True) == 'True']
        if (not self.__ifttt_expression_validator.is_valid(rule_data)):
            self.write(self.__ifttt_expression_validator.get_error(rule_data))
            self.set_status(406)
            return
        if (self.get_argument("type", None, True) == 'update'):
            self.__ifttt_rules.upsert(rule_name, rule_data, actuator_name, actuator_state, active)

        self.set_status(200, 'OK')
