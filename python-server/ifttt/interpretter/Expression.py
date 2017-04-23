import abc

class Expression(metaclass=abc.ABCMeta):
    keycount = 0

    def __init__(self):
        self.__key = 0

    @abc.abstractmethod
    def interpret(self, context):
        pass

    def get_key(self):
        if self.__key is 0:
            Expression.keycount += 1
            self.__key = Expression.keycount

        return self.__key