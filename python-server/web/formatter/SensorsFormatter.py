from datetime import datetime

from typeguard import typechecked

from repository.SensorsRepository import SensorsRepository


class SensorsFormatter:
    def __init__(self, sensors_repository: SensorsRepository) -> None:
        self.__sensors_repository = sensors_repository

    @typechecked()
    def get_sensor_values(self, id: str, start_date: datetime, end_date: datetime) -> list:
        sensor_data_points = self.__sensors_repository.get_sensor_values(id, start_date, end_date)

        return [{'date' : data_point.timestamp, 'value': data_point.value} for data_point in sensor_data_points]