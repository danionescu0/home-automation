from tornado.web import authenticated
from typeguard import typechecked

from communication.actuator.AsyncActuatorCommands import AsyncActuatorCommands
from repository.ActuatorsRepository import ActuatorsRepository
from repository.SensorsRepository import SensorsRepository
from web.BaseHandler import BaseHandler


class MainHandler(BaseHandler):
    @typechecked()
    def initialize(self, async_actuator_commands: AsyncActuatorCommands, actuators_repo: ActuatorsRepository,
                   sensors_repo: SensorsRepository):
        self.__async_actuator_commands = async_actuator_commands
        self.__actuators_repo = actuators_repo
        self.__sensors_repo = sensors_repo

    @authenticated
    def get(self):
        self.render(
            "./template/main.html",
            actuators = self.__group_actuators(),
            sensors = self.__sensors_repo.get_sensors(),
            selected_menu_item="home"
        )

    @authenticated
    def post(self, *args, **kwargs):
        actuator_name = self.get_argument("actuator_name", None, True)
        actuator_value = self.get_argument("actuator_value", None, True)
        self.__async_actuator_commands.change_actuator(actuator_name, {'false' : False, 'true': True}[actuator_value])

    def __group_actuators(self):
        actuators = self.__actuators_repo.get_actuators()
        grouped_actuators = {}
        for id, actuator in actuators.items():
            group_key = actuator.room
            if not group_key in grouped_actuators:
                grouped_actuators[group_key] = []
            actuator_data = actuators[id]
            grouped_actuators[group_key].append(actuator_data)

        return grouped_actuators