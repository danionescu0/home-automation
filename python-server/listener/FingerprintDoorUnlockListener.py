from blinker import signal

class FingerprintDoorUnlockListener:
    def __init__(self, actuator_commands, authentication):
        self.__actuator_commands = actuator_commands
        self.__authentication = authentication
        sensor_update =  signal("sensor_update")
        sensor_update.connect(self.callback)

    def callback(self, sensor_update):
        if self.__should_unlock_door(sensor_update):
            self.__actuator_commands.change_actuator('door', True)

    def __should_unlock_door(self, sensor_update):
        sensor_name = sensor_update.get_name()
        fingerprint_code = sensor_update.get_new_value()

        return sensor_name == 'fingerprint' and self.__authentication.verify_fingerprint_code(fingerprint_code)