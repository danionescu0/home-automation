import json
from datetime import datetime, timedelta
from typeguard import typechecked

from web.CorsHandler import CorsHandler
from web.security.secure import secure
from web.formatter.SensorsFormatter import SensorsFormatter


class ApiSensorHandler(CorsHandler):
    @typechecked()
    def initialize(self, sensors_formatter: SensorsFormatter):
        self.__sensors_formatter = sensors_formatter

    @secure
    def get(self, id):
        nr_days_behind = 1
        start_date = datetime.today() - timedelta(days=nr_days_behind)
        end_date = datetime.today()
        self.write(json.dumps(self.__sensors_formatter.get_sensor_values(id, start_date, end_date)))