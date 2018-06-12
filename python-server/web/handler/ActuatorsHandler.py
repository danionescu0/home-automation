import json

from typeguard import typechecked

from repository.ActuatorsRepository import ActuatorsRepository
from web.formatter.ActuatorsFormatter import ActuatorsFormatter
from web.handler.CorsHandler import CorsHandler
from web.security.secure import secure


class ActuatorsHandler(CorsHandler):
    @typechecked()
    def initialize(self, actuators_formatter: ActuatorsFormatter, actuators_repository: ActuatorsRepository):
        self.__actuators_formatter = actuators_formatter
        self.__actuators_repository = actuators_repository

    @secure
    def get(self):
        self.write(json.dumps(self.__actuators_formatter.get_all()))

    @secure
    def post(self):
        raw_data = self.request.body.decode("utf-8").replace('\\n', '')
        data = json.loads(raw_data)
        try:
            components = json.loads(data['components'])
            self.__actuators_repository.set_actuators(components)
            self.set_status(200)
        except Exception as e:
            self.set_status(500)