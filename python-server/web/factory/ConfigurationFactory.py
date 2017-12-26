from typing import Dict

from typeguard import typechecked

from model.configuration.BaseConfig import BaseConfig
from model.configuration.BluetoothCommunicationCfg import BluetoothCommunicationCfg
from model.configuration.EmailCfg import EmailCfg
from model.configuration.HomeDefenceCfg import HomeDefenceCfg
from model.configuration.SerialCommunicationCfg import SerialCommunicationCfg
from model.configuration.ZwaveCommunicationCfg import ZwaveCommunicationCfg

class ConfigurationFactory:
    @typechecked()
    def from_request_data(self, data: dict) -> Dict[str, BaseConfig]:
        configuration = []

        return configuration