from typeguard import typechecked
from pydispatch import dispatcher

from event.LocationEvent import LocationEvent
from repository.LocationTrackerRepository import LocationTrackerRepository
from listener.BaseListener import BaseListener


class SaveLocationListener(BaseListener):
    @typechecked()
    def __init__(self, location_tracker : LocationTrackerRepository):
        self.location_tracker = location_tracker

    def connect(self):
        dispatcher.connect(self.listen, signal=LocationEvent.NAME, sender=dispatcher.Any)

    def listen(self, event: LocationEvent) -> None:
        self.location_tracker.add_location_point(event.get_device_name(),
                                                 event.get_latitude(), event.get_longitude())