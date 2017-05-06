from typeguard import typechecked

from ifttt.interpretter.OperatorExpression import OperatorExpression
from ifttt.interpretter.InterpretterContext import InterpretterContext
from ifttt.interpretter.Expression import Expression

class GreaterThanExpression(OperatorExpression):
    @typechecked()
    def do_interpret(self, context: InterpretterContext, left_result: Expression, right_result: Expression) -> None:
        context.set(self, left_result > right_result)