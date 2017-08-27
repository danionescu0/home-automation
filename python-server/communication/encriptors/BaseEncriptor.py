import abc

from typeguard import typechecked


class BaseEncriptor(metaclass=abc.ABCMeta):
    @typechecked()
    @abc.abstractmethod
    def encrypt(self, text: str) -> bytes:
        pass

    @typechecked()
    @abc.abstractmethod
    def decrypt(self, text: str) -> str:
        pass

    @typechecked()
    @abc.abstractmethod
    def get_name(self) -> str:
        pass