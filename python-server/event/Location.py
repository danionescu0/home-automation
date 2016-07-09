from blinker import signal

class Location:
    def send(self, deviceName, latitude, longitude):
        event = signal("location")
        self.__deviceName = deviceName
        self.__latitude = latitude
        self.__longitude = longitude
        event.send(self)

    def getDeviceName(self):
        return self.__deviceName

    def getLatitude(self):
        return self.__latitude

    def getLongitude(self):
        return self.__longitude