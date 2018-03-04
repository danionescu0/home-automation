from typeguard import typechecked
from blinker import signal
from typing import Tuple
from geopy.distance import vincenty

from repository.LocationTrackerRepository import LocationTrackerRepository
from repository.SensorsRepository import SensorsRepository
from event.LocationEvent import LocationEvent
from model.Sensor import Sensor


class SetPhoneIsHomeListener:
    HOME_RADIUS = 0.5

    @typechecked()
    def __init__(self, home_coordonates: Tuple[float, float], sensors_repo: SensorsRepository,
                 location_tracker: LocationTrackerRepository):
        self.__home_coordonates = home_coordonates
        self.__location_tracker = location_tracker
        self.__sensors_repo = sensors_repo
        signal("location").connect(self.callback)

    @typechecked()
    def callback(self, location: LocationEvent) -> None:
        current_coordonates = (location.get_latitude(), location.get_longitude())
        distance_from_home = vincenty(self.__home_coordonates, current_coordonates).km
        phone_is_home = distance_from_home < self.HOME_RADIUS
        sensor = Sensor('phoneIsHome', Sensor.SensorType.PHONE_IS_HOME.value, False,
                        phone_is_home, Sensor.DeviceType.ACTION.value)
        self.__sensors_repo.set_sensor(sensor)