from communication.Bluetooth import Bluetooth
from communication.Serial import Serial

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

    def get_communicator(self, type):
        return self.__communicators[type]
