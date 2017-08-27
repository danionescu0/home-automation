from typeguard import typechecked

from ifttt.interpretter.OperatorExpression import OperatorExpression
from ifttt.interpretter.InterpretterContext import InterpretterContext


class BooleanOrExpression(OperatorExpression):
    @typechecked()
    def do_interpret(self, context: InterpretterContext, left_result, right_result) -> None:
        context.set(self, left_result or right_result)

    def __repr__(self):
        return 'Or ({0}) and ({1})'.format(self.__left_operator, self.__right_operator)