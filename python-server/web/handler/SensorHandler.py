import json
from datetime import datetime, timedelta

from typeguard import typechecked

from web.formatter.SensorsFormatter import SensorsFormatter
from repository.SensorsRepository import SensorsRepository
from model.SensorProperties import SensorProperties
from web.handler.CorsHandler import CorsHandler
from web.security.secure import secure


class SensorHandler(CorsHandler):
    __ACCEPTED_DATE_FORMAT = '%m-%d-%Y'
    __DEFAULT_DAYS_BEHIND = 7

    @typechecked()
    def initialize(self, sensors_formatter: SensorsFormatter, sensors_repository: SensorsRepository):
        self.__sensors_formatter = sensors_formatter
        self.__sensors_repository = sensors_repository

    @secure
    def get(self, id):
        date_interval = self.__get_date_interval()
        print(date_interval)
        output = {
            'name': self.__sensors_repository.get_sensor(id).properties.get(SensorProperties.NAME),
            'data': self.__sensors_formatter.get_sensor_values(id, date_interval[0], date_interval[1])
        }
        self.write(json.dumps(output))

    def __get_date_interval(self):
        try:
            start_date = datetime.strptime(self.get_argument('start_date', None, True), self.__ACCEPTED_DATE_FORMAT)
            end_date = datetime.strptime(self.get_argument('end_date', None, True), self.__ACCEPTED_DATE_FORMAT)
            end_date = end_date.replace(hour=23, minute=59, second=59)
            return start_date, end_date
        except TypeError as e:
            start_date = datetime.today() - timedelta(days=self.__DEFAULT_DAYS_BEHIND)
            end_date = datetime.today()
            return start_date, end_date
