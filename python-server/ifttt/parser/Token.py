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
    TYPE_CURRENT_TIME = 'time'
    TYPE_ACTUATOR = 'actuator'

    @typechecked()
    def __init__(self, raw_value: str, type: str, value):
        self.raw_value = raw_value
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return 'Token(raw_value: {0}, type: {1}, value: {2}, type_of_value: {3})'\
                .format(self.raw_value, self.type, self.value, type(self.value))