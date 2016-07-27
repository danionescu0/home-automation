import json
from tornado.web import  authenticated
import time
from web.BaseHandler import BaseHandler

class ActuatorsHandler(BaseHandler):
    def initialize(self, data_container, job_controll):
        self.data_container = data_container
        self.job_controll = job_controll

    @authenticated
    def get(self, actuator, state):
        actuators = self.data_container.get_actuators()
        if actuator in actuators and state in ['on', 'off']:
            state = (False, True)[state == 'on']
            self.job_controll.add_job(json.dumps({"job_name": "actuators", "actuator": actuator, "state" : state}))
            time.sleep(0.3)
        actuators = self.data_container.get_actuators()

        self.render("../html/main.html", actuators = actuators, sensors = self.data_container.get_sensors(), menuSelected="home")
