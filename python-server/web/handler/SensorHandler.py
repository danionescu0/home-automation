import json
from datetime import datetime, timedelta

from typeguard import typechecked

from web.formatter.SensorsFormatter import SensorsFormatter
from repository.SensorsRepository import SensorsRepository
from web.handler.CorsHandler import CorsHandler
from web.security.secure import secure


class SensorHandler(CorsHandler):
    @typechecked()
    def initialize(self, sensors_formatter: SensorsFormatter, sensors_repository: SensorsRepository):
        self.__sensors_formatter = sensors_formatter
        self.__sensors_repository = sensors_repository

    @secure
    def get(self, id):
        nr_days_behind = 7
        start_date = datetime.today() - timedelta(days=nr_days_behind)
        end_date = datetime.today()
        output = {
            'name' : self.__sensors_repository.get_sensor(id).name,
            'data' : self.__sensors_formatter.get_sensor_values(id, start_date, end_date)
        }
        self.write(json.dumps(output))