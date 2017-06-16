import abc
from typeguard import typechecked

from ifttt.interpretter.Expression import Expression
from ifttt.interpretter.InterpretterContext import InterpretterContext

class OperatorExpression(Expression):
    def __init__(self, left_operator, right_operator):
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
    def do_interpret(self, context: InterpretterContext, left_result, right_result) -> None:
        pass

    def __eq__(self, other):
        return self.__left_operator == other.__left_operator and self.__right_operator == other.__right_operator