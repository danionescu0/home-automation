import re

from ifttt.parser.Token import Token
from ifttt.parser.ParseException import ParseException

class Tokenizer:
    def __init__(self):
        self.__token_rules = [
            ('A\[(\w+)\]', Token.TYPE_ACTUATOR),
            ('S\[(\w+\:\w+)\]', Token.TYPE_SENSOR),
            ('TIME', Token.TYPE_TIME),
            ('gt', Token.TYPE_EXPR_GREATER),
            ('lt', Token.TYPE_EXPR_LESS),
            ('btw', Token.TYPE_EXPR_BETWEEN),
            ('eq', Token.TYPE_EXPR_EQUAL),
            ('and', Token.TYPE_BOOLEAN_AND),
            ('or', Token.TYPE_BOOLEAN_OR),
            ('True|False', Token.TYPE_LITERAL_BOOLEAN),
            ('[0-9]{1,2}\:[0-9]{1,2}', Token.TYPE_LITERAL_TIME),
            ('\d+', Token.TYPE_LITERAL_INT),
        ]

    def tokenize(self, text):
        cleanned_text = self.__get_cleanned_text(text)
        tokens = []
        for token_text in cleanned_text.split():
            tokens.append(self.__get_token(token_text))
            print self.__get_token(token_text).get_type() + ' with value ' + str(self.__get_token(token_text).get_value())

        return tokens

    def __get_cleanned_text(self, text):
        return re.sub('[(),]', ' ', text)

    def __get_token(self, token_text):
        for token_rule in self.__token_rules:
            found_matches = re.findall(token_rule[0], token_text)
            if not found_matches:
                continue
            return Token(token_rule[1], self.__get_token_value(token_rule[1], found_matches[0]))

        raise ParseException('Cannot parse symbol: {0}'.format(token_text))

    def __get_token_value(self, token_type, literal_value):
        if token_type == Token.TYPE_LITERAL_BOOLEAN:
            return {'True' : True, 'False' : False}[literal_value]
        elif token_type == Token.TYPE_LITERAL_INT:
            return int(literal_value)

        return literal_value

