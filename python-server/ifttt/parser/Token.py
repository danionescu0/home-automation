class Token:
    TYPE_BOOLEAN_AND = 'and'
    TYPE_BOOLEAN_OR = 'or'
    TYPE_EXPR_EQUAL = 'eq'
    TYPE_EXPR_GREATER = 'gt'
    TYPE_EXPR_LESS = 'lt'
    TYPE_LITERAL = 'literal'
    TYPE_SENSOR = 'sensor'
    TYPE_TIME = 'time'
    TYPE_ACTUATOR = 'actuator'

    def __init__(self, type, value):
        self.__type = type
        self.__value = value

    def get_type(self):
        return self.__type

    def get_value(self):
        return self.__value