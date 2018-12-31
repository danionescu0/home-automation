import serial
from typing import Callable


class Serial():
    def __init__(self, port: str, baud: str) -> None:
        self.__port = port
        self.__baud = baud

    def connect(self):
        self.__serial = serial.Serial(self.__port, self.__baud, timeout=0.5)

    def disconnect(self) -> None:
        self.__serial.close()

    def listen(self, complete_message_callback: Callable[[str], bool], receive_message_callback: Callable[[str], None]):
        received_data = self.__serial.read().decode('utf-8')
        if received_data is False or received_data == '':
            return
        self.__message_buffer += received_data
        if not complete_message_callback(self.__message_buffer):
            return
        receive_message_callback(self.__message_buffer)
        self.__message_buffer = ''
