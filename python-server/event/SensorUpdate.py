from blinker import signal

class SensorUpdate:
    def send(self, name, newValue):
        event = signal("sensor_update")
        self.__name = name
        self.__newValue = newValue
        event.send(self)

    def getName(self):
        return self.__name

    def getNewValue(self):
        return self.__newValue