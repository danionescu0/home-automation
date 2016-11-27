from blinker import signal

class SaveLocationListener:
    def __init__(self, locationTracker):
        self.locationTracker = locationTracker
        signal("location").connect(self.callback)

    def callback(self, location):
        self.locationTracker.add_location_point(location.get_device_name(), location.get_latitude(), location.get_longitude())