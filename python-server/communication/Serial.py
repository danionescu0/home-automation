from logging import RootLogger
from typing import Callable

import serial
from typeguard import typechecked

from communication.BaseSerial import BaseSerial
from communication.exception.SerialDecodeException import SerialDecodeException
from model.configuration.SerialCommunicationCfg import SerialCommunicationCfg


class Serial(BaseSerial):
    @typechecked()
    def __init__(self, serial_communication_cfg: SerialCommunicationCfg, logger: RootLogger):
        self.__serial_communication_cfg = serial_communication_cfg
        self.__message_buffer = ''
        self.__serial = None
        self.__logger = logger

    def connect(self):
        self.__serial = serial.Serial(self.__serial_communication_cfg.port,
                                      self.__serial_communication_cfg.baud_rate,
                                      timeout=0.5)
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
        try:
            received_data = self.__serial.read().decode('utf-8')
        except UnicodeDecodeError as e:
            raise SerialDecodeException(e)
        if received_data is False or received_data == '':
            return
        self.__logger.info("Senzors data received from serial: {0}".format(received_data))
        self.__message_buffer += received_data
        if not complete_message_callback(self.__message_buffer):
            return
        receive_message_callback(self.__message_buffer)
        self.__message_buffer = ''