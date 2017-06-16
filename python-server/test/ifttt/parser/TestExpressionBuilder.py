import unittest

from ifttt.parser.ExpressionBuilder import ExpressionBuilder
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.parser.Token import Token
from ifttt.interpretter.EqualsExpression import EqualsExpression
from ifttt.interpretter.BooleanOrExpression import BooleanOrExpression
from ifttt.interpretter.BooleanAndExpression import BooleanAndExpression
from ifttt.interpretter.LiteralExpression import LiteralExpression
from ifttt.interpretter.GreaterThanExpression import GreaterThanExpression
from ifttt.interpretter.InterpretterContext import InterpretterContext

class TestExpressionBuilder(unittest.TestCase):

    def __get_tokenizer(self, rule):
        tokens = {
                'eq(TIME, 20:26)' :
                    [
                        Token(Token.TYPE_EXPR_EQUAL, 'eq'),
                        Token(Token.TYPE_CURRENT_TIME, '20:26'),
                        Token(Token.TYPE_LITERAL_TIME, '20:26'),
                    ],
                     'and  ( eq(S[phoneIsHome:False], True), or (gt(TIME, 08:52)), eq(A[homeAlarm, On], True) )':
                         [
                             Token(Token.TYPE_BOOLEAN_AND, 'and'),
                             Token(Token.TYPE_EXPR_EQUAL, 'eq'),
                             Token(Token.TYPE_ACTUATOR, False),
                             Token(Token.TYPE_LITERAL_BOOLEAN, True),
                             Token(Token.TYPE_BOOLEAN_OR, 'or'),
                             Token(Token.TYPE_EXPR_GREATER, 'gt'),
                             Token(Token.TYPE_LITERAL_TIME, '08:49'),
                             Token(Token.TYPE_LITERAL_TIME, '08:52'),
                             Token(Token.TYPE_EXPR_EQUAL, 'eq'),
                             Token(Token.TYPE_ACTUATOR, True),
                             Token(Token.TYPE_LITERAL_BOOLEAN, True),
                         ]
                 }[rule]

        Tokenizer.__init__ = lambda self: None
        tokenizer = Tokenizer()
        tokenizer.tokenize = lambda self: tokens

        return tokenizer

    def test_simple_expression(self):
        buildt_statement = self.__get_expresion_builder('eq(TIME, 20:26)')
        expected_statement = EqualsExpression(
            LiteralExpression('20:26'),
            LiteralExpression('20:26'),
        )
        self.assertEqual(buildt_statement, expected_statement)

    def test_elaborate_expression(self):
        rule = "and  ( eq(S[phoneIsHome:False], True), or (gt(TIME, 08:52)), eq(A[homeAlarm, On], True) )"
        buildt_statement = self.__get_expresion_builder(rule)
        expected_statement = BooleanAndExpression(
            EqualsExpression(LiteralExpression(False), LiteralExpression(True)),
            BooleanOrExpression(
            GreaterThanExpression(LiteralExpression('08:49'), LiteralExpression('08:52')),
                EqualsExpression(LiteralExpression(True), LiteralExpression(True))
            )
        )

        context = InterpretterContext()
        expected_statement.interpret(context)
        self.assertEqual(buildt_statement, expected_statement)

    def __get_expresion_builder(self, rule):
        tokenizer = self.__get_tokenizer(rule)
        expression_builder = ExpressionBuilder(tokenizer)
        expression_builder.set_text(rule)
        expression_builder.build()

        return expression_builder.get_expression()

