from enum import Enum

from model.SensorProperties import SensorProperties


class Sensor:
    class SensorType(Enum):
        HUMIDITY = 'humidity'
        TEMPERATURE = 'temperature'
        AIR_PRESSURE = 'airPressure'
        LIGHT = 'light'
        VOLTAGE = 'voltage'
        RAIN = 'rain'
        PRESENCE = 'presence'
        AIR_POLLUTION = 'airPollution'
        FINGERPRINT = 'fingerprint'
        PHONE_IS_HOME = 'phoneIsHome'
        FLOOD = 'flood'
        POWER = 'power'

    class DeviceType(Enum):
        SERIAL = 'serial'
        ZWAVE = 'zwave'
        ACTION = 'action'

    def __init__(self, id: str, type: str, location: str, value, device_type: str, last_updated: int) -> None:
        self.id = id
        self.type = type
        self.location = location
        self.value = value
        self.device_type = device_type
        self.last_updated = last_updated
        self._properties = None

    @property
    def properties(self) -> SensorProperties:
        return self._properties

    @properties.setter
    def properties(self, value: SensorProperties):
        self._properties = value

    def __repr__(self) -> str:
        return "Sensor: id({0}), type({1}), location({2}), value({3}), device_type({4})," \
               " properties({5}), last_updated({6})".format(self.id, self.type, self.location, self.value,
                                         self.device_type, self._properties, self.last_updated)