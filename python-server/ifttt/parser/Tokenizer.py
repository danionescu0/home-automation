import re

from ifttt.parser.Token import Token

class Tokenizer:
    def __init__(self):
        self.__token_rules = [
            ('A\[(\w+)\]', Token.TYPE_ACTUATOR),
            ('S\[(\w+)\]', Token.TYPE_SENSOR),
            ('T\[([0-9]{1,2}\:[0-9]{1,2})]', Token.TYPE_TIME),
            ('gt', Token.TYPE_EXPR_GREATER),
            ('lt', Token.TYPE_EXPR_LESS),
            ('eq', Token.TYPE_EXPR_EQUAL),
            ('and', Token.TYPE_BOOLEAN_AND),
            ('or', Token.TYPE_BOOLEAN_OR),
            ('True|False|\d+', Token.TYPE_LITERAL),
        ]

    def tokenize(self, text):
        cleanned_text = self.__get_cleanned_text(text)
        tokens = []
        for token_text in cleanned_text.split():
            tokens.append(self.__get_token(token_text))
            print self.__get_token(token_text).get_type() + ' with value ' +self.__get_token(token_text).get_value()

        return tokens

        #
        # return [
        #     Token(Token.TYPE_BOOLEAN_AND, None),
        #     Token(Token.TYPE_EXPR_EQUAL, None),
        #     Token(Token.TYPE_ACTUATOR, 'homeAlarm'),
        #     Token(Token.TYPE_LITERAL, 'False'),
        #     Token(Token.TYPE_BOOLEAN_OR, None),
        #     Token(Token.TYPE_EXPR_GREATER, None),
        #     Token(Token.TYPE_SENSOR, 'light'),
        #     Token(Token.TYPE_LITERAL, '18'),
        #     Token(Token.TYPE_EXPR_EQUAL, None),
        #     Token(Token.TYPE_SENSOR, 'temperature'),
        #     Token(Token.TYPE_LITERAL, '26')
        # ]

    def __get_cleanned_text(self, text):
        return re.sub('[(),]', ' ', text)

    def __get_token(self, token_text):
        for token_rule in self.__token_rules:
            found_matches = re.findall(token_rule[0], token_text)
            if not found_matches:
                continue
            return Token(token_rule[1], found_matches[0])

        raise Exception('Cannot parse symbol: {0}'.format(token_text))


