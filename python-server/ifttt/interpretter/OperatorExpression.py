import abc

from ifttt.interpretter.Expression import Expression

class OperatorExpression(Expression):
    def __init__(self, left_operator, right_operator):
        super(OperatorExpression, self).__init__()
        self.__left_operator = left_operator
        self.__right_operator = right_operator

    def interpret(self, context):
        self.__left_operator.interpret(context)
        self.__right_operator.interpret(context)
        left_result = context.lookup(self.__left_operator)
        right_result = context.lookup(self.__right_operator)
        self.do_interpret(context, left_result, right_result)

    @abc.abstractmethod
    def do_interpret(self, context, left_result, right_result):
        pass