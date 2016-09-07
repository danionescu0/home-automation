from datetime import datetime
from dateutil import tz

from ifttt.interpretter.EqualsExpression import EqualsExpression
from ifttt.interpretter.BooleanOrExpression import BooleanOrExpression
from ifttt.interpretter.BooleanAndExpression import BooleanAndExpression
from ifttt.interpretter.LiteralExpression import LiteralExpression
from ifttt.interpretter.GreaterThanExpression import GreaterThanExpression
from ifttt.interpretter.LessThanExpression import LessThanExpression
from ifttt.parser.Token import Token

class ExpressionBuilder:
    current_token_index = 0

    def __init__(self, tokenizer, sensors_repo, actuators_repo):
        self.__tokenizer = tokenizer
        self.__sensors_repo = sensors_repo
        self.__actuators_repo = actuators_repo
        self.__current_token_index = 0

    def set_text(self, text):
        self.__text = text
        self.__expression = None

    def build(self):
        ExpressionBuilder.current_token_index = 0
        self.__tokens = self.__tokenizer.tokenize(self.__text)
        self.__actuators = self.__actuators_repo.get_actuators()
        self.__sensors = self.__sensors_repo.get_sensors()
        self.__expression = self.__evaluate()

    def get_expression(self):
        return self.__expression

    def __evaluate(self):
        token = self.__get_current_token()
        token_type = token.get_type()
        self.__next_token()
        if token_type in [Token.TYPE_LITERAL_BOOLEAN, Token.TYPE_LITERAL_INT, Token.TYPE_LITERAL_TIME]:
            return LiteralExpression(token.get_value())
        elif token_type == Token.TYPE_SENSOR:
            return LiteralExpression(self.__get_senzor_value(token.get_value()))
        elif token_type == Token.TYPE_ACTUATOR:
            return LiteralExpression(self.__get_actuator_value(token.get_value()))
        elif token_type == Token.TYPE_TIME:
            return LiteralExpression(self.__get_time_value())

        left_expr = self.__evaluate()
        right_expr = self.__evaluate()
        if token_type == Token.TYPE_EXPR_EQUAL:
            return EqualsExpression(left_expr, right_expr)
        elif token_type == Token.TYPE_BOOLEAN_AND:
            return BooleanAndExpression(left_expr, right_expr)
        elif token_type == Token.TYPE_BOOLEAN_OR:
            return BooleanOrExpression(left_expr, right_expr)
        elif token_type == Token.TYPE_EXPR_GREATER:
            return GreaterThanExpression(left_expr, right_expr)
        elif token_type == Token.TYPE_EXPR_LESS:
            return LessThanExpression(left_expr, right_expr)

        raise Exception("Token type {0} not implemented".format(token_type))

    def __get_current_token(self):
        return self.__tokens[ExpressionBuilder.current_token_index]

    def __next_token(self):
        ExpressionBuilder.current_token_index += 1

    def __get_senzor_value(self, senzor_name):
        for senzor in self.__sensors:
            if senzor['name'] == senzor_name:
                print "sensor: {0} with value: {1}".format(senzor['name'], senzor['value'])
                return senzor['value']

        raise Exception("Sensor with name {0} not found".format(senzor_name))

    def __get_actuator_value(self, actuator_name):
        if actuator_name not in self.__actuators:
            raise Exception("Actuator with name {0} not found".format(actuator_name))

        print "actuator: {0} with value: {1}".format(actuator_name, self.__actuators[actuator_name]['state'])
        return self.__actuators[actuator_name]['state']

    def __get_time_value(self):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Bucharest')
        initial_date = datetime.now().replace(tzinfo=from_zone)
        local_date = initial_date.astimezone(to_zone)
        print "time is {0}".format(local_date.strftime('%H:%M'))

        return local_date.strftime('%H:%M')