from communication.Bluetooth import Bluetooth
from communication.Serial import Serial
from communication.WemoSwitch import WemoSwitch

class CommunicatorRegistry:
    def __init__(self, configuration, logger):
        self.__configuration = configuration
        self.__logger = logger
        self.__communicators = {}

    def configure_communicators(self):
        serial = Serial(self.__configuration.serial)
        serial.set_logger(self.__logger)
        serial.connect()
        self.__communicators.update({'serial': serial})
        bluetooth = Bluetooth(self.__configuration.bluetooth['connections'])
        bluetooth.set_logger(self.__logger)
        bluetooth.connect()
        self.__communicators.update({'bluetooth' : bluetooth})
        wemo_switch = WemoSwitch()
        wemo_switch.set_logger(self.__logger)
        wemo_switch.connect()
        self.__communicators.update({'wemo_switch': wemo_switch})

    def get_communicator(self, type):
        return self.__communicators[type]
