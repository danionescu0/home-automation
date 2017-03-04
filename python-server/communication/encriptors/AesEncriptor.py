from communication.encriptors.BaseEncriptor import BaseEncriptor
from Crypto.Cipher import AES

class AesEncriptor(BaseEncriptor):

    def __init__(self, key):
        self.__key = key
        self.__encriptor = None

    def encrypt(self, text):
        padded_text = text.ljust(16, ' ')
        encripted = self.__get_encriptor().encrypt(padded_text)
        string_i = ''
        for char in encripted:
            string_i += str(ord(char)) + ","

        return encripted

    def decrypt(self, text):
        return self.__get_encriptor().decrypt(text)

    def get_name(self):
        return 'aes'

    def __get_encriptor(self):
        if None != self.__encriptor:
            return self.__encriptor
        else:
            return AES.new(self.__key, AES.MODE_CBC, IV=self.__key)