from ifttt.interpretter.OperatorExpression import OperatorExpression

class GreaterThanExpression(OperatorExpression):
    def do_interpret(self, context, left_result, right_result):
        context.set(self, left_result > right_result)