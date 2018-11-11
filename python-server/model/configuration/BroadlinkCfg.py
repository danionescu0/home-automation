import abc

from typeguard import typechecked

from model.configuration.BaseConfig import BaseConfig


class BroadlinkCfg(BaseConfig, metaclass=abc.ABCMeta):
    @typechecked()
    def __init__(self, host: str, mac_address: str) -> None:
        self.host = host
        self.mac_address = mac_address
        super(BroadlinkCfg, self).__init__()

    @typechecked()
    def main_description(self) -> str:
        return 'Broadlink configuration settings'

    @typechecked()
    def properties_description(self) -> dict:
        return {
            'host' : 'Hostname of the device ex: 192.168.0.105',
            'mac_address': "Mac address of the device ex: 34EA3442D59E"
        }