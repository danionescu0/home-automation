from web.BaseHandler import BaseHandler
from tornado.web import authenticated
import datetime

class TimeRulesHandler(BaseHandler):
    def initialize(self, data_container, logging):
        self.data_container = data_container
        self.logging = logging

    @authenticated
    def get(self):
        actuatorsList = self.data_container.get_actuators(True)
        theRules = self.data_container.get_time_rules()
        theRules['test'] =\
            {
                "active" : True, "actuator": "livingLight",
                "state"  : True, "stringTime": "12:00:00",
                "template": True
            }

        self.render("../html/timeRules.html",
                    rules = theRules,
                    menuSelected="rules",
                    actuators = actuatorsList
                    )

    @authenticated
    def post(self, *args, **kwargs):
        ruleName = self.get_argument("rule", None, True)
        if (self.get_argument("type", None, True) == 'delete'):
            self.data_container.delete_time_rule(ruleName)

        actuatorName = self.get_argument("actuator", None, True)
        active = (False, True)[self.get_argument("active", None, True) == 'True']
        actuatorState = (False, True)[self.get_argument("state", None, True) == 'True']
        time = datetime.datetime.strptime(self.get_argument("time", None, True), '%H:%M:%S').time()
        if (self.get_argument("type", None, True) == 'update'):
            self.data_container.upsert_time_rule(ruleName, actuatorName, actuatorState, time, active)

        self.set_status(200, 'OK')