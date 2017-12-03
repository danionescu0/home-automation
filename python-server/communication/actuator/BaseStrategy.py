import abc

from typeguard import typechecked


class BaseStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    @typechecked()
    def supports(self, id: str) -> bool:
        pass

    @typechecked()
    @abc.abstractmethod
    def set_state(self, id: str, state) -> bool:
        pass