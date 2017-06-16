from typeguard import typechecked
from Crypto.Cipher import AES

from communication.encriptors.BaseEncriptor import BaseEncriptor

class AesEncriptor(BaseEncriptor):
    @typechecked()
    def __init__(self, key: str):
        self.__key = key
        self.__encriptor = None

    @typechecked()
    def encrypt(self, text: str) -> bytes:
        if len(text) > 16:
            raise RuntimeError("Aes encription does not handle more than 16 characters")
        padded_text = text.ljust(16, ' ')
        encripted = self.__get_encriptor().encrypt(padded_text)

        return encripted

    @typechecked()
    def decrypt(self, text: str) -> str:
        return self.__get_encriptor().decrypt(text)

    @typechecked()
    def get_name(self) -> str:
        return 'aes'

    def __get_encriptor(self):
        if None != self.__encriptor:
            return self.__encriptor
        else:
            return AES.new(self.__key, AES.MODE_CBC, IV=self.__key)