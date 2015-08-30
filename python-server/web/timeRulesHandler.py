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

        self.render("../html/timeRules.html",
                    rules = self.dataContainer.getTimeRules(),
                    menuSelected="rules",
                    actuators = actuatorsList
                    )

    @authenticated
    def post(self, *args, **kwargs):
        actuatorsList = self.dataContainer.getActuators(True)
        ruleName = self.get_argument("rule", None, True)
        actuatorName = self.get_argument("actuator", None, True)
        active = (False, True)[self.get_argument("active", None, True) == 'True']
        actuatorState = (False, True)[self.get_argument("state", None, True) == 'True']
        time = datetime.datetime.strptime(self.get_argument("time", None, True), '%H:%M:%S').time()
        if (self.get_argument("type", None, True) == 'update'):
            self.dataContainer.upsertTimeRule(ruleName, actuatorName, actuatorState, time, active)

        self.render("../html/timeRules.html",
                    rules = self.dataContainer.getTimeRules(),
                    menuSelected="rules",
                    actuators = actuatorsList
                    )