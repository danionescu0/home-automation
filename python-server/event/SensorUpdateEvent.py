from blinker import signal

class SensorUpdateEvent:
    def send(self, name, new_value):
        event = signal("sensor_update")
        self.__name = name
        self.__new_value = new_value
        event.send(self)

    def get_name(self):
        return self.__name

    def get_new_value(self):
        return self.__new_value