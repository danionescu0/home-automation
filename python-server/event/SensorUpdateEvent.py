from blinker import signal
from typeguard import typechecked

class SensorUpdateEvent:
    @typechecked()
    def send(self, type: str, location: str, new_value):
        event = signal("sensor_update")
        self.__type = type
        self.__location = location
        self.__new_value = new_value
        event.send(self)

    @typechecked()
    def get_type(self) -> str:
        return self.__type

    @typechecked()
    def get_location(self) -> str:
        return self.__location

    def get_new_value(self):
        return self.__new_value