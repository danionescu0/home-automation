import json
from tornado.web import  authenticated
import time
from web.BaseHandler import BaseHandler

class ActuatorsHandler(BaseHandler):
    def initialize(self, dataContainer, jobControll):
        self.dataContainer = dataContainer
        self.jobControll = jobControll

    @authenticated
    def get(self, actuator, state):
        actuators = self.dataContainer.getActuators()
        if actuator in actuators and state in ['on', 'off']:
            state = (False, True)[state == 'on']
            self.jobControll.addJob(json.dumps({"job_name": "actuators", "actuator": actuator, "state" : state}))
            time.sleep(0.3)
        actuators = self.dataContainer.getActuators()

        self.render("../html/main.html", actuators = actuators, sensors = self.dataContainer.getSensors(), menuSelected="home")
