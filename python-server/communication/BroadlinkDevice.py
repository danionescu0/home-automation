from logging import RootLogger

from typeguard import typechecked
import broadlink

from communication.DeviceLifetimeCycles import DeviceLifetimeCycles
from model.configuration.BroadlinkCfg import BroadlinkCfg


class BroadlinkDevice(DeviceLifetimeCycles):
    __DEFAULT_TYPE = 0x2712
    __IR_TOKEN = 0x26
    __TICK = 32.84
    __PORT = 80

    @typechecked()
    def __init__(self, broadlink_cfg: BroadlinkCfg, root_logger: RootLogger) -> None:
        self.__broadlink_cfg = broadlink_cfg
        self.__root_logger = root_logger
        self.__dev = None

    def disconnect(self) -> None:
        pass

    def connect(self):
        mac = bytearray.fromhex(self.__broadlink_cfg.mac_address)
        self.__dev = broadlink.gendevice(self.__DEFAULT_TYPE, (self.__broadlink_cfg.host, self.__PORT), mac)
        self.__dev.auth()

    @typechecked()
    def send(self, command: str):
        self.__root_logger.info('Sending broadlink command: {0}'.format(command))
        try:
            data = bytearray.fromhex(''.join(command))
            self.__dev.send_data(data)
        except Exception as e:
            self.__root_logger.info('Sending broadlink command failed: {0}'.format(e.message))
            return False

        return True