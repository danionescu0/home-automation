from model.SensorTypes import SensorTypes


class Sensor:
    SENSOR_TYPE_MAPPING = {
        'T': SensorTypes.TEMPERATURE.value,
        'H': SensorTypes.HUMIDITY.value,
        'PS': SensorTypes.PRESSURE.value,
        'L': SensorTypes.LIGHT.value,
        'R': SensorTypes.RAIN.value
    }

    def __init__(self, type: str, value: float) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return 'Sensor: type({0}), value({1})'.format(self.type, str(self.value))