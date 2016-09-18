from blinker import signal
from geopy.distance import vincenty

class SetPhoneIsHomeListener:
    HOME_RADIUS = 0.5

    def __init__(self, home_coordonates, sensors_repo, location_tracker):
        self.__home_coordonates = home_coordonates
        self.__location_tracker = location_tracker
        self.__sensors_repo = sensors_repo
        location = signal("location")
        location.connect(self.callback)

    def callback(self, location):
        currentCoordonates = (location.get_latitude(), location.get_longitude())
        distance_from_home = vincenty(self.__home_coordonates, currentCoordonates)
        phone_is_home = distance_from_home < self.HOME_RADIUS
        self.__sensors_repo.set_sensor('phoneIsHome', False, phone_is_home)
        print(distance_from_home)
        print(phone_is_home)
