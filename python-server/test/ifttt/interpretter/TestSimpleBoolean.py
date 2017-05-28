import unittest

from ifttt.interpretter.InterpretterContext import InterpretterContext
from ifttt.interpretter.VariableExpression import VariableExpression
from ifttt.interpretter.BooleanOrExpression import BooleanOrExpression
from ifttt.interpretter.BooleanAndExpression import BooleanAndExpression
from ifttt.interpretter.LiteralExpression import LiteralExpression

class TestSimpleBoolean(unittest.TestCase):
    def test_with_logical_and_true(self):
        context = InterpretterContext()
        statement = self.__get_simple_boolean_and(True)
        statement.interpret(context)
        self.assertEqual(context.lookup(statement), True)
        statement = self.__get_simple_boolean_and(False)
        statement.interpret(context)
        self.assertEqual(context.lookup(statement), False)

    def test_with_logical_or_true(self):
        context = InterpretterContext()
        statement = self.__get_simple_boolean_or(True)
        statement.interpret(context)
        self.assertEqual(context.lookup(statement), True)
        statement = self.__get_simple_boolean_or(False)
        statement.interpret(context)
        self.assertEqual(context.lookup(statement), False)

    def __get_simple_boolean_or(self, will_return):
        return BooleanOrExpression(
            LiteralExpression(False),
            VariableExpression('test', will_return)
        )

    def __get_simple_boolean_and(self, will_return):
        return BooleanAndExpression(
            LiteralExpression(will_return),
            VariableExpression('test', will_return)
        )
