from communication.encriptors.BaseEncriptor import BaseEncriptor

class PlainTextEncriptor(BaseEncriptor):
    def encrypt(self, text):
        return text

    def decrypt(self, text):
        return text

    def get_name(self):
        return 'plain'