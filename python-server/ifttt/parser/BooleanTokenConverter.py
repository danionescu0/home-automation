from ifttt.parser.TokenConverter import TokenConverter
from ifttt.parser.Token import Token


class BooleanTokenConverter(TokenConverter):
    def get_value(self, token_raw_value: str):
        return {'True' : True, 'False' : False}[token_raw_value]

    def get_supported_token(self) -> str:
        return Token.TYPE_LITERAL_BOOLEAN