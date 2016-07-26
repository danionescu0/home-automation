from blinker import signal

class FingerprintDoorUnlockListener:
    def __init__(self, data_container, actuator_commands):
        self.__dataContainer = data_container
        self.__actuator_commands = actuator_commands
        sensor_update =  signal("sensor_update")
        sensor_update.connect(self.callback)

    def callback(self, sensor_update):
        if self.__should_unlock_door(sensor_update):
            self.__actuator_commands.change_actuator('door', True)

    def __should_unlock_door(self, sensor_update):
        sensorName = sensor_update.get_name()
        sensorValue = sensor_update.get_new_value()
        return sensorName == 'fingerprint' and sensorValue > -1