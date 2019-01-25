import re
from typing import List

from model.Sensor import Sensor
from model.SensorTypes import SensorTypes


class SensorBuilder:
    SENSOR_TYPE_MAPPING = {
        'T': SensorTypes.TEMPERATURE.value,
        'H': SensorTypes.HUMIDITY.value,
        'PS': SensorTypes.PRESSURE.value,
        'L': SensorTypes.LIGHT.value,
        'R': SensorTypes.RAIN.value
    }

    SENSOR_REGEX = '([A-Z]{1,2})(\d{1,2})?\:([\d\-\.]{1,4})'
    SENSOR_SEPARATOR = '|'
    SENSOR_TYPE_SKIP = 'V'

    def __init__(self) -> None:
        self.__text_buffer = ''

    def is_complete(self) -> bool:
        return self.__text_buffer.endswith(self.SENSOR_SEPARATOR)

    def add_text(self, text: str):
        self.__text_buffer += text

    def build(self) -> List[Sensor]:
        text_buffer = self.__text_buffer[:-1]
        sensors = []
        for sensor_data in text_buffer.split('|'):
            sensor_components = re.findall(self.SENSOR_REGEX, sensor_data)
            if not sensor_components:
                raise RuntimeError('Cannot parse string:{0}'.format(sensor_data))
            sensor = self.__get_sensor(sensor_components[0])
            if sensor is not None:
                sensors.append(sensor)
        self.__text_buffer = ''

        return sensors

    def __get_sensor(self, sensor_components: list) -> Sensor:
        code, location, value = sensor_components
        if code not in self.SENSOR_TYPE_MAPPING:
            raise RuntimeError('Code with {0} not mapped with any sensor'.format(code))
        if code == self.SENSOR_TYPE_SKIP:
            return None
        try:
            return Sensor(self.SENSOR_TYPE_MAPPING[code], float(value))
        except ValueError as e:
            raise RuntimeError(
                'Badly formatted sensor value: {0}, error: {1})'.format(value, e.message))