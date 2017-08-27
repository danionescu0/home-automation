from typeguard import typechecked

from communication.encriptors.BaseEncriptor import BaseEncriptor


class PlainTextEncriptor(BaseEncriptor):
    @typechecked()
    def encrypt(self, text: str) -> bytes:
        return str.encode(text)

    @typechecked()
    def decrypt(self, text: str) -> str:
        return text

    @typechecked()
    def get_name(self) -> str:
        return 'plain'