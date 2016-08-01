from web.BaseHandler import BaseHandler
from tornado.web import authenticated
import datetime

class TimeRulesHandler(BaseHandler):
    def initialize(self, data_container, time_rules, logging):
        self.data_container = data_container
        self.time_rules = time_rules
        self.logging = logging

    @authenticated
    def get(self):
        actuator_list = self.data_container.get_actuators(True)
        all_rules = self.time_rules.get_all()
        all_rules['test'] =\
            {
                "active" : True, "actuator": "livingLight",
                "state"  : True, "stringTime": "12:00:00",
                "template": True
            }

        self.render("../html/timeRules.html",
                    rules = all_rules,
                    selected_menu_item="rules",
                    actuators = actuator_list
                    )

    @authenticated
    def post(self, *args, **kwargs):
        ruleName = self.get_argument("rule", None, True)
        if (self.get_argument("type", None, True) == 'delete'):
            self.time_rules.delete(ruleName)

        actuatorName = self.get_argument("actuator", None, True)
        active = (False, True)[self.get_argument("active", None, True) == 'True']
        actuatorState = (False, True)[self.get_argument("state", None, True) == 'True']
        time = datetime.datetime.strptime(self.get_argument("time", None, True), '%H:%M:%S').time()
        if (self.get_argument("type", None, True) == 'update'):
            self.time_rules.upsert(ruleName, actuatorName, actuatorState, time, active)

        self.set_status(200, 'OK')