import abc

from typeguard import typechecked

from communication.encriptors.BaseEncriptor import BaseEncriptor


class BaseStrategy(metaclass=abc.ABCMeta):
    def __init__(self):
        self.__encriptor = None

    @abc.abstractmethod
    @typechecked()
    def supports(self, actuator_name: str) -> bool:
        pass

    @typechecked()
    def set_encription(self, encriptor: BaseEncriptor):
        self.__encriptor = encriptor
        return self

    @typechecked()
    def get_encriptor(self) -> BaseEncriptor:
        return self.__encriptor

    @typechecked()
    @abc.abstractmethod
    def set_state(self, actuator_name: str, state) -> bool:
        pass