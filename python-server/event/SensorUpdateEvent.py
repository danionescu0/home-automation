from blinker import signal
from typeguard import typechecked

from model.Sensor import Sensor


class SensorUpdateEvent:
    @typechecked()
    def send(self, sensor: Sensor):
        event = signal("sensor_update")
        self.sensor = sensor
        event.send(self)