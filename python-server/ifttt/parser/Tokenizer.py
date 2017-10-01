import re
from typing import List
from logging import RootLogger

from typeguard import typechecked

from ifttt.parser.Token import Token
from ifttt.parser.ParseException import ParseException
from ifttt.parser.TokenConverter import TokenConverter

class Tokenizer:
    __token_rules = [
        ('A\[(\w+)\]', Token.TYPE_ACTUATOR),
        ('S\[(\w+\:\w+)\]', Token.TYPE_SENSOR),
        ('TIME', Token.TYPE_CURRENT_TIME),
        ('gt', Token.TYPE_EXPR_GREATER),
        ('lt', Token.TYPE_EXPR_LESS),
        ('btw', Token.TYPE_EXPR_BETWEEN),
        ('eq', Token.TYPE_EXPR_EQUAL),
        ('and', Token.TYPE_BOOLEAN_AND),
        ('or', Token.TYPE_BOOLEAN_OR),
        ('True|False', Token.TYPE_LITERAL_BOOLEAN),
        ('On|Off', Token.TYPE_ACTUATOR_STATE),
        ('[0-9]{1,2}\:[0-9]{1,2}', Token.TYPE_LITERAL_TIME),
        ('\d+', Token.TYPE_LITERAL_INT),
    ]

    def __init__(self, root_logger: RootLogger) -> None:
        self.__root_logger = root_logger
        self.__token_converters = []

    def add_token_converter(self, token_converter: TokenConverter):
        self.__token_converters.append(token_converter)

    @typechecked()
    def tokenize(self, text: str) -> List[Token]:
        return [self.__get_token(token_text) for token_text in self.__get_cleanned_text(text).split()]

    def __get_cleanned_text(self, text : str) -> str:
        return re.sub('[(),]', ' ', text)

    def __get_token(self, token_text: str) -> Token:
        for token_rule in self.__token_rules:
            found_matches = re.findall(token_rule[0], token_text)
            if not found_matches:
                continue

            return Token(token_rule[1], self.__get_token_value(token_rule[1], found_matches[0]))

        raise ParseException('Cannot parse token symbol: {0}'.format(token_text))

    def __get_token_value(self, token_type: str, token_raw_value: str):
        token_converter = [converter
                           for converter in self.__token_converters if converter.get_supported_token() == token_type]
        if 1 != len(token_converter):
            return token_raw_value
        token_converter = token_converter[0]
        value = token_converter.get_value(token_raw_value)

        return value