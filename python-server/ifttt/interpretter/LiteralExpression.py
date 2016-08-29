from ifttt.interpretter.Expression import Expression

class LiteralExpression(Expression):
    def __init__(self, value):
        super(LiteralExpression, self).__init__()
        self.__value = value

    def interpret(self, context):
        context.set(self, self.__value)

