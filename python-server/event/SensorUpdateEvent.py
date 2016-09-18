from blinker import signal

class SensorUpdateEvent:
    def send(self, type, location, new_value):
        event = signal("sensor_update")
        self.__type = type
        self.__location = location
        self.__new_value = new_value
        event.send(self)

    def get_type(self):
        return self.__type

    def get_location(self):
        return self.__location

    def get_new_value(self):
        return self.__new_value