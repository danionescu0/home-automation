import abc

from typeguard import typechecked

from model.configuration.BaseConfig import BaseConfig


class BluetoothCommunicationCfg(BaseConfig, metaclass=abc.ABCMeta):
    @typechecked()
    def __init__(self, connections: dict) -> None:
        self.connections = connections
        super(BluetoothCommunicationCfg, self).__init__()

    @typechecked()
    def main_description(self) -> str:
        return 'Bluetooth'

    @typechecked()
    def properties_description(self) -> dict:
        return {
            'connections' : 'Bluetooth communication dict, ex: { \'holway\' : \'20:14:21:26:10:26\','
                            ' \'fingerprint\': \'20:25:12:22:47:86\'}'
        }