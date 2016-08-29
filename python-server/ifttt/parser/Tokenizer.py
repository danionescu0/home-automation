from ifttt.parser.Token import Token

class Tokenizer:
    def tokenize(self, text):
        return [
            Token(Token.TYPE_BOOLEAN_AND, None),
            Token(Token.TYPE_EXPR_EQUAL, None),
            Token(Token.TYPE_ACTUATOR, 'homeAlarm'),
            Token(Token.TYPE_LITERAL, False),
            Token(Token.TYPE_BOOLEAN_OR, None),
            Token(Token.TYPE_EXPR_GREATER, None),
            Token(Token.TYPE_SENSOR, 'light'),
            Token(Token.TYPE_LITERAL, 18),
            Token(Token.TYPE_EXPR_GREATER, None),
            Token(Token.TYPE_SENSOR, 'temperature'),
            Token(Token.TYPE_LITERAL, 25)
        ]