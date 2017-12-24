import abc

from typeguard import typechecked

from model.configuration.BaseConfig import BaseConfig


class ZwaveCommunicationCfg(BaseConfig, metaclass=abc.ABCMeta):
    @typechecked()
    def __init__(self, port: str, openzwave_config_path: str) -> None:
        self.port = port
        self.openzwave_config_path = openzwave_config_path

    @typechecked()
    def main_description(self) -> str:
        return 'Zwave communication'

    @typechecked()
    def properties_description(self) -> dict:
        return {
            'port' : 'The serial port used for communication with the zwave device, ex: /dev/ttyUSB1',
            'openzwave_config_path' : 'The path of the openzwave config (download_path/config)'
        }