from logging import RootLogger

from typeguard import typechecked

from communication.BaseSerial import BaseSerial
from communication.SerialBluetooth import SerialBluetooth
from communication.Serial import Serial


class SerialCommunicatorRegistry:
    @typechecked()
    def __init__(self, configuration, logger: RootLogger):
        self.__configuration = configuration
        self.__logger = logger
        self.__communicators = {}

    def configure_communicators(self):
        serial = Serial(self.__configuration['serial'])
        serial.set_logger(self.__logger)
        serial.connect()
        self.__communicators.update({'serial': serial})
        bluetooth = SerialBluetooth(self.__configuration['bluetooth']['connections'])
        bluetooth.set_logger(self.__logger)
        # bluetooth.connect()
        self.__communicators.update({'bluetooth' : bluetooth})

    @typechecked()
    def get_communicator(self, type: str) -> BaseSerial:
        return self.__communicators[type]