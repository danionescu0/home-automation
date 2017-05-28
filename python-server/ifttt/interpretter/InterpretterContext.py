from typeguard import typechecked

from ifttt.interpretter.Expression import Expression

class InterpretterContext:
    def __init__(self):
        self.__expressions = {}

    @typechecked()
    def set(self, expression: Expression, value):
        self.__expressions[expression.get_key()] = value

    @typechecked()
    def lookup(self, expression: Expression):
        return self.__expressions[expression.get_key()]