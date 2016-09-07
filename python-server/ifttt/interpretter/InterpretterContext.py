class InterpretterContext:
    def __init__(self):
        self.__expressions = {}

    def set(self, expression, value):
        self.__expressions[expression.get_key()] = value

    def lookup(self, expression):
        return self.__expressions[expression.get_key()]