import json

from typeguard import typechecked

from web.CorsHandler import CorsHandler
from web.security.secure import secure
from web.formatter.ActuatorsFormatter import ActuatorsFormatter


class ApiActuatorsHandler(CorsHandler):
    @typechecked()
    def initialize(self, actuators_formatter: ActuatorsFormatter):
        self.__actuators_formatter = actuators_formatter

    @secure
    def get(self):
        self.write(json.dumps(self.__actuators_formatter.get_all()))