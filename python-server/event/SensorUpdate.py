from blinker import signal

class SensorUpdate:
    def send(self, name, newValue):
        event = signal("sensor_update")
        self.__name = name
        self.__newValue = newValue
        event.send(self)

    def get_name(self):
        return self.__name

    def get_new_value(self):
        return self.__newValue