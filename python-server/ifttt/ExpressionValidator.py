from typeguard import typechecked

from ifttt.parser.ExpressionBuilder import ExpressionBuilder
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.parser.ParseException import ParseException


class ExpressionValidator:
    @typechecked()
    def __init__(self, tokenizer: Tokenizer):
        self.__tokenizer = tokenizer
        self.__error = None

    @typechecked()
    def is_valid(self, rule: str) -> bool:
        expression_builder = ExpressionBuilder(self.__tokenizer)
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

        return str(self.__error)