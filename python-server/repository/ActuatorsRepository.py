import collections
import json
from typing import Dict

from typeguard import typechecked

from repository.AbstractRepository import AbstractRepository
from model.Actuator import Actuator
from model.ActuatorProperties import ActuatorProperties


class ActuatorsRepository(AbstractRepository):
    REDIS_KEY = 'actuators'

    @typechecked()
    def __init__(self, redis_configuration: dict, actuators_config: dict):
        AbstractRepository.__init__(self, redis_configuration)
        self.keys = {self.REDIS_KEY: actuators_config}

    def get_actuators(self) -> Dict[str, Actuator]:
        actuators_data = self.get(self.REDIS_KEY)
        actuators = {}
        for id, data in actuators_data.items():
            actuator = Actuator(id, data['name'], data['value'], data['type'], data['room'], data['device_type'])
            actuator.properties = self.__get_actuator_properties(data['properties'])
            actuators[id] = actuator

        return collections.OrderedDict(sorted(actuators.items()))

    @typechecked()
    def set_actuator(self, name: str, value) -> None:
        return self.__set(self.REDIS_KEY, name, value)

    def __set(self, key, name, value):
        data = self.get(key)
        data[name]['value'] = value
        self.client.set(key, json.dumps(data))

    def __get_actuator_properties(self, properties: dict) -> ActuatorProperties:
        actuator_properties = ActuatorProperties()
        for name, value in properties.items():
            actuator_properties.set(name, value)

        return actuator_properties