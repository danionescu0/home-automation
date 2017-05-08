from typeguard import typechecked
from blinker import signal
from typing import Tuple
from geopy.distance import vincenty

from repository.LocationTracker import LocationTracker
from repository.Sensors import Sensors
from event.LocationEvent import LocationEvent

class SetPhoneIsHomeListener:
    HOME_RADIUS = 0.5

    @typechecked()
    def __init__(self, home_coordonates: Tuple[float, float], sensors_repo: Sensors, location_tracker: LocationTracker):
        self.__home_coordonates = home_coordonates
        self.__location_tracker = location_tracker
        self.__sensors_repo = sensors_repo
        signal("location").connect(self.callback)

    @typechecked()
    def callback(self, location: LocationEvent) -> None:
        currentCoordonates = (location.get_latitude(), location.get_longitude())
        distance_from_home = vincenty(self.__home_coordonates, currentCoordonates).km
        phone_is_home = distance_from_home < self.HOME_RADIUS
        self.__sensors_repo.set_sensor('phoneIsHome', False, phone_is_home)