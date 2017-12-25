import abc

from typeguard import typechecked


class BaseConfig:
    def __init__(self) -> None:
        self._enabled = False

    @typechecked()
    @abc.abstractmethod
    def main_description(self) -> str:
        pass

    @typechecked()
    @abc.abstractmethod
    def properties_description(self) -> dict:
        pass

    @property
    def enabled(self) -> bool:
        return self._enabled if hasattr(self, '_enabled') else False

    @enabled.setter
    def enabled(self, state: bool):
        self._enabled = state

    @classmethod
    def get_classname(cls) -> str:
        return cls.__name__