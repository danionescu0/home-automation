from typeguard import typechecked

from ifttt.interpretter.Expression import Expression
from ifttt.interpretter.InterpretterContext import InterpretterContext

class LiteralExpression(Expression):
    def __init__(self, value):
        super(LiteralExpression, self).__init__()
        self.__value = value

    @typechecked()
    def interpret(self, context: InterpretterContext) -> None:
        context.set(self, self.__value)

    def __eq__(self, other):
        return self.__value == other.__value

    def __repr__(self):
        return 'Literal ({0})'.format(self.__value)