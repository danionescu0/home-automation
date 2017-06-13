import unittest
from unittest.mock import patch

from ifttt.parser.ExpressionBuilder import ExpressionBuilder
from ifttt.parser.Tokenizer import Tokenizer
from ifttt.parser.Token import Token


class TestExpressionBuilder(unittest.TestCase):

    def __get_tokenizer(self, rule):
        tokens = {
                'eq(TIME, 20:26)' :
                    [
                        Token(Token.TYPE_EXPR_EQUAL, 'eq'),
                        Token(Token.TYPE_CURRENT_TIME, 'TIME'),
                        Token(Token.TYPE_LITERAL_TIME, '20:26'),
                    ]
                 }[rule]
        def mock_tokenize(tokens):
            return tokens

        def mock_init(self):
            pass

        Tokenizer.__init__ = mock_init
        tokenizer = Tokenizer()
        tokenizer.tokenize = mock_tokenize(tokens)

        return tokenizer


    # @patch('ifttt.parser.Tokenizer')
    def test_simple_expression(self):

        rule = "eq(TIME, 20:26)"
        # tokenizer.tokenize.return_value = self.__get_tokenizer(rule)
        # tokenizer.tokenize.return_value = [
        #                 Token(Token.TYPE_EXPR_EQUAL, 'eq'),
        #                 Token(Token.TYPE_CURRENT_TIME, 'TIME'),
        #                 Token(Token.TYPE_LITERAL_TIME, '20:26'),
        #             ]
        tokenizer = self.__get_tokenizer(rule)
        print(tokenizer.tokenize(rule))
        expression_builder = ExpressionBuilder(tokenizer)
        expression_builder.set_text(rule)
        expression_builder.build()
        statement = expression_builder.get_expression()

