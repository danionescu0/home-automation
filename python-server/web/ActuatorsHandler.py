import json

from typeguard import typechecked

from web.CorsHandler import CorsHandler
from web.security.secure import secure
from web.formatter.ActuatorsFormatter import ActuatorsFormatter
from repository.ActuatorsRepository import ActuatorsRepository

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
            actuators = json.loads(data['actuators'])
            self.__actuators_repository.set_actuators(actuators)
            self.set_status(200)
        except Exception as e:
            print(e)
            self.set_status(500)