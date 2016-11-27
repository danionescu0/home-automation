from blinker import signal
from tools.DaytimeMoments import DaytimeMoments

class FingerprintDoorUnlockListener:
    def __init__(self, actuator_commands, authentication):
        self.__actuator_commands = actuator_commands
        self.__authentication = authentication
        signal("sensor_update").connect(self.callback)

    def callback(self, sensor_update):
        if self.__should_unlock_door(sensor_update):
            self.__actuator_commands.change_actuator('door', True)
            if self.__should_open_lights():
                self.__actuator_commands.change_actuator('holwayLight', True)
                self.__actuator_commands.change_actuator('livingLight', True)

    def __should_unlock_door(self, sensor_update):
        sensor_type = sensor_update.get_type()
        fingerprint_code = str(sensor_update.get_new_value())

        return sensor_type == 'fingerprint' and self.__authentication.verify_fingerprint_code(fingerprint_code)

    def __should_open_lights(self):
        return DaytimeMoments.is_over_sunset()