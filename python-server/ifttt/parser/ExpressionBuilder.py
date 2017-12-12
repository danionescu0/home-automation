from typeguard import typechecked
from logging import RootLogger

from ifttt.parser.ParseException import ParseException
from ifttt.interpretter.EqualsExpression import EqualsExpression
from ifttt.interpretter.BooleanOrExpression import BooleanOrExpression
from ifttt.interpretter.BooleanAndExpression import BooleanAndExpression
from ifttt.interpretter.LiteralExpression import LiteralExpression
from ifttt.interpretter.GreaterThanExpression import GreaterThanExpression
from ifttt.interpretter.LessThanExpression import LessThanExpression
from ifttt.interpretter.BetweenExpression import BetweenExpression
from ifttt.parser.Token import Token
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.interpretter.Expression import Expression


class ExpressionBuilder:
    current_token_index = 0

    @typechecked()
    def __init__(self, tokenizer: Tokenizer, logger: RootLogger):
        self.__tokenizer = tokenizer
        self.__current_token_index = 0
        self.__logger = logger

    @typechecked()
    def set_text(self, text: str) -> None:
        self.__text = text
        self.__expression = None

    def build(self):
        ExpressionBuilder.current_token_index = 0
        self.__tokens = self.__tokenizer.tokenize(self.__text)
        self.__expression = self.__evaluate()
        [self.__logger.info(token) for token in self.__tokens]

    @typechecked()
    def get_expression(self) -> Expression:
        return self.__expression

    def __evaluate(self):
        token = self.__get_current_token()
        token_type = token.type
        self.__next_token()
        if token_type in [Token.TYPE_LITERAL_BOOLEAN, Token.TYPE_LITERAL_INT, Token.TYPE_LITERAL_TIME,
                          Token.TYPE_ACTUATOR_STATE, Token.TYPE_SENSOR, Token.TYPE_ACTUATOR, Token.TYPE_CURRENT_TIME]:
            return LiteralExpression(token.value)

        left_expr = self.__evaluate()
        right_expr = self.__evaluate()
        if token_type == Token.TYPE_EXPR_BETWEEN:
            third_expr = self.__evaluate()
            return BetweenExpression(left_expr, right_expr, third_expr)
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

        raise ParseException("Token type {0} not implemented".format(token_type))

    def __get_current_token(self):
        return self.__tokens[ExpressionBuilder.current_token_index]

    def __next_token(self):
        ExpressionBuilder.current_token_index += 1