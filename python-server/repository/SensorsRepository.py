import calendar
import json
import math
from datetime import datetime
from typing import List
from typing import Optional

from typeguard import typechecked

from repository.AbstractRepository import AbstractRepository
from model.Sensor import Sensor
from model.SensorDataPoint import SensorDataPoint


class SensorsRepository(AbstractRepository):
    __REDIS_SENSORS_KEY = 'sensors'
    __REDIS_SENSORS_HISTORY_KEY = 'sensors_history_{0}'
    __SENSORS_UPDATE_INTERVAL_IN_HISTORY = 300

    @typechecked()
    def __init__(self, redis_configuration: dict):
        AbstractRepository.__init__(self, redis_configuration)
        self.keys = {self.__REDIS_SENSORS_KEY: {}}
        self.last_averages = {}
        self.sensors_last_updated = {}
        self.current_timestamp = 0

    @typechecked()
    def get_sensors(self) -> List[Sensor]:
        sensors_data = self.get(self.__REDIS_SENSORS_KEY)
        sensors = []
        for sensor_data in sensors_data:
            sensor = Sensor(sensor_data['id'], sensor_data['type'], sensor_data['location'], sensor_data['value'])
            if 'name' in sensor_data:
                sensor.name = sensor_data['name']
            if 'communication_code' in sensor_data:
                sensor.communication_code = sensor_data['communication_code']
            else:
                sensor.communication_code = (False, False)
            if 'last_updated' in sensor_data:
                sensor.last_updated = sensor_data['last_updated']
            else:
                sensor.last_updated = 0
            sensors.append(sensor)

        return sensors

    @typechecked()
    def get_sensor(self, id: str) -> Optional[Sensor]:
        sensors = self.get_sensors()
        sensor = [sensor for sensor in sensors if sensor.id == id]
        if len(sensor) == 1:
            return sensor[0]

        return None

    @typechecked()
    def set_sensor(self, sensor: Sensor) -> None:
        self.current_timestamp = calendar.timegm(datetime.now().timetuple())
        self.__set(sensor)
        self.__add_last_sensor_averages_in_history(sensor)

    @typechecked()
    def set_sensors(self, sensors: list):
        self.client.set(self.__REDIS_SENSORS_KEY, json.dumps(sensors))

    @typechecked()
    def get_sensor_values(self, id: str, start_date: datetime, end_date: datetime) -> List[SensorDataPoint]:
        redis_key = self.__REDIS_SENSORS_HISTORY_KEY.format(id)
        start_timestamp = calendar.timegm(start_date.timetuple())
        end_timestamp = calendar.timegm(end_date.timetuple())
        range = self.client.zrangebyscore(redis_key, start_timestamp, end_timestamp, withscores=True)

        return [SensorDataPoint(json.loads(datapoint[0].decode("utf-8"))['value'], datapoint[1]) for datapoint in range]

    def __set(self, sensor: Sensor):
        sensors = self.get(self.__REDIS_SENSORS_KEY)
        for redis_sensor in sensors:
            if redis_sensor['id'] == sensor.id:
                redis_sensor['value'] = sensor.value
                redis_sensor['last_updated'] = self.current_timestamp

        self.client.set(self.__REDIS_SENSORS_KEY, json.dumps(sensors))

    def __add_last_sensor_averages_in_history(self, sensor: Sensor):
        name = self.__get_sensor_key(sensor.id)
        if name not in list(self.last_averages.keys()):
            self.last_averages[name] = []
        self.last_averages[name].append(sensor.value)
        if name not in self.sensors_last_updated:
            self.sensors_last_updated[name] = 0
        if (self.current_timestamp - self.sensors_last_updated[name] < self.__SENSORS_UPDATE_INTERVAL_IN_HISTORY):
            return

        self.sensors_last_updated[name] = self.current_timestamp
        sensor_average_value = int(math.ceil(float(sum(self.last_averages[name])) / len(self.last_averages[name])))
        self.add_to_list(self.__get_sensor_key(sensor.id), {'value': sensor_average_value})
        self.last_averages[name] = []

    def __get_sensor_key(self, id: str) -> str:
        return self.__REDIS_SENSORS_HISTORY_KEY.format(id)