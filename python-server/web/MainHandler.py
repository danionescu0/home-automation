from tornado.web import authenticated
from typeguard import typechecked

from web.BaseHandler import BaseHandler
from tools.AsyncJobs import AsyncJobs
from repository.ActuatorsRepository import ActuatorsRepository
from repository.SensorsRepository import SensorsRepository


class MainHandler(BaseHandler):
    @typechecked()
    def initialize(self, job_controll: AsyncJobs, actuators_repo: ActuatorsRepository, sensors_repo: SensorsRepository):
        self.job_controll = job_controll
        self.__actuators_repo = actuators_repo
        self.__sensors_repo = sensors_repo

    @authenticated
    def get(self):
        actuators = self.__actuators_repo.get_actuators()
        self.render(
            "./template/main.html",
            actuators = self.__group_actuators(actuators, 'room'),
            sensors = self.__sensors_repo.get_sensors(),
            selected_menu_item="home"
        )

    @authenticated
    def post(self, *args, **kwargs):
        actuator_name = self.get_argument("actuator_name", None, True)
        actuator_value = self.get_argument("actuator_value", None, True)
        self.job_controll.change_actuator(actuator_name, {'false' : False, 'true': True}[actuator_value])

    def __group_actuators(self, actuators, by):
        grouped_actuators = {}
        for actuator_name, actuator_properties in actuators.items():
            group_key = actuator_properties[by]
            if not group_key in grouped_actuators:
                grouped_actuators[group_key] = []
            actuator_data = actuators[actuator_name]
            actuator_data['name'] = actuator_name
            grouped_actuators[group_key].append(actuator_data)

        return grouped_actuators