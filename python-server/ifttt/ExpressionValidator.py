from typeguard import typechecked

from ifttt.parser.ExpressionBuilder import ExpressionBuilder
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.parser.ParseException import ParseException
from repository.Sensors import Sensors
from repository.Actuators import Actuators


class ExpressionValidator:
    @typechecked()
    def __init__(self, sensors_repo: Sensors, actuators_repo: Actuators):
        self.__sensors_repo = sensors_repo
        self.__actuators_repo = actuators_repo
        self.__error = None

    @typechecked()
    def is_valid(self, rule: str) -> bool:
        expression_builder = ExpressionBuilder(Tokenizer(), self.__sensors_repo, self.__actuators_repo)
        expression_builder.set_text(rule)
        try:
            expression_builder.build()
        except ParseException as e:
            self.__error = e
            return False

        return True

    @typechecked()
    def get_error(self, rule: str) -> str:
        self.is_valid(rule)

        return self.__error.message