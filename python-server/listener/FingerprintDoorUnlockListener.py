from typeguard import typechecked
from blinker import signal

from communication.actuator.ActuatorCommands import ActuatorCommands
from event.SensorUpdateEvent import SensorUpdateEvent
from tools.Authentication import Authentication
from model.Sensor import Sensor


class FingerprintDoorUnlockListener:
    @typechecked()
    def __init__(self, actuator_commands: ActuatorCommands, authentication: Authentication):
        self.__actuator_commands = actuator_commands
        self.__authentication = authentication
        signal("sensor_update").connect(self.callback)

    @typechecked()
    def callback(self, sensor_update: SensorUpdateEvent) -> None:
        if self.__should_unlock_door(sensor_update):
            self.__actuator_commands.change_actuator('door', True)
            self.__actuator_commands.change_actuator('homeAlarm', False)

    def __should_unlock_door(self, sensor_update: SensorUpdateEvent):
        fingerprint_code = str(sensor_update.sensor.value)

        return sensor_update.sensor.type == Sensor.SensorType.FINGERPRINT.value \
               and self.__authentication.verify_fingerprint_code(fingerprint_code)