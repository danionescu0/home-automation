from ifttt.interpretter.OperatorExpression import OperatorExpression

class BooleanOrExpression(OperatorExpression):
    def do_interpret(self, context, left_result, right_result):
        context.set(self, left_result or right_result)