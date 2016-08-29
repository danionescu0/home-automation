from ifttt.interpretter.Expression import Expression

class VariableExpression(Expression):
    def __init__(self, name, value):
        super(VariableExpression, self).__init__()
        self.__name = name
        self.__value = value

    def interpret(self, context):
        context.set(self, self.__value)

    def get_key(self):
        return self.__name