import re
from typeguard import typechecked

from communication.SensorsParseException import SensorsParseException

class TextSensorDataParser:
    SENSOR_REGEX = '([A-Z]{1,2})(\d{1,2})?\:([\d\-\.]{1,4})'

    @typechecked()
    def __init__(self, sensors_conf: list):
        self.__sensors_conf = sensors_conf
        self.__sensor_separator = '|'

    @typechecked()
    def is_buffer_parsable(self, buffer: str) -> bool:
        return buffer.endswith(self.__sensor_separator)

    @typechecked()
    def parse(self, text_buffer: str) -> list:
        text_buffer = text_buffer[:-1]
        sensors = []
        for sensor in text_buffer.split('|'):
            sensor_components = re.findall(self.SENSOR_REGEX, sensor)
            if not sensor_components:
                raise SensorsParseException('Cannot parse string:{0}'.format(sensor))
            sensors.append(self.__get_sensor(sensor_components[0]))

        return sensors

    def __get_sensor(self, sensor_components):
        code = sensor_components[0]
        if sensor_components[1] == '':
            location = False
        else:
            location = sensor_components[1]
        value = sensor_components[2]
        for sensor in self.__sensors_conf:
            if sensor['communication_code'][0] == code and sensor['communication_code'][1] == location:
                found_sensor = sensor
                try:
                    found_sensor['value'] = int(value)
                except ValueError as e:
                    raise SensorsParseException(
                        'Badly formatted sensor value: {0}, error: {1})'.format(value, e.message))
                return found_sensor

        raise SensorsParseException('Sensor with code: {0} and location {1} not found!'.format(code, location))