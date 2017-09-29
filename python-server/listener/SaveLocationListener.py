from typeguard import typechecked
from blinker import signal

from event.LocationEvent import LocationEvent
from repository.LocationTrackerRepository import LocationTrackerRepository


class SaveLocationListener:
    @typechecked()
    def __init__(self, location_tracker : LocationTrackerRepository):
        self.location_tracker = location_tracker
        signal("location").connect(self.callback)

    @typechecked()
    def callback(self, location: LocationEvent) -> None:
        self.location_tracker.add_location_point(location.get_device_name(), location.get_latitude(), location.get_longitude())