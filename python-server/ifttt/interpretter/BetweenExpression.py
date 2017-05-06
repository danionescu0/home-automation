from typeguard import typechecked

from ifttt.interpretter.Expression import Expression
from ifttt.interpretter.InterpretterContext import InterpretterContext

class BetweenExpression(Expression):
    @typechecked()
    def __init__(self, reference: Exception, left_operator: Expression, right_operator: Expression):
        super(BetweenExpression, self).__init__()
        self.__reference = reference
        self.__left_operator = left_operator
        self.__right_operator = right_operator

    @typechecked()
    def interpret(self, context: InterpretterContext):
        self.__reference.interpret(context)
        self.__left_operator.interpret(context)
        self.__right_operator.interpret(context)
        reference = context.lookup(self.__reference)
        left_result = context.lookup(self.__left_operator)
        right_result = context.lookup(self.__right_operator)

        context.set(self, left_result <= reference <= right_result)