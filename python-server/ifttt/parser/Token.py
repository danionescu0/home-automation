from typeguard import typechecked


class Token:
    TYPE_BOOLEAN_AND = 'and'
    TYPE_BOOLEAN_OR = 'or'
    TYPE_EXPR_EQUAL = 'eq'
    TYPE_EXPR_GREATER = 'gt'
    TYPE_EXPR_BETWEEN = 'btw'
    TYPE_EXPR_LESS = 'lt'
    TYPE_LITERAL_BOOLEAN = 'literal_bool'
    TYPE_ACTUATOR_STATE = 'actuator_state'
    TYPE_LITERAL_INT = 'literal_int'
    TYPE_LITERAL_TIME = 'literal_time'
    TYPE_SENSOR = 'sensor'
    TYPE_SENSOR_LAST_UPDATED = 'sensor_last_updated'
    TYPE_CURRENT_TIME = 'time'
    TYPE_ACTUATOR = 'actuator'

    @typechecked()
    def __init__(self, raw_value: str, type: str, value):
        self.raw_value = raw_value
        self.type = type
        self.value = value

    @staticmethod
    def is_literal(type: str):
        return True if type in [Token.TYPE_LITERAL_BOOLEAN, Token.TYPE_LITERAL_INT, Token.TYPE_LITERAL_TIME,
                          Token.TYPE_ACTUATOR_STATE, Token.TYPE_SENSOR, Token.TYPE_ACTUATOR,
                          Token.TYPE_CURRENT_TIME, Token.TYPE_SENSOR_LAST_UPDATED] else False

    def __repr__(self) -> str:
        return 'Token(raw_value: {0}, type: {1}, value: {2}, type_of_value: {3})'\
                .format(self.raw_value, self.type, self.value, type(self.value))