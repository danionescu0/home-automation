import abc
from typeguard import typechecked

from ifttt.interpretter.Expression import Expression
from ifttt.interpretter.InterpretterContext import InterpretterContext

class OperatorExpression(Expression):
    @typechecked()
    def __init__(self, left_operator: Expression, right_operator: Expression):
        super(OperatorExpression, self).__init__()
        self.__left_operator = left_operator
        self.__right_operator = right_operator

    @typechecked()
    def interpret(self, context: InterpretterContext):
        self.__left_operator.interpret(context)
        self.__right_operator.interpret(context)
        left_result = context.lookup(self.__left_operator)
        right_result = context.lookup(self.__right_operator)
        self.do_interpret(context, left_result, right_result)

    @typechecked()
    @abc.abstractmethod
    def do_interpret(self, context: InterpretterContext, left_result: Expression, right_result: Expression) -> None:
        pass