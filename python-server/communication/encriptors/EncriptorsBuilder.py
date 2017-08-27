from typing import List

from typeguard import typechecked

from communication.encriptors.AesEncriptor import AesEncriptor
from communication.encriptors.PlainTextEncriptor import PlainTextEncriptor
from communication.encriptors.BaseEncriptor import BaseEncriptor


class EncriptorsBuilder():
    @typechecked()
    def __init__(self, aes_key: str) -> None:
        self.__aes_key = aes_key
        self.__encription_strategies = None

    def build(self):
        if None != self.__encription_strategies:
            return self
        self.__encription_strategies = []
        self.__encription_strategies.append(PlainTextEncriptor())
        self.__encription_strategies.append(AesEncriptor(self.__aes_key))

        return self

    @typechecked()
    def get_encriptors(self) -> List[BaseEncriptor]:
        return self.__encription_strategies