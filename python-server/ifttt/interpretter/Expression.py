import abc
from typeguard import typechecked

class Expression(metaclass=abc.ABCMeta):
    keycount = 0

    def __init__(self):
        self.__key = 0

    @typechecked()
    @abc.abstractmethod
    def interpret(self, context) -> None:
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass

    def get_key(self):
        if self.__key is 0:
            Expression.keycount += 1
            self.__key = Expression.keycount

        return self.__key