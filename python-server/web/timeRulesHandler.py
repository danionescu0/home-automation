from web.baseHandler import baseHandler
from tornado.web import authenticated

class timeRulesHandler(baseHandler):
    def initialize(self, dataContainer):
        self.dataContainer = dataContainer

    @authenticated
    def get(self):
        actuatorsList = self.dataContainer.getActuators(True)

        self.render("../html/timeRules.html",
                    rules = self.dataContainer.getTimeRules(),
                    menuSelected="rules",
                    actuators = actuatorsList
                    )