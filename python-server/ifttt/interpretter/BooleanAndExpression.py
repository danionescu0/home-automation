from ifttt.interpretter.OperatorExpression import OperatorExpression

class BooleanAndExpression(OperatorExpression):
    def do_interpret(self, context, left_result, right_result):
        context.set(self, left_result and right_result)