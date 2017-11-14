import abc

from typeguard import typechecked


class BaseStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    @typechecked()
    def supports(self, actuator_name: str) -> bool:
        pass

    @typechecked()
    @abc.abstractmethod
    def set_state(self, actuator_name: str, state) -> bool:
        pass