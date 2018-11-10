from typeguard import typechecked
from pydispatch import dispatcher

from communication.actuator.ActuatorCommands import ActuatorCommands
from event.SensorUpdateEvent import SensorUpdateEvent
from tools.Authentication import Authentication
from model.Sensor import Sensor
from listener.BaseListener import BaseListener


class FingerprintDoorUnlockListener(BaseListener):
    @typechecked()
    def __init__(self, actuator_commands: ActuatorCommands, authentication: Authentication):
        self.__actuator_commands = actuator_commands
        self.__authentication = authentication

    def connect(self):
        dispatcher.connect(self.listen, signal=SensorUpdateEvent.NAME, sender=dispatcher.Any)

    def listen(self, event: SensorUpdateEvent) -> None:
        if self.__should_unlock_door(event):
            self.__actuator_commands.change_actuator('door', True)
            self.__actuator_commands.change_actuator('homeAlarm', False)

    def __should_unlock_door(self, sensor_update: SensorUpdateEvent):
        fingerprint_code = str(sensor_update.sensor.value)

        return sensor_update.sensor.type == Sensor.SensorType.FINGERPRINT.value \
               and self.__authentication.verify_fingerprint_code(fingerprint_code)