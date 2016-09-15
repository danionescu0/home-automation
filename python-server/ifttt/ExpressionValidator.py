from ifttt.parser.ExpressionBuilder import ExpressionBuilder
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.parser.ParseException import ParseException

class ExpressionValidator:
    def __init__(self, sensors_repo, actuators_repo):
        self.__sensors_repo = sensors_repo
        self.__actuators_repo = actuators_repo
        self.__error = None

    def is_valid(self, rule):
        expression_builder = ExpressionBuilder(Tokenizer(), self.__sensors_repo, self.__actuators_repo)
        expression_builder.set_text(rule)
        try:
            expression_builder.build()
        except ParseException as e:
            self.__error = e
            return False

        return True

    def get_error(self, rule):
        self.is_valid(rule)

        return self.__error.message