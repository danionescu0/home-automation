from datetime import datetime
from dateutil import tz

from typeguard import typechecked

from tools.DateUtils import DateUtils
from repository.SensorsRepository import SensorsRepository


class SensorsFormatter:
    def __init__(self, sensors_repository: SensorsRepository) -> None:
        self.__sensors_repository = sensors_repository

    @typechecked()
    def get_sensor_values(self, id: str, start_date: datetime, end_date: datetime) -> list:
        sensor_data_points = self.__sensors_repository.get_sensor_values(id, start_date, end_date)
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(DateUtils.get_timezone())
        formatted = []
        for datapoint in sensor_data_points:
            initial_date = datetime.fromtimestamp(int(datapoint.timestamp)).replace(tzinfo=from_zone)
            local_date = initial_date.astimezone(to_zone)
            datetime_text = local_date.strftime('%m-%d %H:%M')
            formatted.append({'date' : datetime_text, 'value': datapoint.value})

        return formatted