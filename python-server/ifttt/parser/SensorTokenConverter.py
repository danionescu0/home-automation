from ifttt.parser.TokenConverter import TokenConverter
from ifttt.parser.Token import Token
from ifttt.parser.ParseException import ParseException
from repository.SensorsRepository import SensorsRepository


class SensorTokenConverter(TokenConverter):
    def __init__(self, sensors_repository: SensorsRepository) -> None:
        self.__sensors_repository = sensors_repository

    def get_value(self, token_raw_value: str):
        sensor = self.__sensors_repository.get_sensor(token_raw_value)
        if None is not sensor:
            return sensor.value

        raise ParseException("Sensor with id {0} not found".format(token_raw_value))

    def get_supported_token(self) -> str:
        return Token.TYPE_SENSOR