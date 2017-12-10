import abc

from typeguard import typechecked
from model.Actuator import Actuator


class BaseStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    @typechecked()
    def supports(self, actuator: Actuator) -> bool:
        pass

    @typechecked()
    @abc.abstractmethod
    def set_state(self, actuator: Actuator, state) -> bool:
        pass