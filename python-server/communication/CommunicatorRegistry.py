from typeguard import typechecked

from communication.Base import Base
from communication.SerialBluetooth import SerialBluetooth
from communication.Serial import Serial
from communication.WemoSwitch import WemoSwitch
from logging import RootLogger

class CommunicatorRegistry:
    @typechecked()
    def __init__(self, configuration, logger: RootLogger):
        self.__configuration = configuration
        self.__logger = logger
        self.__communicators = {}

    def configure_communicators(self):
        serial = Serial(self.__configuration.serial)
        serial.set_logger(self.__logger)
        serial.connect()
        self.__communicators.update({'serial': serial})
        bluetooth = SerialBluetooth(self.__configuration.bluetooth['connections'])
        bluetooth.set_logger(self.__logger)
        bluetooth.connect()
        self.__communicators.update({'bluetooth' : bluetooth})
        wemo_switch = WemoSwitch()
        wemo_switch.set_logger(self.__logger)
        wemo_switch.connect()
        self.__communicators.update({'wemo_switch': wemo_switch})

    @typechecked()
    def get_communicator(self, type: str) -> Base:
        return self.__communicators[type]
