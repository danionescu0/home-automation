import calendar
import json
import math
from collections import Counter
from datetime import datetime
from typing import List

from typeguard import typechecked

from repository.AbstractRepository import AbstractRepository
from model.Sensor import Sensor


class SensorsRepository(AbstractRepository):
    REDIS_SENSORS_KEY = 'sensors'
    REDIS_SENSORS_HISTORY_KEY = 'sensors_history_{0}'
    SENSORS_UPDATE_INTERVAL_IN_HISTORY = 300

    @typechecked()
    def __init__(self, redis_configuration: dict, sensors_configuration: list):
        AbstractRepository.__init__(self, redis_configuration)
        self.keys = {self.REDIS_SENSORS_KEY: sensors_configuration}
        self.last_averages = {}
        self.sensors_last_updated = {}
        self.current_timestamp = 0

    @typechecked()
    def get_sensors2(self) -> list:
        return self.get(self.REDIS_SENSORS_KEY)

    @typechecked()
    def get_sensors(self) -> List[Sensor]:
        sensors_data = self.get(self.REDIS_SENSORS_KEY)
        sensors = []
        for sensor_data in sensors_data:
            sensor = Sensor(sensor_data['type'], sensor_data['location'], sensor_data['value'])
            sensor.communication_code = sensor_data['communication_code']
            sensor.visible = sensor_data['visible']
            sensor.last_updated = sensor_data['last_updated']
            sensors.append(sensor)

        return sensors

    @typechecked()
    def set_sensor(self, sensor: Sensor) -> None:
        self.current_timestamp = calendar.timegm(datetime.now().timetuple())
        self.__set(sensor)
        self.__add_last_sensor_averages_in_history(sensor)

    def __set(self, sensor: Sensor):
        sensors = self.get(self.REDIS_SENSORS_KEY)
        for redis_sensor in sensors:
            if redis_sensor['type'] == sensor.type and redis_sensor['location'] == sensor.location:
                redis_sensor['value'] = sensor.value
                redis_sensor['last_updated'] = self.current_timestamp

        self.client.set(self.REDIS_SENSORS_KEY, json.dumps(sensors))

    def __add_last_sensor_averages_in_history(self, sensor: Sensor):
        name = self.__get_sensor_key(sensor.type, sensor.location)
        if name not in list(self.last_averages.keys()):
            self.last_averages[name] = []
        self.last_averages[name].append(sensor.value)
        if name not in self.sensors_last_updated:
            self.sensors_last_updated[name] = 0
        if (self.current_timestamp - self.sensors_last_updated[name] < self.SENSORS_UPDATE_INTERVAL_IN_HISTORY):
            return

        self.sensors_last_updated[name] = self.current_timestamp
        sensor_average_value = int(math.ceil(float(sum(self.last_averages[name])) / len(self.last_averages[name])))
        self.add_to_list(self.__get_sensor_key(sensor.type, sensor.location), {'value': sensor_average_value})
        self.last_averages[name] = []

    @typechecked()
    def get_sensor_values_in_interval(self, type: str, location: str, start_date: datetime, end_date: datetime) -> list:
        start_timestamp = calendar.timegm(start_date.timetuple())
        end_timestamp = calendar.timegm(end_date.timetuple())
        range = self.client.zrangebyscore(self.__get_sensor_key(type, location), start_timestamp, end_timestamp, withscores=True)
        for index, element in enumerate(range):
            timestamp = range[index][1]
            range[index] = json.loads(range[index][0].decode("utf-8"))
            range[index]['timestamp'] = timestamp

        return range

    def get_hourly_sensor_values_in_interval(self, type, location, start_date, end_date):
        range = self.get_sensor_values_in_interval(type, location, start_date, end_date)
        last_hour = datetime.fromtimestamp(int(range[0]['timestamp'])).hour
        counter = 0
        average_date = range[0]
        grouped_range = []
        for datapoint in range:
            extracted_hour = datetime.fromtimestamp(int(datapoint['timestamp'])).hour
            counter += 1
            if extracted_hour != last_hour:
                last_hour = extracted_hour
                average_date.update((x, y / counter) for x, y in list(average_date.items()))
                grouped_range.append(average_date)
                counter = 0
            else:
                average_date = dict(Counter(average_date) + Counter(datapoint))

        return grouped_range

    def __get_sensor_key(self, type, location):
        return self.REDIS_SENSORS_HISTORY_KEY.format(self.__get_sensor_name(type, location))

    def __get_sensor_name(self, type, location):
        return '{0}_{1}'.format(type, location)