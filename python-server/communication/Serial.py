import serial
from typing import Callable
from typeguard import typechecked

from communication.Base import Base

class Serial(Base):
    @typechecked()
    def __init__(self, endpoint: dict):
        self.__endpoint = endpoint
        self.__message_buffer = ''
        self.__serial = None

    def connect(self):
        self.__serial = serial.Serial(self.__endpoint['port'], self.__endpoint['baud_rate'], timeout=0.5)

        return self

    @typechecked()
    def disconnect(self) -> None:
        self.__serial.close()

    @typechecked()
    def send(self, which: str, value: bytes) -> bool:
        self.__serial.write(which.encode('ascii'))
        self.__serial.write(':'.encode('ascii'))
        self.__serial.write(value)

        return True

    @typechecked()
    def listen(self, complete_message_callback: Callable[[str], bool],
                   receive_message_callback: Callable[[str], None]):
        received_data = self.__serial.read().decode('utf-8')
        if received_data == False or received_data == '':
            return
        self.get_logger().debug("Senzors data received from serial: {0}".format(received_data))
        self.__message_buffer += received_data
        if not complete_message_callback(self.__message_buffer):
            return
        receive_message_callback(self.__message_buffer)
        self.__message_buffer = ''

    @typechecked()
    def __get_endpoint(self) -> str:
        return self.__endpoint