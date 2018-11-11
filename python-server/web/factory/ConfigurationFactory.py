import json
from typing import Dict
from ast import literal_eval

from typeguard import typechecked

from model.configuration.BaseConfig import BaseConfig
from model.configuration.BluetoothCommunicationCfg import BluetoothCommunicationCfg
from model.configuration.EmailCfg import EmailCfg
from model.configuration.HomeDefenceCfg import HomeDefenceCfg
from model.configuration.SerialCommunicationCfg import SerialCommunicationCfg
from model.configuration.ZwaveCommunicationCfg import ZwaveCommunicationCfg
from model.configuration.GeneralCfg import GeneralCfg
from model.configuration.RemoteSpeakerCfg import RemoteSpeakerCfg
from model.configuration.BroadlinkCfg import BroadlinkCfg


class ConfigurationFactory:
    @typechecked()
    def from_request_data(self, data: str) -> Dict[str, BaseConfig]:
        decoded = json.loads(data)
        configuration = {}
        for object_properties in decoded:
            configuration_class = globals()[object_properties['name']]
            enabled = object_properties['properties']['_enabled']
            object_properties['properties'].pop('_enabled')
            configuration_instance = configuration_class(
                **self.__get_processed_properties(object_properties['properties'])
            )
            configuration_instance.enabled = enabled
            configuration[object_properties['name']] = configuration_instance

        return configuration

    def __get_processed_properties(self, properties: dict):
        formatted = {}
        for name, value in properties.items():
            try:
                formatted.update({name: literal_eval(value)})
            except Exception as e:
                formatted.update({name: value})

        return formatted
