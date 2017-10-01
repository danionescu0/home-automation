from ifttt.parser.TokenConverter import TokenConverter
from ifttt.parser.Token import Token
from ifttt.parser.ParseException import ParseException
from repository.ActuatorsRepository import ActuatorsRepository


class ActuatorTokenConverter(TokenConverter):
    def __init__(self, actuators_repository: ActuatorsRepository) -> None:
        self.__actuators_repository = actuators_repository

    def get_value(self, token_raw_value: str):
        actuators = self.__actuators_repository.get_actuators()
        if token_raw_value not in actuators:
            raise ParseException("Actuator with name {0} not found".format(token_raw_value))

        return actuators[token_raw_value].state

    def get_supported_token(self) -> str:
        return Token.TYPE_ACTUATOR