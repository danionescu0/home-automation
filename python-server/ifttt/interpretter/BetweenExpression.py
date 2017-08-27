from typeguard import typechecked

from ifttt.interpretter.Expression import Expression
from ifttt.interpretter.InterpretterContext import InterpretterContext


class BetweenExpression(Expression):
    @typechecked()
    def __init__(self, reference: Expression, left_operator, right_operator):
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

    def __eq__(self, other):
        return self.__left_operator == other.__left_operator and self.__right_operator == other.__right_operator \
               and self.__reference == other.__reference

    def __repr__(self):
        return 'Between ({0}) and ({1})'.format(self.__left_operator, self.__right_operator)