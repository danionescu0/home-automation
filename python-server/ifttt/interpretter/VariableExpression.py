from typeguard import typechecked

from ifttt.interpretter.Expression import Expression
from ifttt.interpretter.InterpretterContext import InterpretterContext

class VariableExpression(Expression):
    @typechecked()
    def __init__(self, name: str, value):
        super(VariableExpression, self).__init__()
        self.__name = name
        self.__value = value

    @typechecked()
    def interpret(self, context: InterpretterContext):
        context.set(self, self.__value)

    def get_key(self):
        return self.__name

    def __eq__(self, other):
        return self.__name == other.name and self.__value == other.__value

    def __repr__(self):
        return 'Variable {0}({1})'.format(self.__name, self.__value)