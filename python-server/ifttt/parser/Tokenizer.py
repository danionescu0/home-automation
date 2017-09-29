import re
from typing import List
from datetime import datetime
from dateutil import tz

from typeguard import typechecked
from tools.DateUtils import DateUtils

from ifttt.parser.Token import Token
from ifttt.parser.ParseException import ParseException
from repository.SensorsRepository import SensorsRepository
from repository.ActuatorsRepository import ActuatorsRepository


class Tokenizer:
    __token_rules = [
        ('A\[(\w+)\]', Token.TYPE_ACTUATOR),
        ('S\[(\w+\:\w+)\]', Token.TYPE_SENSOR),
        ('TIME', Token.TYPE_CURRENT_TIME),
        ('gt', Token.TYPE_EXPR_GREATER),
        ('lt', Token.TYPE_EXPR_LESS),
        ('btw', Token.TYPE_EXPR_BETWEEN),
        ('eq', Token.TYPE_EXPR_EQUAL),
        ('and', Token.TYPE_BOOLEAN_AND),
        ('or', Token.TYPE_BOOLEAN_OR),
        ('True|False', Token.TYPE_LITERAL_BOOLEAN),
        ('On|Off', Token.TYPE_ACTUATOR_STATE),
        ('[0-9]{1,2}\:[0-9]{1,2}', Token.TYPE_LITERAL_TIME),
        ('\d+', Token.TYPE_LITERAL_INT),
    ]

    def __init__(self, sensors_repo: SensorsRepository, actuators_repo: ActuatorsRepository):
        self.__sensors_repo = sensors_repo
        self.__actuators_repo = actuators_repo
        self.__actuators = None
        self.__sensors = None

    @typechecked()
    def tokenize(self, text:str) -> List[Token]:
        self.__actuators = self.__actuators_repo.get_actuators()
        self.__sensors = self.__sensors_repo.get_sensors()
        cleanned_text = self.__get_cleanned_text(text)

        return [self.__get_token(token_text) for token_text in cleanned_text.split()]

    def __get_cleanned_text(self, text):
        return re.sub('[(),]', ' ', text)

    def __get_token(self, token_text):
        for token_rule in self.__token_rules:
            found_matches = re.findall(token_rule[0], token_text)
            if not found_matches:
                continue
            return Token(token_rule[1], self.__get_token_value(token_rule[1], found_matches[0]))

        raise ParseException('Cannot parse symbol: {0}'.format(token_text))

    def __get_token_value(self, token_type, literal_value):
        if token_type == Token.TYPE_LITERAL_BOOLEAN:
            return {'True' : True, 'False' : False}[literal_value]
        elif token_type == Token.TYPE_ACTUATOR_STATE:
            return {'On' : True, 'Off' : False}[literal_value]
        elif token_type == Token.TYPE_LITERAL_INT:
            return int(literal_value)
        elif token_type == Token.TYPE_ACTUATOR:
            return self.__get_actuator_value(literal_value)
        elif token_type == Token.TYPE_SENSOR:
            return self.__get_sensor_value(literal_value)
        elif token_type == Token.TYPE_CURRENT_TIME:
            return self.__get_current_time()

        return literal_value

    def __get_sensor_value(self, sensor_data):
        data = sensor_data.split(':')
        sensor_type = data[0]
        sensor_location = data[1]
        for sensor in self.__sensors:
            if sensor.location and sensor.location != sensor_location:
                continue
            if sensor.type != sensor_type:
                continue

            return sensor.value

        raise ParseException("Sensor with name {0} not found".format(sensor_data))

    def __get_actuator_value(self, actuator_name):
        if actuator_name not in self.__actuators:
            raise ParseException("Actuator with name {0} not found".format(actuator_name))

        return self.__actuators[actuator_name]['state']

    def __get_current_time(self):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(DateUtils.get_timezone())
        initial_date = datetime.now().replace(tzinfo=from_zone)
        local_date = initial_date.astimezone(to_zone)

        return local_date.strftime('%H:%M')