from typing import Dict

import jsonpickle
from typeguard import typechecked

from repository.AbstractRepository import AbstractRepository
from model.configuration.BaseConfig import BaseConfig
from model.configuration.BluetoothCommunicationCfg import BluetoothCommunicationCfg
from model.configuration.EmailCfg import EmailCfg
from model.configuration.HomeDefenceCfg import HomeDefenceCfg
from model.configuration.SerialCommunicationCfg import SerialCommunicationCfg
from model.configuration.ZwaveCommunicationCfg import ZwaveCommunicationCfg
from model.configuration.RemoteSpeakerCfg import RemoteSpeakerCfg
from model.configuration.GeneralCfg import GeneralCfg


class ConfigurationRepository(AbstractRepository):
    __REDIS_KEY = 'configuration'

    @typechecked()
    def __init__(self, configuration: dict):
        AbstractRepository.__init__(self, configuration)

    @typechecked()
    def get_config(self, name: str):
        config = self.__get()
        return config[name] if name in config else self.__get_default_configurations()[name]

    @typechecked()
    def get_all(self) -> Dict[str, BaseConfig]:
        return {**self.__get_default_configurations(), **self.__get()}

    @typechecked()
    def set_all(self, new_config: Dict[str, BaseConfig]):
        config = {**self.__get(), **new_config}

        return self.client.set(self.__REDIS_KEY, jsonpickle.encode(config))

    def __get(self) -> dict:
        config = self.client.get(self.__REDIS_KEY)
        if config:
            return jsonpickle.decode(config.decode("utf-8"))

        return {}

    def __get_default_configurations(self) -> Dict[str, BaseConfig]:
        return {
            BluetoothCommunicationCfg.get_classname(): BluetoothCommunicationCfg({}),
            EmailCfg.get_classname(): EmailCfg('', ''),
            HomeDefenceCfg.get_classname(): HomeDefenceCfg(0, [], 0, ''),
            SerialCommunicationCfg.get_classname(): SerialCommunicationCfg('', 0),
            ZwaveCommunicationCfg.get_classname(): ZwaveCommunicationCfg('', ''),
            GeneralCfg.get_classname(): GeneralCfg((0.0, 0.0), ''),
            RemoteSpeakerCfg.get_classname(): RemoteSpeakerCfg('192.168.0.1', 'some_user', 'some_password'),
        }