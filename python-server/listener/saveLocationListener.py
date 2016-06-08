from blinker import signal

class saveLocationListener:
    def __init__(self, locationTracker):
        self.locationTracker = locationTracker
        location = signal("location")
        location.connect(self.callback)

    def callback(self, location):
        self.locationTracker.addLocationPoint(location.getDeviceName(), location.getLatitude(), location.getLongitude())