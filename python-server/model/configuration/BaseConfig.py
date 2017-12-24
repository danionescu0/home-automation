import abc

from typeguard import typechecked


class BaseConfig:
    @typechecked()
    @abc.abstractmethod
    def main_description(self) -> str:
        pass

    @typechecked()
    @abc.abstractmethod
    def properties_description(self) -> dict:
        pass