import json

from typeguard import typechecked

from communication.actuator.AsyncActuatorCommands import AsyncActuatorCommands
from web.handler.CorsHandler import CorsHandler
from web.security.secure import secure


class ActuatorHandler(CorsHandler):
    @typechecked()
    def initialize(self, async_actuator_commands: AsyncActuatorCommands):
        self.__async_actuator_commands = async_actuator_commands

    @secure
    def post(self, id):
        data = json.loads(self.request.body.decode("utf-8"))
        self.__async_actuator_commands.change_actuator(id, data['value'])
        self.set_status(200)