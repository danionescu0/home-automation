from blinker import signal

class saveLocationListener:
    def __init__(self):
        location = signal("location")
        location.connect(self.callback)
        print("listener connected")

    def callback(self, data):
        print "call"
        print data.getLatitude()
