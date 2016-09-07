from ifttt.interpretter.Expression import Expression

class BetweenExpression(Expression):
    def __init__(self, reference, left_operator, right_operator):
        super(BetweenExpression, self).__init__()
        self.__reference = reference
        self.__left_operator = left_operator
        self.__right_operator = right_operator

    def interpret(self, context):
        self.__reference.interpret(context)
        self.__left_operator.interpret(context)
        self.__right_operator.interpret(context)
        reference = context.lookup(self.__reference)
        left_result = context.lookup(self.__left_operator)
        right_result = context.lookup(self.__right_operator)

        context.set(self, left_result <= reference <= right_result)