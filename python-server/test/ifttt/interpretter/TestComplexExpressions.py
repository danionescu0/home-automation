import unittest

from ifttt.interpretter.InterpretterContext import InterpretterContext
from ifttt.interpretter.VariableExpression import VariableExpression
from ifttt.interpretter.BooleanOrExpression import BooleanOrExpression
from ifttt.interpretter.BooleanAndExpression import BooleanAndExpression
from ifttt.interpretter.LiteralExpression import LiteralExpression
from ifttt.interpretter.GreaterThanExpression import GreaterThanExpression
from ifttt.interpretter.LessThanExpression import LessThanExpression
from ifttt.interpretter.EqualsExpression import EqualsExpression
from ifttt.interpretter.BetweenExpression import BetweenExpression

class TestComplexExpressions(unittest.TestCase):
    def test_complex1(self):
        context = InterpretterContext()
        statement = BooleanAndExpression(
            BooleanOrExpression(
                GreaterThanExpression(
                    LiteralExpression(5),
                    LiteralExpression(9)
                ),
                EqualsExpression(
                    VariableExpression("test1", 150),
                    VariableExpression("test2", 150)
                )
            ),
            LessThanExpression(
                LiteralExpression(9),
                VariableExpression("test3", 10)
            )
        )
        statement.interpret(context)
        self.assertEqual(context.lookup(statement), True)

    def test_complex2(self):
        context = InterpretterContext()
        statement = BooleanAndExpression(
            EqualsExpression(
                LiteralExpression(9),
                LiteralExpression(9)
            ),
            GreaterThanExpression(
                LiteralExpression(5),
                LiteralExpression(9)
            )
        )
        statement.interpret(context)
        self.assertEqual(context.lookup(statement), False)

    def test_between(self):
        context = InterpretterContext()
        statement = BetweenExpression(
            LiteralExpression(9),
            VariableExpression("test1", 1),
            LiteralExpression(10)
        )
        statement.interpret(context)
        self.assertEqual(context.lookup(statement), True)
        statement = BetweenExpression(
            LiteralExpression(9),
            VariableExpression("test1", 1),
            LiteralExpression(8)
        )
        statement.interpret(context)
        self.assertEqual(context.lookup(statement), False)