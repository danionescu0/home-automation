from typeguard import typechecked

from model.Sensor import Sensor


class SensorUpdateEvent:
    NAME = 'sensor_update'

    @typechecked()
    def __init__(self, sensor: Sensor):
        self.sensor = sensor