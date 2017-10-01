from ifttt.parser.TokenConverter import TokenConverter
from ifttt.parser.Token import Token
from ifttt.parser.ParseException import ParseException
from repository.SensorsRepository import SensorsRepository


class SensorTokenConverter(TokenConverter):
    def __init__(self, sensors_repository: SensorsRepository) -> None:
        self.__sensors_repository = sensors_repository

    def get_value(self, token_raw_value: str):
        data = token_raw_value.split(':')
        sensors = self.__sensors_repository.get_sensors()
        sensor_type, sensor_location = data
        for sensor in sensors:
            if sensor.location and sensor.location != sensor_location:
                continue
            if sensor.type != sensor_type:
                continue

            return sensor.value

        raise ParseException("Sensor with name {0} not found".format(token_raw_value))

    def get_supported_token(self) -> str:
        return Token.TYPE_SENSOR