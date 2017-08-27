import abc
from typing import Callable
from logging import RootLogger

from typeguard import typechecked


class Base(metaclass=abc.ABCMeta):
    def __init__(self):
        self.__endpoint = None
        self.__callback = None
        self.__logger = None

    @typechecked()
    @abc.abstractmethod
    def send(self, which: str, value: bytes) -> bool:
        pass

    @typechecked()
    @abc.abstractmethod
    def listen(self, complete_message_callback: Callable[[str], bool], receive_message_callback: Callable[[str], None]):
        pass

    @abc.abstractmethod
    def connect(self):
        pass

    @typechecked()
    @abc.abstractmethod
    def disconnect(self) -> None:
        pass

    @typechecked()
    def set_receive_message_callback(self, callback: Callable[[str], bool]) -> None:
        self.__callback = callback

    @typechecked()
    def get_receive_message_callback(self) -> Callable[[str], None]:
        return self.__callback

    @typechecked()
    def set_logger(self, logger: RootLogger):
        self.__logger = logger

    @typechecked()
    def get_logger(self) -> RootLogger:
        return self.__logger