from blinker import signal

class Location:
    def send(self, deviceName, latitude, longitude):
        event = signal("location")
        self.__deviceName = deviceName
        self.__latitude = latitude
        self.__longitude = longitude
        event.send(self)

    def get_device_name(self):
        return self.__deviceName

    def get_latitude(self):
        return self.__latitude

    def get_longitude(self):
        return self.__longitude