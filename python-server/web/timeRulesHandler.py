from web.baseHandler import baseHandler
from tornado.web import authenticated
import datetime

class timeRulesHandler(baseHandler):
    def initialize(self, dataContainer, logging):
        self.dataContainer = dataContainer
        self.logging = logging

    @authenticated
    def get(self):
        actuatorsList = self.dataContainer.getActuators(True)
        theRules = self.dataContainer.getTimeRules()
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
            self.dataContainer.deleteTimeRule(ruleName)

        actuatorName = self.get_argument("actuator", None, True)
        active = (False, True)[self.get_argument("active", None, True) == 'True']
        actuatorState = (False, True)[self.get_argument("state", None, True) == 'True']
        time = datetime.datetime.strptime(self.get_argument("time", None, True), '%H:%M:%S').time()
        if (self.get_argument("type", None, True) == 'update'):
            self.dataContainer.upsertTimeRule(ruleName, actuatorName, actuatorState, time, active)

        self.set_status(200, 'OK')