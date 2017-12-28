import abc

from typeguard import typechecked

from model.configuration.BaseConfig import BaseConfig


class SerialCommunicationCfg(BaseConfig, metaclass=abc.ABCMeta):
    @typechecked()
    def __init__(self, port: str, baud_rate: int) -> None:
        self.port = port
        self.baud_rate = baud_rate
        super(SerialCommunicationCfg, self).__init__()

    @typechecked()
    def main_description(self) -> str:
        return 'Serial communication'

    @typechecked()
    def properties_description(self) -> dict:
        return {
            'port' : 'The port for serial comm, ex: /dev/ttyUSB0',
            'baud_rate' : 'Baud rate for port, ex: 9600 (default)'
        }