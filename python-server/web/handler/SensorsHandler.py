import json

from typeguard import typechecked

from repository.SensorsRepository import SensorsRepository
from web.formatter.SensorsFormatter import SensorsFormatter
from web.handler.CorsHandler import CorsHandler
from web.security.secure import secure


class SensorsHandler(CorsHandler):
    @typechecked()
    def initialize(self, sensors_formatter: SensorsFormatter, sensors_repository: SensorsRepository):
        self.__sensors_formatter = sensors_formatter
        self.__sensors_repository = sensors_repository

    @secure
    def get(self):
        self.write(json.dumps(self.__sensors_formatter.get_all()))

    @secure
    def post(self):
        raw_data = self.request.body.decode("utf-8").replace('\\n', '')
        data = json.loads(raw_data)
        try:
            components = json.loads(data['components'])
            self.__sensors_repository.set_sensors(components)
            self.set_status(200)
        except Exception as e:
            self.set_status(500)