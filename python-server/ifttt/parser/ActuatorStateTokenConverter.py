from ifttt.parser.TokenConverter import TokenConverter
from ifttt.parser.Token import Token


class ActuatorStateTokenConverter(TokenConverter):
    def get_value(self, token_raw_value: str):
        return {'On' : True, 'Off' : False}[token_raw_value]

    def get_supported_token(self) -> str:
        return Token.TYPE_ACTUATOR_STATE