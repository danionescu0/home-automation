from typeguard import typechecked
from Crypto.Cipher import AES


class AesEncriptor:
    @typechecked()
    def __init__(self, key: str):
        self.__key = key
        self.__encriptor = None

    @typechecked()
    def encrypt(self, text: str) -> bytes:
        if len(text) > 16:
            raise RuntimeError("Aes encription does not handle more than 16 characters")
        padded_text = text.ljust(16, ' ')
        return self.__get_encriptor().encrypt(padded_text.encode())

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
            return AES.new(self.__key.encode(), AES.MODE_CBC, IV=self.__key.encode())