from blinker import signal
from typeguard import typechecked


class LocationEvent:
    @typechecked()
    def send(self, device_name: str, latitude: float, longitude: float):
        event = signal("location")
        self.__device_name = device_name
        self.__latitude = latitude
        self.__longitude = longitude
        event.send(self)

    @typechecked()
    def get_device_name(self) -> str:
        return self.__device_name

    @typechecked()
    def get_latitude(self) -> float:
        return self.__latitude

    @typechecked()
    def get_longitude(self) -> float:
        return self.__longitude