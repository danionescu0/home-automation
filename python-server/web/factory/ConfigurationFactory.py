import json
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
    def from_request_data(self, data: str) -> Dict[str, BaseConfig]:
        decoded = json.loads(data)
        configuration = {}
        for object_properties in decoded:
            configurationClass = globals()[object_properties['name']]
            enabled = object_properties['properties']['_enabled']
            object_properties['properties'].pop('_enabled')
            configurationInstance = configurationClass(
                **self.__get_processed_properties(object_properties['properties'])
            )
            configurationInstance.enabled = enabled
            configuration[object_properties['name']] = configurationInstance

        return configuration

    def __get_processed_properties(self, properties: dict):
        formatted = {}
        for name, value in properties.items():
            try:
                formatted.update({name: json.loads(value)})
            except Exception as e:
                print(value, e)
                formatted.update({name: value})

        return formatted
