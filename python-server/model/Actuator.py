from enum import Enum

from model.ActuatorProperties import ActuatorProperties


class Actuator:
    class ActuatorType(Enum):
        PUSHBUTTON = 'pushbutton'
        SWITCH = 'switch'
        DIMMER = 'dimmer'
        MAX_DIMMER_VALUE = 255

    class DeviceType(Enum):
        SERIAL = 'serial'
        GROUP = 'group'
        WEMO = 'wemo'
        ZWAVE = 'zwave'
        ACTION = 'action'

    def __init__(self, id: str, name: str, value, type: str, room: str, device_type: str) -> None:
        self.id = id
        self.name = name
        self.value = value
        self.type = type
        self.room = room
        self.device_type = device_type
        self._properties = None

    @property
    def properties(self) -> ActuatorProperties:
        return self._properties

    @properties.setter
    def properties(self, value: ActuatorProperties):
        self._properties = value

    def __repr__(self) -> str:
        return "Actuator: id({0}), name({1}), value({2}), type({3}), room({4})," \
               " communicator({5}), properties({6})".\
                format(self.id, self.name, self.value, self.type, self.room, self.device_type, self.properties)