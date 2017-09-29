import collections
import json
from typing import Dict

from typeguard import typechecked

from repository.AbstractRepository import AbstractRepository
from model.Actuator import Actuator

class ActuatorsRepository(AbstractRepository):
    REDIS_KEY = 'actuators'

    @typechecked()
    def __init__(self, redis_configuration: dict, actuators_config: dict):
        AbstractRepository.__init__(self, redis_configuration)
        self.keys = {self.REDIS_KEY: actuators_config}

    def get_actuators(self) -> Dict[str, Actuator]:
        actuators_data = self.get(self.REDIS_KEY)
        actuators = {}
        for name, data in actuators_data.items():
            actuator = Actuator(name, data['state'], data['device_type'])
            actuator.type = data['type']
            actuator.room = data['room']
            actuator.strategy = data['strategy']
            actuator.communicator = data['communicator']
            actuator.send_to_device = data['send_to_device']
            actuator.command = data['command']
            actuator.encription = data['encription']
            actuators[name] = actuator

        return collections.OrderedDict(sorted(actuators.items()))

    @typechecked()
    def set_actuator(self, name: str, value) -> None:
        return self.__set(self.REDIS_KEY, name, value)

    def __set(self, key, name, value):
        data = self.get(key)
        data[name]['state'] = value
        self.client.set(key, json.dumps(data))